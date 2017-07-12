import unittest
from Matrix import *

class TestPersistenceMatrix(unittest.TestCase):

    def test_init(self):
        p = PersistenceMatrix()

    def test_insert_col(self):
        p = PersistenceMatrix()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([0,1])
        p.insert_col([1,3])
        for i in range(6):
            assert(p.red[i] == [i])
        assert(p.inc[4] == [0,1])
        assert(p.inc[5] == [1,3])

    def test_reduce_triangle(self):
        p = PersistenceMatrix()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([1,2])
        p.insert_col([2,3])
        p.insert_col([1,3])
        p.reduce()
        for n in {0,1,2,3,6}:
            assert(not p.inc[n])
        for n in range(5):
            assert(p.red[n] == [n])
        assert(p.red[6] == [4,5,6])
        assert(p.inc[5] == [2,3])
        assert(p.inc[4] == [1,2])
        assert(p.dgm[2] == 4)
        assert(p.dgm[3] == 5)
        for x in ([0,1,6]):
            assert(p.dgm[x] == "inf")
    
    def test_reduce_sphere(self):
        p = PersistenceMatrix()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([0,1])
        p.insert_col([0,1])
        p.insert_col([2,3])
        p.insert_col([2,3])
        p.reduce()
        assert(not p.inc[3])
        assert(not p.inc[5])
        assert(p.red[3] == [2,3])
        assert(p.red[5] == [4,5])
        assert(p.dgm[1] == 2)
        assert(p.dgm[3] == 4)
        assert(p.dgm[0] == "inf")
        assert(p.dgm[5] == "inf")

if __name__ == '__main__':
    unittest.main()
