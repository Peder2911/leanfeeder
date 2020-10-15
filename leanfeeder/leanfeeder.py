
import csv
import os
import sys
from io import StringIO

from contextlib import closing

import psycopg2
from psycopg2 import errorcodes
import fire

from leanfeeder.infer import inferPgTypes 

def inferSchema(file):
    reader = csv.reader(file)
    header = next(reader)
    pgt = inferPgTypes(reader)
    return ", ".join([f"{name} {type}" for name,type in zip(header,pgt)])

def push(c,fobj,dataname = "data",drop=True):
    try:
        con = psycopg2.connect(c)
    except TypeError:
        con = c

    c = con.cursor()
    c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name=%s)",(dataname,))
    exists = c.fetchone()[0]
    sio = StringIO(fobj.read())

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
