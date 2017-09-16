import unittest
from Matrix import *
from test_PersistenceMatrix import PersistenceMatrixTestCase

class TestCoPersistenceMatrix(PersistenceMatrixTestCase):

    matrix_class = CoPersistenceMatrix

    def test_pHrow_triangle(self):
        p = self.setup_triangle()
        p.R = p.R.transpose()
        p.pHrow()
        self.assertEqual(p.dgm[2], 4)
        self.assertEqual(p.dgm[3], 5)

    def test_pHrow_sphere(self):
        p = self.setup_sphere()
        p.R = p.R.transpose()
        p.pHrow()
        self.assertEqual(p.dgm[1], 2)
        self.assertEqual(p.dgm[3], 4)

    def setup_different_triangle(self):
        p = self.matrix_class()
        p.insert([], [], [], [0,1], [1,2], [0,2], [3,4,5])
        return p

    def test_pCoh_triangle(self):
        p = self.setup_different_triangle()
        p.R = p.R.transpose()
        p.pCoh()
        self.assertEqual(p.dgm[1], 3)
        self.assertEqual(p.dgm[2], 4)
        self.assertEqual(p.dgm[5], 6)

    def test_annotations_triangle(self):
        p = self.setup_different_triangle()
        p.annotations()
        self.assertEqual(p.dgm[1], 3)
        self.assertEqual(p.dgm[2], 4)
        self.assertEqual(p.dgm[5], 6)

    def test_annotations_sphere(self):
        p = self.setup_sphere()
        p.annotations()
        self.assertEqual(p.dgm[1], 2)
        self.assertEqual(p.dgm[3], 4)

if __name__ == '__main__':
    unittest.main()

