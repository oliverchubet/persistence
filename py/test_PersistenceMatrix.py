import unittest
from Matrix import *
import dionysus as d
import math

class PersistenceMatrixTestCase(unittest.TestCase):
    matrix_class = PersistenceMatrix

    def test_init(self):
        self.matrix_class()

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

    @classmethod
    def setup_different_triangle(self):
        p = self.matrix_class()
        p.insert([], [], [], [0,1], [1,2], [0,2], [3,4,5])
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

class TestAnnotationsMatrix(PersistenceMatrixTestCase):

    matrix_class = AnnotationMatrix

    def reduced_triangle_assertions(self, p):
        self.assertEqual(p.dgm[2], 4)
        self.assertEqual(p.dgm[3], 5)

    def reduced_sphere_assertions(self, p):
        self.assertEqual(p.dgm[1], 2)
        self.assertEqual(p.dgm[3], 4)

    def test_annotations_triangle(self):
        p = self.setup_different_triangle()
        p.reduce()
        self.assertEqual(p.dgm[1], 3)
        self.assertEqual(p.dgm[2], 4)
        self.assertEqual(p.dgm[5], 6)

    def test_annotations_sphere(self):
        p = self.setup_sphere()
        p.reduce()
        self.assertEqual(p.dgm[1], 2)
        self.assertEqual(p.dgm[3], 4)

class ZigZagPersistenceTestCase(PersistenceMatrixTestCase):

    matrix_class = ZigZagPersistenceMatrix

    def test_zigzag_reduce_triangle_sequence(self):
        p = ZigZagPersistenceMatrix()
        p.insert([],[],[],[0,1],[0,2],[1,2],[3,4,5])
        order = [0,1,2,3,4,5,6,6,5,4,3,2,1,0]
        arrows = [1,1,1,1,1,1,1,0,0,0,0,0,0,0]
        p.zigzag_reduce(order, arrows)
        self.assertEqual(p.dgm[0], 12)
        self.assertEqual(p.dgm[1], 2)
        self.assertEqual(p.dgm[10], 11)
        self.assertEqual(p.dgm[2], 3)
        self.assertEqual(p.dgm[9], 10)
        self.assertEqual(p.dgm[5], 5)
        self.assertEqual(p.dgm[7], 7)

    def test_zigzag_reduce_segment_sequence(self):
        p = ZigZagPersistenceMatrix()
        p.insert([],[],[0,1])
        order = [0,1,2,2,1,0]
        arrows = [1,1,1,0,0,0]
        p.zigzag_reduce(order, arrows)
        self.assertEqual(p.dgm[1], 1)
        self.assertEqual(p.dgm[3], 3)
        self.assertEqual(p.dgm[0], 4)

    def test_zigzag_reduce_segment(self):
        p = ZigZagPersistenceMatrix()
        p.insert([],[],[0,1])
        order = [0,1,2,2,2]
        arrows = [1,1,1,0,1]
        p.zigzag_reduce(order, arrows)
        self.assertEqual(p.dgm[1], 1)
        self.assertEqual(p.dgm[3], 3)
        self.assertEqual(p.dgm[0], 4)

    def test_compare_to_dionysus(self):
        p = ZigZagPersistenceMatrix()
        p.insert([],[],[],[0,1],[0,2],[1,2],[3,4,5],[])
        order = [0,1,2,3,4,5,6,6,5,4,3,2,1,0,7]
        arrows = [1,1,1,1,1,1,1,0,0,0,0,0,0,0,1]
        p.zigzag_reduce(order, arrows)
        f = d.Filtration([[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2],[3]])
        times = [[0,13],[1,12],[2,11],[3,10],[4,9],[5,8],[6,7],[14]]
        zz, dgms = d.zigzag_homology_persistence(f, times)
        for i in dgms[0]:
            if i.death == math.inf:
                self.assertEqual(len(arrows), p.dgm[i.birth]+1)
            else:
                self.assertEqual(i.death, p.dgm[i.birth]+1)

    @staticmethod
    def get_vertices(p, col):
        if not p.R[col]:
            return [col]
        to_check = set(p.R[col])
        vertices = []
        while to_check:
            s = to_check.pop()
            if p.R[s]:
                to_check.update(set(p.R[s]))
            else:
                vertices.append(s)
        return vertices

    def test_get_vertices(self):
        p = ZigZagPersistenceMatrix()
        p.insert([],[],[],[0,1],[0,2],[1,2],[3,4,5],[])
        vertices = self.get_vertices(p, 6)
        self.assertEqual(vertices, [0,1,2])
        vertices = self.get_vertices(p,0)
        self.assertEqual(vertices, [0])
        vertices = self.get_vertices(p,3)
        self.assertEqual(vertices, [0,1])
        
    def convert_to_dionysus(self, p, order):
        f = []
        times = []
        for i in range(len(p.R)):
            f.append(self.get_vertices(p,i))
            times.append([])
        for i,s in enumerate(order):
            times[s].append(i)
        zz, dgms = d.zigzag_homology_persistence(d.Filtration(f), times)
        return dgms

    def test_convert_to_dionysus(self):
        p = ZigZagPersistenceMatrix()
        p.insert([],[],[],[0,1],[0,2],[1,2],[3,4,5],[])
        order = [0,1,2,3,4,5,6,6,5,4,3,2,1,0,7]
        arrows = [1,1,1,1,1,1,1,0,0,0,0,0,0,0,1]
        p.zigzag_reduce(order, arrows)
        dgms = self.convert_to_dionysus(p,order)
        for i in dgms[0]:
            if i.death == math.inf:
                self.assertEqual(len(arrows), p.dgm[i.birth]+1)
            else:
                self.assertEqual(i.death, p.dgm[i.birth]+1)

    def arbitrary_zigzag_assertions(self, p, order, arrows):
        p.zigzag_reduce(order, arrows)
        dgms = self.convert_to_dionysus(p,order)
        for j in dgms:
            for i in j:
                if i.death == math.inf:
                    self.assertEqual(len(arrows), p.dgm[i.birth]+1)
                else:
                    self.assertEqual(i.death, p.dgm[i.birth]+1)
                p.dgm.pop(i.birth)
        assert(not p.dgm)

    def test_zigzags_0(self):
        p = ZigZagPersistenceMatrix()
        p.insert([],[],[],[],[0,1],[0,2],[0,3],[1,2],[1,3],[2,3])
        order =  [0,1,2,2,1,1,2,3,4,3,5,3,6,7,6,8,9,8]
        arrows = [1,1,1,0,0,1,1,1,1,0,1,1,1,1,0,1,1,0]
        self.arbitrary_zigzag_assertions(p,order,arrows)

    def test_zigzags_1(self):
        p = ZigZagPersistenceMatrix()
        p.insert([],[],[],[],[0,1],[0,2],[0,3],[1,2],[1,3],[2,3])
        order = [0,0,1,1,0,1,2,2,1,1,2,3,4,5,6]
        arrows= [1,0,1,0,1,1,1,0,0,1,1,1,1,1,1]
        self.arbitrary_zigzag_assertions(p,order,arrows)

    def test_zigzags_2(self):
        p = ZigZagPersistenceMatrix()
        p.insert([],[],[],[],[0,1],[0,2],[0,3],[1,2],[1,3],[2,3])
        order = [0,1,2,4,5,7,5]
        arrows = [1,1,1,1,1,1,0]
        self.arbitrary_zigzag_assertions(p,order,arrows)

#if __name__ == '__main__':
#    unittest.main()
