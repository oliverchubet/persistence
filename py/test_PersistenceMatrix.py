import unittest
from Matrix import *


def setup_triangle():
    p = PersistenceMatrix()
    p.insert_col([])
    p.insert_col([])
    p.insert_col([])
    p.insert_col([])
    p.insert_col([1,2])
    p.insert_col([2,3])
    p.insert_col([1,3])
    return p

def setup_sphere():
    p = PersistenceMatrix()
    p.insert_col([])
    p.insert_col([])
    p.insert_col([0,1])
    p.insert_col([0,1])
    p.insert_col([2,3])
    p.insert_col([2,3])
    return p

def reduced_triangle_assertions(p):
    for n in {0,1,2,3,6}:
        assert(not p.R[n])
    for n in range(5):
        assert(p.U[n] == [n])
    assert(p.U[6] == [4,5,6])
    assert(max(p.R[5]) == 3)
    assert(max(p.R[4]) == 2)
    assert(p.dgm[2] == 4)
    assert(p.dgm[3] == 5)

def reduced_sphere_assertions(p):
        assert(not p.R[3])
        assert(not p.R[5])
        assert(p.U[3] == [2,3])
        assert(p.U[5] == [4,5])
        assert(p.dgm[1] == 2)
        assert(p.dgm[3] == 4)

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
            assert(p.U[i] == [i])
        assert(p.R[4] == [0,1])
        assert(p.R[5] == [1,3])

    def test_reduce_triangle(self):
        p = setup_triangle()
        p.reduce()
        reduced_triangle_assertions(p)

    def test_reduce_sphere(self):
        p = setup_sphere()
        p.reduce()
        reduced_sphere_assertions(p)

    def test_future_reduce_triangle(self):
        p = setup_triangle() 
        p.future_reduce()
        reduced_triangle_assertions(p)

    def test_future_reduce_sphere(self):
        p = setup_sphere() 
        p.future_reduce()
        reduced_sphere_assertions(p)

    def test_iso_reordering(self):
        p = setup_triangle()
        p.iso_reordering()

if __name__ == '__main__':
    unittest.main()
