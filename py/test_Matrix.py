import unittest
from Matrix import *
from SortedList import *

class TestMatrix(unittest.TestCase):
    def test_init(self):
        m = Matrix()

    def test_insert_col(self):
        m = Matrix()
        m.insert_col([])
        m.insert_col([])
        m.insert_col([0,1])
        assert(not m[0])
        assert(not m[1])
        assert(m[2] == [0,1])

    def test_add_col(self):
        m = Matrix()
        m.insert_col([1,3,4])
        m.insert_col([1,2,5])
        m.add_col(0,1)
        assert(m[0] == [1,3,4])
        assert(m[1] == [2,3,4,5])
        m.add_col(1,0)
        assert(m[0] == [1,2,5])
        m.add_col(0,1)
        assert(m[1] == [1,3,4])
        m.insert_col([])
        m.insert_col([])
        m.add_col(2,3)
        assert(not m[2])
        assert(not m[3])

    def test_add_row(self):
        m = Matrix()
        m.insert_col([1,2,3])
        m.insert_col([2,3,4])
        m.add_row(1,2)
        assert(m[0] == [1,3])
        assert(m[1] == [2,3,4])
        m.add_row(2,3)
        assert(m[0] == [1,3])
        assert(m[1] == [2,4])

    def test_swap_col(self):
        m = Matrix()
        m.insert_col([0])
        m.insert_col([1,2])
        m.swap_col(0,1)
        assert(m[0] == [1,2])
        assert(m[1] == [0])
        m.insert_col([3,4,5])
        m.swap_col(0,2)
        assert(m[0] == [3,4,5])
        assert(m[2] == [1,2])
        assert(m[1] == [0])

    def test_swap_row(self):
        m = Matrix()
        m.insert_col([0,1,2])
        m.insert_col([2,3,4])
        m.swap_row(3,4)
        assert(m[0] == [0,1,2])
        assert(m[1] == [2,3,4])
        m.swap_row(2,3)
        assert(m[0] == [0,1,3])
        assert(m[1] == [2,3,4])

    def test_reduce(self):
        m = Matrix()
        m.insert_col([])
        m.insert_col([])
        m.insert_col([])
        m.insert_col([0,1])
        m.insert_col([1,2])
        m.insert_col([0,2])
        m.reduce()
        assert(not m[0])
        assert(not m[1])
        assert(not m[2]) 
        assert(m[3] == [0,1])
        assert(m[4] == [1,2])
        assert(not m[5])
        

if __name__ == '__main__':
    unittest.main()
