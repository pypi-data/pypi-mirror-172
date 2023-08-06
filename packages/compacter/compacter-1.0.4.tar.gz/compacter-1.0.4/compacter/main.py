import argparse
import fnmatch
import io
import itertools
import json
import operator
import os
import re
import sys
import time
import tqdm
import traceback

import dask.bag as db
import fsspec
import pyarrow
import pyarrow.parquet as pq
import s3fs


def fsprotocol(fs):
    p = fs.protocol
    if isinstance(p, str):
        return p
    return p[0]


def fillcolumns(a, fields):
    cols = {field.name: field.type for field in fields}
    ex = set(a.column_names)
    for c in set(cols) - ex:
        a = a.append_column(
            pyarrow.field(c, cols[c]),
            pyarrow.array([None] * len(a), cols[c])
        )
    return a.select(list(cols) + sorted(set(a.column_names) - set(cols)))


def shared_items(item_lists):
    return list(map(operator.itemgetter(0), itertools.takewhile(
        lambda _: len(set(_)) == 1,
        [list(filter(None, _)) for _ in itertools.zip_longest(*item_lists)]
    )))


def concat_unique(item_lists):
    head = shared_items(item_lists)
    return head + list({item for l in item_lists for item in l[len(head):]})


def laxconcat(tables):
    tables = list(filter(None, tables))
    if not tables:
        return None
    fields = concat_unique([list(table.schema) for table in tables])
    return pyarrow.concat_tables([
        fillcolumns(table, fields)
        for table in tables
        if table is not None
    ]).combine_chunks()


def singledir(
    in_,
    out,
    infs,
    filepath_column,
    all_fields,
    npartitions_per_file,
    per_file_split_every
):
    return (
        db.from_sequence(
            infs.glob(os.path.join(in_, "**")),
            npartitions=npartitions_per_file
        )
        .map(f"{fsprotocol(infs)}://{{}}".format)
        .map(lambda f: (f, pq.read_table(io.BytesIO(infs.open(f).read()), use_threads=False)))
        .starmap(lambda f, table: table.append_column(
                pyarrow.field(filepath_column, pyarrow.string()),
                pyarrow.array([f] * len(table), pyarrow.string())
        ))
        .map(fillcolumns, all_fields)
        .reduction(laxconcat, laxconcat, split_every=per_file_split_every)
        .apply(lambda table: (
            pq.write_table(table, out),
            out
        )[1])
        .compute()
    )


def successful_tasks(l, client):
    futs = [
        (args, kwargs, client.submit(func, *args, **kwargs))
        for func, args, kwargs in l
    ]
    res = []
    for args, kwargs, f in futs:
        try:
            res.append(f.result())
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"error args=[{args}], kwargs=[{kwargs}]", file=sys.stderr)
            print(
                ''.join(traceback.format_exception(None, e, e.__traceback__)),
                file=sys.stderr
            )
    return res


def get_fields(files, infs, last_fields, partition_size=50, npartitions=None):
    set_last_fields = set(last_fields)
    return (
        db.from_sequence(
            files,
            partition_size=partition_size,
            npartitions=npartitions
        )
        .map_partitions(lambda files: [
            set(pq.read_schema(infs.open(f, "rb"))) - set_last_fields
            for f in files
        ])
        .reduction(
            lambda ss: {f for s in ss for f in s},
            lambda ss: {f for s in ss for f in s}
        )
    )


def get_triples(
    input_path,
    infs,
    input_pattern,
    output_path
) -> "[(inputdir, outputfile, outputexists)]":
    return (
        db.from_sequence(infs.glob(input_path))
        .map(f"{fsprotocol(infs)}://{{}}".format)
        .map(lambda in_: (
            in_,
            re.sub(input_pattern, output_path, in_)
        ))
        .starmap(lambda in_, out: (
            in_,
            out,
            fsspec.open(out).fs.isfile(out)
        ))
        .compute()
    )


def compactify(
    input_path: str,
    input_pattern: str,
    output_path: str,
    filepath_column: str,
    client: "dask.distributed.Client",
    overlap: int=1,
    per_file_split_every: int=16,
    npartitions_per_file: int=128,
    highest_priority: int=0,
):
    existing_ins = fsspec.open_files(input_path)
    infs = existing_ins.fs
    existing_ins = [f"{fsprotocol(infs)}://{f}" for f in infs.glob(input_path)]

    ismatch = [(fnmatch.fnmatch(f, input_path), f) for f in existing_ins]
    ismatch, f = min(ismatch)
    assert ismatch, (
        f"you must use protocol in input path like fsspec would."
        f"fsspec file path that didn't match input path: {f}"
    )

    triples = get_triples(input_path, infs, input_pattern, output_path)

    existing_pairs = sorted(a for *a, exists in triples if exists)
    overlapping = existing_pairs[len(existing_pairs) - overlap:]
    newouts = sorted(a for *a, exists in triples if not exists)
    pairs = overlapping + newouts

    last_fields = []
    if len(existing_pairs):
        last_fields = list(pq.read_schema(
            fsspec.open(max(out for _, out in existing_pairs)).open()
        ))

    all_infiles = (
        db.from_sequence(pairs)
        .starmap(lambda in_, _: infs.glob(os.path.join(in_, "**")))
        .flatten()
        .compute()
    )
    new_fields = get_fields(all_infiles, infs, last_fields).compute()

    all_fields = last_fields + list(new_fields)

    highest_priority = highest_priority or len(pairs)
    tasks = successful_tasks([
        (
            singledir,
            (
                in_, out, infs, filepath_column, all_fields,
                npartitions_per_file, per_file_split_every
            ),
            dict(priority=highest_priority - i)
        )
        for i, (in_, out) in enumerate(pairs)
    ], client=client)
    
    return tasks


def get_argparser():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_path", type=str)
    ap.add_argument("input_pattern", type=str)
    ap.add_argument("output_path", type=str)
    ap.add_argument("filepath_column", type=str)
    ap.add_argument("--dask-kwargs", type=str, default=None)
    ap.add_argument("--overlap", type=int, default=1)
    ap.add_argument("--per-file-split-every", type=int, default=16)
    ap.add_argument("--npartitions-per-file", type=int, default=64)
    ap.add_argument("--highest-priority", type=int, default=0)
    return ap

def main(argv=None):
    from dask.distributed import Client
    if argv is None:
        argv = sys.argv[1:]
    d = get_argparser().parse_args(argv)
    with Client(**json.loads(d.dask_kwargs or '{}')) as client:
        tasks = compactify(
            client=client,
            **{k: v for k, v in vars(d).items() if k != 'dask_kwargs'}
        )
        for t in tasks:
            print(t)
      
    
if __name__ == "__main__":
    main()

