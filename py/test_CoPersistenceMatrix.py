import unittest
from Matrix import *

class TestCoPersistenceMatrix(unittest.TestCase):

    def test_init(self):
        p = CoPersistenceMatrix()

    def test_pHrow_triangle(self):
        p = CoPersistenceMatrix()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([1,2])
        p.insert_col([2,3])
        p.insert_col([1,3])
        p.R = p.R.transpose()
        p.pHrow()
        assert(p.dgm[2] == 4)
        assert(p.dgm[3] == 5)

    def test_pHrow_sphere(self):
        p = CoPersistenceMatrix()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([0,1])
        p.insert_col([0,1])
        p.insert_col([2,3])
        p.insert_col([2,3])
        p.R = p.R.transpose()
        p.pHrow()
        assert(p.dgm[1] == 2)
        assert(p.dgm[3] == 4)

    def test_pCoh_triangle(self):
        p = CoPersistenceMatrix()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([0,1])
        p.insert_col([1,2])
        p.insert_col([0,2])
        p.insert_col([3,4,5])
        p.R = p.R.transpose()
        p.pCoh()
        assert(p.dgm[1] == 3)
        assert(p.dgm[2] == 4)
        assert(p.dgm[5] == 6)

if __name__ == '__main__':
    unittest.main()

