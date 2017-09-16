import unittest
from Matrix import *

class PersistenceMatrixTestCase(unittest.TestCase):
    matrix_class = PersistenceMatrix

    def test_init(self):
        p = self.matrix_class()

    def reduced_triangle_assertions(self, p):
        for n in {0,1,2,3,6}:
            self.assertFalse(p.R[n])
        for n in range(5):
            self.assertEqual(p.U[n], [n])
        self.assertEqual(p.U[6], [4,5,6])
        self.assertEqual(max(p.R[5]), 3)
        self.assertEqual(max(p.R[4]), 2)
        self.assertEqual(p.dgm[2], 4)
        self.assertEqual(p.dgm[3], 5)

    def reduced_sphere_assertions(self, p):
        self.assertFalse(p.R[3])
        self.assertFalse(p.R[5])
        self.assertEqual(p.U[3], [2,3])
        self.assertEqual(p.U[5], [4,5])
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

    @classmethod
    def setup_triangle(cls):
        p = cls.matrix_class()
        p.insert([], [], [], [], [1,2], [2,3], [1,3])
        return p

    @classmethod
    def setup_sphere(cls):
        p = cls.matrix_class()
        p.insert([], [], [0,1], [0,1], [2,3], [2,3])
        return p

    @classmethod
    def setup_line(cls):
        p = cls.matrix_class()
        p.insert([], [], [0,1], [],
                 [3,1], [], [5,3], [],
                 [7,5], [], [9,7], [])
        return p

    def test_insert_col(self):
        p = self.matrix_class()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([0,1])
        p.insert_col([1,3])
        for i in range(6):
            self.assertEqual(p.U[i], [i])
        self.assertEqual(p.R[4], [0,1])
        self.assertEqual(p.R[5], [1,3])

    def test_reduce_triangle(self):
        p = self.setup_triangle()
        p.reduce()
        self.reduced_triangle_assertions(p)

    def test_reduce_sphere(self):
        p = self.setup_sphere()
        p.reduce()
        self.reduced_sphere_assertions(p)

    @unittest.skip("test not implemented")
    def test_iso_reordering(self):
        p = self.setup_triangle()
        p.iso_reordering()
        raise NotImplementedError()  # need to test something

class SpectralPersistenceMatrixTestCase(PersistenceMatrixTestCase):
    matrix_class = SpectralPersistenceMatrix

class FuturePersistenceMatrixTestCase(PersistenceMatrixTestCase):
    matrix_class = FuturePersistenceMatrix

if __name__ == '__main__':
    unittest.main()
