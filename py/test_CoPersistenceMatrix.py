import unittest
from Matrix import *

class TestCoPersistenceMatrix(unittest.TestCase):

    def test_init(self):
        p = CoPersistenceMatrix()

    def test_insert_col(self):
        p = CoPersistenceMatrix()
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
        assert(p.lowR[1] == [4])
        assert(p.lowR[3] == [5])

    def test_pHrow_triangle(self):
        p = CoPersistenceMatrix()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([1,2])
        p.insert_col([2,3])
        p.insert_col([1,3])
        p.pHrow()
        for n in {0,1,2,3,6}:
            assert(not p.inc[n])
        for n in range(5):
            assert(p.red[n] == [n])
        assert(p.red[6] == [4,5,6])
        assert(p.inc[5] == [2,3])
        assert(p.inc[4] == [1,2])
        #assert(p.dgm[2] == 4)
        #assert(p.dgm[3] == 5)
        for x in ([0,1,6]):
            #assert(p.dgm[x] == "inf")
            break

    def test_pHrow_sphere(self):
        p = CoPersistenceMatrix()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([0,1])
        p.insert_col([0,1])
        p.insert_col([2,3])
        p.insert_col([2,3])
        p.pHrow()
        assert(not p.inc[3])
        assert(not p.inc[5])
        assert(p.red[3] == [2,3])
        assert(p.red[5] == [4,5])
        #assert(p.dgm[1] == 2)
        #assert(p.dgm[3] == 4)
        #assert(p.dgm[0] == "inf")
        #assert(p.dgm[5] == "inf")

    def test_pCoh_triangle(self):
        p = CoPersistenceMatrix()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([0,1])
        p.insert_col([1,2])
        p.insert_col([0,2])
        p.insert_col([3,4,5])
        p.inc = p.inc.transpose()
        p.pCoh()
        assert(p.dgm[1] == 3)
        assert(p.dgm[2] == 4)
        assert(p.dgm[5] == 6)

if __name__ == '__main__':
    unittest.main()

