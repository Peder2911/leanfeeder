
import csv
import os
import sys

from contextlib import closing

import psycopg2
from psycopg2 import errorcodes
import fire

from infer import inferPgTypes 

def inferSchema(fname):
    with open(fname) as f:
        reader = csv.reader(f)
        header = next(reader)
        pgt = inferPgTypes(reader)
    return ", ".join([f"{name} {type}" for name,type in zip(header,pgt)])

def main(uri,data,drop=True):
    dataname = os.path.splitext(os.path.split(data)[-1])[0]

    with closing(psycopg2.connect(uri)) as con:
        c = con.cursor()
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name=%s)",(dataname,))
        exists = c.fetchone()[0]

        if drop and exists:
            print(f"Dropping existing table {dataname}")
            c.execute(f"DROP TABLE IF EXISTS {dataname}")
            exists = False

        if not exists:
            print(f"Creating table {dataname}")
            schema = inferSchema(data)
            c.execute(f"CREATE TABLE {dataname} ({schema})")
        else:
            print(f"Appending to {dataname}")

        with open(data) as f:
            next(f)
            c.copy_from(f,dataname,sep=",",null = "")

        con.commit()

if __name__ == "__main__":
    fire.Fire(main)
