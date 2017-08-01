#/usr/bin/env python3

from SortedList import *

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
        self.dgm = {}       # persistence diagram (brith:death)

    def __len__(self):
        return len(self.R)

    def insert_col(self, col):
        col = SortedList(col)
        self.R.append(col)
        self.U.append(SortedList([len(self)-1]))

    def reduce(self): # Optimized original persistence algo
        for i in range(len(self)):
            while self.R[i]:
                j = max(self.R[i])
                if j in self.dgm:
                    self.R.add_col(self.dgm[j],i)
                    self.U.add_col(self.dgm[j],i)
                else:
                    self.dgm[j] = i
                    break

    def future_reduce(self): # From the Kerber paper
        for i in range(len(self)):
            if self.R[i]:
                low = max(self.R[i])
                self.dgm[low] = i
                for j in range(i+1,len(self)):
                    if low in self.R[j]:
                        self.U.add_col(i,j)
                        self.R.add_col(i,j)

class CoPersistenceMatrix(PersistenceMatrix):
    def pHrow(self):
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
                self.dgm[p] = min(self.R[p])

    def pCoh(self): # maybe it would be better if columns were passed in one at a time and Z was a dictionary of columns
                    # otherwise you're not really "throwing out" columns
                    # but there's no point throwing things out if you're given it all at once because it'll just take up time to delete stuff and your max space is still whatever they originally gave you
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

class Vineyard(PersistenceMatrix):
    def __init__(self):
        super().__init__()
        self.vineyard = [] 

    def switcheroo(self,i):
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
                    if k < l : # Case 1.1.1
                        self.switcheroo(i)
                        self.col_row_op(k,l) # PDP = (PRPV)(VPUP)
                    if l < k : # Case 1.1.2
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

