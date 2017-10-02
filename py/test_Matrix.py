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
        self.assertFalse(m[0])
        self.assertFalse(m[1])
        self.assertEqual(m[2], [0,1])

    def test_add_col(self):
        m = Matrix()
        m.insert_col([1,3,4])
        m.insert_col([1,2,5])
        m.add_col(0,1)
        self.assertEqual(m[0], [1,3,4])
        self.assertEqual(m[1], [2,3,4,5])
        m.add_col(1,0)
        self.assertEqual(m[0], [1,2,5])
        m.add_col(0,1)
        self.assertEqual(m[1], [1,3,4])
        m.insert_col([])
        m.insert_col([])
        m.add_col(2,3)
        self.assertFalse(m[2])
        self.assertFalse(m[3])

    def test_add_row(self):
        m = Matrix()
        m.insert_col([1,2,3])
        m.insert_col([2,3,4])
        m.add_row(1,2)
        self.assertEqual(m[0], [1,3])
        self.assertEqual(m[1], [2,3,4])
        m.add_row(2,3)
        self.assertEqual(m[0], [1,3])
        self.assertEqual(m[1], [2,4])

    def test_swap_col(self):
        m = Matrix()
        m.insert_col([0])
        m.insert_col([1,2])
        m.swap_col(0,1)
        self.assertEqual(m[0], [1,2])
        self.assertEqual(m[1], [0])
        m.insert_col([3,4,5])
        m.swap_col(0,2)
        self.assertEqual(m[0], [3,4,5])
        self.assertEqual(m[2], [1,2])
        self.assertEqual(m[1], [0])

    def test_swap_row(self):
        m = Matrix()
        m.insert_col([0,1,2])
        m.insert_col([2,3,4])
        m.swap_row(3,4)
        self.assertEqual(m[0], [0,1,2])
        self.assertEqual(m[1], [2,3,4])
        m.swap_row(2,3)
        self.assertEqual(m[0], [0,1,3])
        self.assertEqual(m[1], [2,3,4])

if __name__ == '__main__':
    unittest.main()
