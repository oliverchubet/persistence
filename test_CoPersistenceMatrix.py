import unittest
from Matrix import *
from test_PersistenceMatrix import PersistenceMatrixTestCase

class TestCoPersistenceMatrix(PersistenceMatrixTestCase):

    matrix_class = CoPersistenceMatrix

    def reduced_triangle_assertions(self, p):
        self.assertEqual(p.dgm[2], 4)
        self.assertEqual(p.dgm[3], 5)

    def reduced_sphere_assertions(self, p):
        self.assertEqual(p.dgm[1], 2)
        self.assertEqual(p.dgm[3], 4)

    def reduced_line_assertions(self, p):
        self.assertEqual(p.dgm[1], 2)
        self.assertEqual(p.dgm[3], 4)
        self.assertEqual(p.dgm[5], 6)
        self.assertEqual(p.dgm[7], 8)
        self.assertEqual(p.dgm[9], 10)
        self.assertFalse(p.dgm[11])
        self.assertFalse(p.dgm[0])

    def test_reduce_triangle(self):
        p = self.setup_triangle()
        p.R = p.R.transpose()
        p.reduce()
        self.reduced_triangle_assertions(p)

    def test_reduce_sphere(self):
        p = self.setup_sphere()
        p.R = p.R.transpose()
        p.reduce()
        self.reduced_sphere_assertions(p)

    def test_pHrow_triangle(self):
        p = self.setup_triangle()
        p.R = p.R.transpose()
        p.reduce()
        self.assertEqual(p.dgm[2], 4)
        self.assertEqual(p.dgm[3], 5)

    def test_pHrow_sphere(self):
        p = self.setup_sphere()
        p.R = p.R.transpose()
        p.reduce()
        self.assertEqual(p.dgm[1], 2)
        self.assertEqual(p.dgm[3], 4)

class TestpCohCoPersistenceMatrix(TestCoPersistenceMatrix):

    matrix_class = pCohCoPersistenceMatrix

    def test_pCoh_triangle(self):
        p = self.setup_different_triangle()
        p.R = p.R.transpose()
        p.reduce()
        self.assertEqual(p.dgm[1], 3)
        self.assertEqual(p.dgm[2], 4)
        self.assertEqual(p.dgm[5], 6)

if __name__ == '__main__':
    unittest.main()

