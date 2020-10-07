
import unittest

from infer import typemax, pgtype, inferPgTypes 

class TestOps(unittest.TestCase):
    def test_pg(self):
        self.assertEqual(pgtype(int,10), "smallint")
        self.assertEqual(pgtype(int,1000000), "integer")
        self.assertEqual(pgtype(int,10000000000), "bigint")
        self.assertEqual(pgtype(str,0), "text")
        self.assertEqual(pgtype(float,1.0), "double precision")
    def test_tm(self):
        self.assertIs(typemax(int,str),str)
        self.assertIs(typemax(str,int),str)
        self.assertIs(typemax(int,float),float)
        self.assertIs(typemax(float,int),float)
        self.assertIs(typemax(int,int),int)
        self.assertIs(typemax(None,int),int)
    def test_inferral(self):
        pgt = inferPgTypes([
                ("1","","1"),
                ("2","1","2"),
                ("3","","3")
            ])
        self.assertEqual(pgt,["smallint","smallint","smallint"])

        pgt = inferPgTypes([
                ("1.1","1","1000000"),
                ("2.2","a","2"),
                ("3.3","3","3")
            ])
        self.assertEqual(pgt,["double precision","text","integer"])
