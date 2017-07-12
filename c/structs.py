from ctypes import *
from frechet.complex import *
from frechet.persistence import *

md = cdll.LoadLibrary('/home/shpew12/git/sheehy_is_2017/c/libtest.so')

null_ptr = POINTER(c_int)()

class MATRIX(Structure):
    _fields_ = [("values", POINTER(c_int)),
            ("used", c_size_t),
            ("size", c_size_t)]

    def __iter__(self):
        v = self.values
        for j in range(self.used):
            yield ''.join(str(md.bit(v[j],self.used-i-1)) for i in range(self.used))

    def to_sc(self):
        v = self.vertices_matrix()
        return SimplicialComplex(*(
            set(j for j in range(len(i)) if i[self.used-j-1] == '1')
            for i in v))

    def __init__(self):
        md.init_matrix(pointer(self))

    def copy(self):
        copy = MATRIX()
        md.copy(pointer(self),pointer(copy))
        return copy

    def print(self):
        md.bv_print(pointer(self))

    def insert_col(self, value):
        md.insert_col(pointer(self), value)

    def in_matrix(self, value):
        return md.in_matrix(pointer(self), value)

    def add_col(self, i, j):
        md.add_col(pointer(self),i,j)

    def set_col(self, col, value):
        md.set_col(pointer(self), col, value)

    def add_row(self, i, j):
        md.add_row(pointer(self),i,j)

    def free(self):
        md.free_matrix(pointer(self))

    def lowest(self, col):
        return md.lowest(pointer(self), col)

    def inv_matrix(self):
        inv = MATRIX()
        md.inv_matrix(pointer(self),pointer(inv))
        return inv

    def simple_mult(m1, m2):
        res = MATRIX()
        md.simple_mult(pointer(m1),pointer(m2),pointer(res))
        return res

    def switch_ij(self, i, j):
        md.switch_ij(pointer(self),i,j)

    def vertices_matrix(self):
        v = MATRIX()
        md.vertices_matrix(pointer(self),pointer(v))
        return v

class PERSISTENCE(Structure):
    _fields_ = [("inc", POINTER(MATRIX)),
            ("red", POINTER(MATRIX))]

    def __init__(self,inc,red):
        md.init_persistence(pointer(self),pointer(inc),pointer(red))

    def free(self):
        md.free_persistence(pointer(self))

    def insert_simplex(self, sim):
        md.insert_simplex(pointer(self),sim)

    def set_simplex(self, index, sim):
        md.set_simplex(pointer(self),index,sim)

    def reduce(self):
        md.reduce(pointer(self))

    def vineyard(self, i):
        md.vineyard(pointer(self),i)

    def print(self):
        md.printp(pointer(self))

    def birth_death(self):
        md.birth_death(pointer(self))

