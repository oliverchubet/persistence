import unittest
from UnionFind import *

class TestUnionFind(unittest.TestCase):
    
    def test_union_find(self):
        uf = UnionFind([0,1,2,3,4,5])
        assert(not uf.find(0,1))
        assert(not uf.find(3,5))
        assert(uf.find(0,0))
        uf.union(0,1)
        uf.union(3,4)
        assert(not uf.find(1,3))
        assert(uf.find(0,1))
        assert(uf.find(3,4))

