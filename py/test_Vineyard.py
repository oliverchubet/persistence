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

    def test_vineyard_algo(self): 
        v = Vineyard()
        v.insert([],[],[],[0,1],[0,2],[1,2],[3,4,5])
        v.reduce()
        v.vineyard_algo(4)
        w = Vineyard()
        w.insert([],[],[],[0,1],[1,2],[0,2],[3,4,5])
        w.reduce()
        w.update_dgm()
        self.assertEqual(w.dgm, v.dgm)
        v.vineyard_algo(2)
        w = Vineyard()
        w.insert([],[],[0,1],[],[1,3],[0,3],[2,4,5])
        w.reduce()
        w.update_dgm()
        self.assertEqual(w.dgm, v.dgm)
        y = Vineyard()
        y.insert([],[],[0,1],[],[1,3],[0,3],[2,4,5])
        y.reduce()
        for i in [0,2,4]: # all other swaps would break the filtration
            self.assertEqual(w.R, y.R)
            y.vineyard_algo(i)
            y.vineyard_algo(i)
            self.assertEqual(w.dgm, y.dgm)
        w = Vineyard()
        w.insert([],[],[0,1],[],[0,3],[1,3],[2,4,5])
        w.reduce()
        w.update_dgm()
        y.vineyard_algo(4)
        self.assertEqual(w.dgm, v.dgm)

    def test_vineyard_algo_2(self):
        w = Vineyard()
        w.insert([],[],[],[0,1],[1,2],[0,2],[3,4,5])
        w.reduce()
        w.update_dgm()
        y = Vineyard()
        y.insert([],[],[],[0,1],[1,2],[0,2],[3,4,5])
        y.reduce()
        for i in range(5): 
            y.vineyard_algo(i)
            y.vineyard_algo(i)
            self.assertEqual(w.dgm, y.dgm)

    def test_vineyard_algo_3(self):
        w = Vineyard()
        w.insert([],[],[],[0,2],[1,2],[0,1],[3,4,5])
        w.reduce()
        w.update_dgm()
        y = Vineyard()
        y.insert([],[],[],[0,2],[1,2],[0,1],[3,4,5])
        y.reduce()
        for i in range(5): 
            y.vineyard_algo(i)
            y.vineyard_algo(i)
            self.assertEqual(w.dgm, y.dgm)


    def test_vineyard_list(self):
        w = Vineyard()
        w.insert([],[],[],[0,2],[1,2],[0,1],[3,4,5])
        w.reduce()
        w.vineyard_list(0,0,0,1,1,1)
        w.vineyard_list(3,4,4,3)

     
