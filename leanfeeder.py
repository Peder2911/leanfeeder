
import csv
import os
import sys
from io import StringIO

from contextlib import closing

import psycopg2
from psycopg2 import errorcodes
import fire

from infer import inferPgTypes 

def inferSchema(file):
    reader = csv.reader(file)
    header = next(reader)
    pgt = inferPgTypes(reader)
    return ", ".join([f"{name} {type}" for name,type in zip(header,pgt)])

def main(uri,data,name = None,drop=True):
    if name is None:
        dataname = os.path.splitext(os.path.split(data)[-1])[0]
    else:
        dataname = name

    with closing(psycopg2.connect(uri)) as con:
        c = con.cursor()
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name=%s)",(dataname,))
        exists = c.fetchone()[0]

        with open(data) as f:
            """
            Copy everything into a buffer to avoid repeated reads.
            (necessary, because detailed type inference requires
            needs the whole data set in memory, for data too big to
            fit in memory, add data in chunks).
            """
            sio = StringIO(f.read())

        if drop and exists:
            print(f"Dropping existing table {dataname}")
            c.execute(f"DROP TABLE IF EXISTS {dataname}")
            exists = False

        if not exists:
            print(f"Creating table {dataname}")
            sio.seek(0)
            schema = inferSchema(sio)
            c.execute(f"CREATE TABLE {dataname} ({schema})")
        else:
            print(f"Appending to {dataname}")

        sio.seek(0)
        next(sio)
        c.copy_from(sio,dataname,sep=",",null = "")

        con.commit()

if __name__ == "__main__":
    fire.Fire(main)
