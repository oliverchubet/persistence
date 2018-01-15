#/usr/bin/env python3

from SortedList import *
from UnionFind import *
#from PIL import Image, ImageDraw, ImageColor
import random as r

class Matrix(list):
    def insert_col(self, col):
        self.append(SortedList(col))

    def add_col(self, i, j):
        self[j] = self[i] ^ self[j]

    def add_row(self, i, j):
        for x in self:
            if i in x:
                x.remove(j) if j in x else x.add(j)

    def swap_col(self, i, j):
        self[i], self[j] = self[j], self[i]

    def swap_row(self, i, j):
        self.add_row(i,j)
        self.add_row(j,i)
        self.add_row(i,j)

    def transpose(self):
        T = Matrix()
        for i in range(len(self)):
            L = SortedList()
            for j in range(len(self)):
                if i in self[j]:
                    L.add(j)
            T.insert_col(L)
        return T

class PersistenceMatrix:

    def __init__(self):
        self.R = Matrix() # incidence matrix
        self.U = Matrix() # reducing matrix
        self.dgm = {}       # persistence diagram (birth:death)

    def __len__(self):
        return len(self.R)

    def insert(self, *columns):
        for col in columns:
            self.insert_col(col)

    def insert_col(self, col):
        col = SortedList(col)
        self.R.append(col)
        self.U.append(SortedList([len(self)-1]))

    def reduce(self): # original persistence algo
        for i in range(len(self)):
            while self.R[i]:
                j = max(self.R[i])
                if j in self.dgm:
                    self.R.add_col(self.dgm[j],i)
                    self.U.add_col(self.dgm[j],i)
                else:
                    self.dgm[j] = i
                    break

    def get_vertices(self, col):
        if not self.R[col]:
            return [col]
        to_check = set(self.R[col])
        vertices = []
        while to_check:
            s = to_check.pop()
            if self.R[s]:
                to_check.update(set(self.R[s]))
            else:
                vertices.append(s)
        return vertices

    def to_svg(self):
        xsize = 500
        ysize = 200 
        point_radius = 4
        stroke_width = 2
        poly_opacity = .25
        line_opacity = .75
        f = open("test.svg", "w")
        f.write(''.join(["<svg width=\"", str(xsize),
            "\" height=\"", str(ysize), "\">\n"]))
        pts = {}
        for i in range(len(self)):
            if len(self.R[i]) == 0:
                pts[i] = (r.randint(0,xsize),
                        r.randint(0, ysize))
        for i in reversed(range(len(self))):
            if len(self.R[i]) == 0:
                p = pts[i]
                f.write(''.join(["\t<circle cx=\"", str(p[0]),
                    "\" cy=\"", str(p[1]),
                    "\" r=\"", str(point_radius),
                    "\" stroke=\"green\"
                    stroke-width=\"", str(stroke_width),
                    "\" fill=\"yellow\" />\n"]))
            elif len(self.R[i]) == 2:
                p0 = pts[self.R[i][0]]
                p1 = pts[self.R[i][1]]
                f.write(''.join(["\t<line x1=\"", str(p0[0]),
                    "\" y1=\"",  str(p0[1]),
                    "\" x2=\"", str(p1[0]),
                    "\" y2=\"", str(p1[1]),
                    "\" style=\"stroke:rgb(0,0,255);",
                    "stroke-width:", str(stroke_width),
                    ";opacity:", str(line_opacity),
                    "\" />\n"]))
            else:
                v = self.get_vertices(i)
                polypts = []
                string = "\t<polygon points=\""
                for p in v:
                    polypts.append(pts[p])
                    string = ''.join([string,
                        str(pts[p][0]), ",",
                        str(pts[p][1]), " "])
                string = ''.join([string,
                    "\" style=\"fill:mediumpurple;",
                    "stroke:purple;",
                    "stroke-width:0;",
                    "opacity:", str(poly_opacity),
                    "\" />\n"])
                f.write(string)
        f.write('</svg>')
        f.close()

    def iso_reordering(self): # returns backwards and only does dfs down
        rT = self.R.transpose()
        tops, order, marks = set(), [], set()
        for i in range(len(self)):
            if not rT[i]:
                tops.add(i)
        for t in tops:
            stack = [t]
            temp = []
            while stack:
                if stack[-1] in marks:
                    stack.pop()
                else:
                    temp.append(stack[-1])
                    marks.add(stack[-1])
                    stack.extend(self.R[stack.pop()])
            temp.extend(order)
            order = temp
        return order

class CoPersistenceMatrix(PersistenceMatrix):
    """ pHrow co-persistence algorithm """
    def reduce(self):
        lows = {}
        for i in range(len(self)):
            if self.R[i]:
                if self.R[i][0] in lows:
                    lows[self.R[i][0]].append(i)
                else:
                    lows[self.R[i][0]] = [i]
        for i in reversed(range(len(self))):
            if i in lows:
                indices = lows[i]
                p = indices.pop()
                for j in indices:
                    self.R[j] = self.R[j] ^ self.R[p]
                    self.U[j] = self.U[j] ^ self.U[p]
                self.dgm[p] = i

class pCohCoPersistenceMatrix(PersistenceMatrix):
    """ pCoh co-persistence algorithm """

    def reduce(self):
        Z = []
        for i in range(len(self)):
            indices = []
            for j in Z:
                if i in self.R[j]:
                    indices.append(j)
            if not indices:
                Z.append(i)
            else:
                p = indices.pop()
                for j in reversed(indices):
                    self.R[j] = self.R[j] ^ self.R[p]
                    self.U[j] = self.U[j] ^ self.U[p]
                Z.remove(p)
                self.dgm[p] = i

class AnnotationMatrix(PersistenceMatrix):
    """ annotations co-persistence algorithm """
    def reduce(self): # doesn't use union-find
        av = {}     # annotation vectors
        avT = {}    # transpose of annotation vectors
        for i in range(len(self)):
            temp = SortedList() # so that I can use ^
            for j in self.R[i]:
                if j in av:
                    temp ^= av[j]
            if not temp:
                av[i] = SortedList([i])
                avT[i] = [i]
            else:
                low = temp.pop()
                av[i] = temp
                for j in temp:
                    avT[j].append(i)
                for k in avT.pop(low):
                    av[k].remove(low)
                    av[k] = av[k] ^ temp
                self.dgm[low] = i

class SpectralPersistenceMatrix(PersistenceMatrix):
    """from Harer and Edelsbrunner"""
    def reduce(self):
        for r in range(len(self)):
            for j in range(r,len(self)):
                while self.R[j] and max(self.R[j]) > j-r:
                    low = max(self.R[j])
                    if low in self.dgm and self.dgm[low] is not j:
                        self.R.add_col(self.dgm[low], j)
                        self.U.add_col(self.dgm[low], j)
                    else:
                        self.dgm[low] = j
                        break

class FuturePersistenceMatrix(PersistenceMatrix):
    """ From Nested Dissection paper """
    def reduce(self):
        for i in range(len(self)):
            if self.R[i]:
                low = max(self.R[i])
                self.dgm[low] = i
                for j in range(i+1,len(self)):
                    if low in self.R[j]:
                        self.U.add_col(i,j)
                        self.R.add_col(i,j)

class Vineyard(PersistenceMatrix):
    def __init__(self):
        super().__init__()
        self.vineyard = []

    def switcheroo(self,i): # the old vineyard switcheroo
        self.R.swap_col(i,i+1)
        self.R.swap_row(i,i+1)
        self.U.swap_col(i,i+1)
        self.U.swap_row(i,i+1)

    def col_row_op(self, m, n):
        self.R.add_col(m,n)
        self.U.add_row(n,m)

    def vineyard_algo(self,i):
        self.vineyard.append([i,-1])
        if not self.R[i] and not self.R[i+1]: # Case 1
            if i in self.U[i+1]:
                self.U[i+1].remove(i)
            k = -1
            l = -1
            for n in range(len(self)):
                if self.R[n] and max(self.R[n]) == i:
                    k = n
                if self.R[n] and max(self.R[n]) == i+1:
                    l = n
            if k != l and i in self.R[l]: # Case 1.1
                if k < l: # Case 1.1.1
                    self.switcheroo(i)
                    self.col_row_op(k,l) # PDP = (PRPV)(VPUP)
                if l < k: # Case 1.1.2
                    self.switcheroo(i)
                    self.col_row_op(l,k) # PDP = (PRPV)(VPUP)
                    self.vineyard[-1] = [i]
        if self.R[i] and self.R[i+1]: # Case 2
            if i in self.U[i+1]: # Case 2.1
                self.col_row_op(i,i+1)
                self.switcheroo(i) # PDP = (PRWP)(PWUP)
                if max(self.R[i]) == max(self.R[i+1]): # Case 2.1.2
                    self.col_row_op(i,i+1)
                    self.vineyard[-1] = [i,max(self.R[i+1]), max(self.R[i])]
        if self.R[i] and not self.R[i+1]: # Case 3
            if i in self.U[i+1]: # Case 3.1
                self.vineyard[-1] = [i,max(self.R[i])]
                self.col_row_op(i,i+1)
                self.switcheroo(i)
                self.col_row_op(i,i+1) # PDP = (PRWPW)(WPWUP)
        if not self.R[i] and self.R[i+1]: # Case 4
            if i in self.U[i+1]:
                self.U[i+1].remove(i)

class ZigZagPersistenceMatrix(PersistenceMatrix):

    def __init__(self):
        super().__init__()
        self.coR = []       # coboundary matrix

    def insert_col(self, col):
        super().insert_col(col)
        self.coR.append([])
        s = len(self.R)
        for i in col:
            self.coR[i].append(s)

    def zigzag_reduce(self, order, arrows):
        M = {}      # current matrix 
        Mdgm = {}   # current diagram
        b = {}      # birth times of current cycles
        rMdgm = {}  # reverse lookup for Mdgm
        for t in range(len(arrows)): # 1 is forward arrow, 0 for backward
            s = order[t]
            if arrows[t]:
                M[s] = self.R[s]
                while M[s]:
                    j = max(M[s])
                    if j in Mdgm:
                        M[s] = M[s] ^ M[Mdgm[j]]
                        self.U[Mdgm[j]].append(s)
                    else:
                        self.dgm[b[j]] = t-1
                        Mdgm[j] = s
                        rMdgm[s] = j
                        break
                if not M[s]:
                    b[s] = t
            else:
                if s in rMdgm:
                    p = rMdgm.pop(s)
                    Mdgm.pop(p)
                    b[p] = t
                    for k in self.U[s]:
                        if k in M and k != s:
                            M[k] = M[k] ^ M[s]
                            while M[k]:
                                j = max(M[k])
                                if j in Mdgm:
                                    M[k] = M[k] ^ M[Mdgm[j]]
                                    self.U[Mdgm[j]].append(k)
                                else:
                                    self.dgm[b[k]] = t-1
                                    Mdgm[j] = k
                                    rMdgm[k] = j
                                    break
                            if not M[k]:
                                b[k] = t
                        self.U[s] = [s]
                else:
                    self.dgm[b[s]] = t-1
                M.pop(s)
        for s in b:
            if not b[s] in self.dgm and not s in Mdgm:
                self.dgm[b[s]] = t

