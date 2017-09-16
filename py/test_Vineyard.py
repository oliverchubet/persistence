import unittest
from Matrix import *

class TestVineyard(unittest.TestCase):
    def test_switcheroo(self):
       p = Vineyard()
       p.insert_col([])
       p.insert_col([])
       p.insert_col([])
       p.insert_col([0,1])
       p.insert_col([1,2])
       p.switcheroo(3)
       self.assertEqual(p.R[3], [1,2])
       self.assertEqual(p.R[4], [0,1])

       q = Vineyard()
       q.insert_col([])
       q.insert_col([])
       q.insert_col([])
       q.insert_col([0,2])
       q.insert_col([1,2])
       q.insert_col([0,1])
       q.reduce()
       q.switcheroo(4)

    def test_col_row_op(self):
       p = Vineyard()
       p.insert_col([])
       p.insert_col([])
       p.insert_col([])
       p.insert_col([0,1])
       p.insert_col([1,2])
       p.col_row_op(3,4)
       self.assertEqual(p.R[4], [0,2])
       self.assertEqual(p.R[3], [0,1])
       self.assertEqual(p.U[4], [3,4])
       self.assertEqual(p.U[3], [3])

    def test_vineyard_algo_case_1_1_2(self):
        p = Vineyard()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([1,2])
        p.insert_col([0,1])
        p.insert_col([0,2])
        p.reduce()
        p.vineyard_algo(1)
        for i in range(len(p)):
           self.assertLessEqual(max(p.U[i]), i)
        self.assertEqual(p.vineyard, [[1]])
        p.vineyard_algo(1)
        self.assertEqual(p.vineyard, [[1],[1]])

    def test_vineyard_algo_case_2_1_2(self):
        p = Vineyard()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([0,2])
        p.insert_col([1,2])
        p.reduce()
        self.assertEqual(p.U[4], [3,4])
        p.vineyard_algo(3)
        self.assertEqual(p.vineyard, [[3,1,2]])

    def test_vineyard_algo_case_3_1(self):
        p = Vineyard()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([0,1])
        p.insert_col([0,2])
        p.insert_col([1,2])
        p.insert_col([3,4,5])
        p.reduce()
        self.assertEqual(p.U[5], [3,4,5])
        p.vineyard_algo(4)
        self.assertEqual(p.vineyard, [[4,2]])
