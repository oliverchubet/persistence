import unittest
from UnionFind import *
import string

class TestUnionFind(unittest.TestCase):

    def test_union_find(self):
        uf = UnionFind([0,1,2,3,4,5])
        self.assertFalse(uf.find(0,1))
        self.assertFalse(uf.find(3,5))
        self.assertTrue(uf.find(0,0))
        uf.union(0,1)
        uf.union(3,4)
        self.assertFalse(uf.find(1,3))
        self.assertTrue(uf.find(0,1))
        self.assertTrue(uf.find(3,4))

    def test_for_weird_bugs(self):
        uf = UnionFind(string.ascii_lowercase)
        uf.union("a", "b")
        self.assertTrue(uf.find("a", "b"))
        self.assertTrue(uf.find("b", "a"))
        self.assertFalse(uf.find("z", "y"))

        self.assertTrue(uf.find(chr(ord("a")), chr(ord("a") + 1)))
        self.assertTrue(uf.find(chr(ord("a") + 1), chr(ord("a"))))

        with self.assertRaises(Exception):
            uf.find("A", "b")
