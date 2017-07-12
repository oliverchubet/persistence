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
       assert(p.inc[3] == [1,2])
       assert(p.inc[4] == [0,1])

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
       assert(p.inc[4] == [0,2])
       assert(p.inc[3] == [0,1])
       assert(p.red[4] == [3,4])
       assert(p.red[3] == [3])

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
           assert(max(p.red[i]) <= i)
        assert(p.vineyard == [[1]])
        p.vineyard_algo(1)
        assert(p.vineyard == [[1],[1]])

    def test_vineyard_algo_case_2_1_2(self):
        p = Vineyard()
        p.insert_col([])
        p.insert_col([])
        p.insert_col([])
        p.insert_col([0,2])
        p.insert_col([1,2])
        p.reduce()
        assert(p.red[4] == [3,4])
        p.vineyard_algo(3)
        assert(p.vineyard == [[3,1,2]])

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
        assert(p.red[5] == [3,4,5])
        p.vineyard_algo(4)
        assert(p.vineyard == [[4,2]])
