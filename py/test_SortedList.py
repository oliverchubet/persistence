import unittest
from SortedList import *

class TestSortedList(unittest.TestCase):
    
    def test_init(self):
        s = SortedList()
        p = SortedList([9,7,8])
        self.assertEqual(p, [7,8,9])

    def test_add(self):
        s = SortedList()
        for i in range(10):
            s.add(i + (-1)**i)
        self.assertEqual(s, [0,1,2,3,4,5,6,7,8,9])
        s = SortedList()
        self.assertFalse(s)
        for i in {2,5,8,0,1,3}:
            s.add(i)
        self.assertEqual(s, [0,1,2,3,5,8])

    def test_remove(self):
        s = SortedList()
        for i in range(10):
            s.add(i + (-1)**i)
        for i in range(10):
            s.remove(i)
        self.assertFalse(s)

    def test_getitem(self):
        s = SortedList()
        for i in {1,3,5,7,9}:
            s.add(i)
        for i in range(5):
            self.assertEqual(s[i], 2*i+1)

    def test_contains(self):
        s = SortedList()
        for i in {2,4,6,7,8,9}:
            s.add(i)
        for i in {2,4,6,7,8,9}:
            self.assertIn(i, s)

    def test_len(self):
        s = SortedList()
        for i in range(20):
            s.add(i)
        self.assertEqual(len(s), 20)
        s.remove(4)
        self.assertEqual(len(s), 19)

    def test_max(self):
        s = SortedList()
        for i in {3,4,2,6,8}:
            s.add(i)
        self.assertEqual(max(s), 8)
        s.add(100)
        self.assertEqual(max(s), 100)

    def test_min(self):
        s = SortedList()
        for i in {1,3,4,7,2,4,8}:
            s.add(i)
        self.assertEqual(min(s), 1)
        s.add(0)
        self.assertEqual(min(s), 0)

    def test_eq(self):
        s = SortedList([2,4,5,1])
        q = SortedList([1,2,4,5])
        self.assertEqual(s, [1,2,4,5])
        self.assertEqual(s, q)

    def test_sub(self):
        s = SortedList([1,4,5])
        o = SortedList([9,8,7])
        s - o
        self.assertEqual(s, [1,4,5,7,8,9])
        self.assertEqual(o, [7,8,9])
        p = SortedList([1,2,4,5])
        s - p
        self.assertEqual(s, [2,7,8,9])
        self.assertEqual(p, [1,2,4,5])
