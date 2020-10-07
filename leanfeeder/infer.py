
import sys
import time
import csv
import strconv

def typemax(a,b):
    types = [int,float,str]
    try:
        ai,bi = (types.index(v) for v in (a,b))
    except ValueError:
        return b
    else:
        return types[max(ai,bi)]

def pgtype(pytype,intmax):
    if pytype is str:
        return "text"
    elif pytype is int:
        if intmax < 32767:
            return "smallint"
        elif intmax >= 32767 and intmax <= 2147483647:
            return "integer"
        else:
            return "bigint"
    elif pytype is float:
        return "double precision"

def inferPgTypes(iterable):
    converter = strconv.Strconv(
            converters = [(t,strconv.get_converter(t)) for t in ("int","float")]
        )
    def convert_none(s):
        if s in (""):
            return
        else:
            raise ValueError
    converter.register_converter("none",convert_none, priority = 0)

    mat = converter.convert_matrix(iterable)
    mat = [*mat]

    rowlength = len(mat[0])

    maxima = [0 for _ in range(rowlength)]
    types = [int for _ in range(rowlength)]

    for r in mat:
        for idx,v in enumerate(r):
            try:
                maxima[idx] = max(v,maxima[idx])
            except TypeError:
                pass
            types[idx] = typemax(type(v),types[idx])

    pgtypes = ["" for _ in range(rowlength)]

    for idx,info in enumerate(zip(types,maxima)):
        t,m = info
        pgtypes[idx] = pgtype(t,m)

    return pgtypes

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        r = csv.reader(f)
        header = next(r)
        types = inferPgTypes(r)
        print(types)

