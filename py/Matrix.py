#!/usr/bin/env python3

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

    def reduce(self): # original persistence algorithm
        for k1 in range(len(self)):
            check = False
            while not check:
                check = True
                for k2 in range(len(self)):
                    if (self[k1] and self[k2]) \
                        and (k2 < k1) and (max(self[k1]) == max(self[k2])):
                        self.add_col(k2,k1)
                        check = False

class PersistenceMatrix:
    def __init__(self):
        self.inc = Matrix() # incidence matrix
        self.red = Matrix() # reducing matrix
        self.dgm = {}       # persistence diagram (birth:death)

    def __len__(self):
        return len(self.inc)

    def insert_col(self, col):
        col = SortedList(col)
        self.inc.append(col)
        self.red.append(SortedList([len(self)-1]))

    def reduce(self): # persistence algorithm that updates the reducing matrix and diagram
        for k1 in range(len(self)):
            if k1 and self.inc[k1-1]:
                self.dgm[max(self.inc[k1-1])] = k1-1
            check = False
            while not check:
                check = True
                for k2 in range(k1):
                    if self.inc[k1] and self.inc[k2] \
                            and max(self.inc[k1]) == max(self.inc[k2]):
                        self.inc.add_col(k2,k1)
                        self.red.add_col(k2,k1)
                        check = False
        for x in range(len(self)): # arguably I don't need this
            if not self.inc[x] and x not in self.dgm:
                self.dgm[x] = "inf"

class CoPersistenceMatrix(PersistenceMatrix):
    def __init__(self):
        super().__init__()
        self.lowR = {} # dictionary of sets of indices for lowest ones equal to j

    def insert_col(self,col):
        super().insert_col(col)
        if col:
            if max(col) in self.lowR:
                self.lowR[max(col)].add(len(self)-1) 
            else:
                self.lowR[max(col)] = SortedList([len(self)-1])

    def reduce(self): #pHrow
        for i in reversed(range(len(self))):
            if i in self.lowR:
                indices = self.lowR[i]
                p = indices[0] 
                for j in indices[1:]:
                    self.inc[j] = self.inc[j] ^ self.inc[p]
                    self.lowR[i].remove(j)
                    if self.inc[j]:
                        self.lowR[max(self.inc[j])].add(j)
                    self.red[j] = self.red[j] ^ self.red[p]
        
class Vineyard(PersistenceMatrix):
    def __init__(self):
        super().__init__()
        self.vineyard = [] 

    def switcheroo(self,i):
        self.inc.swap_col(i,i+1)
        self.inc.swap_row(i,i+1)
        self.red.swap_col(i,i+1)
        self.red.swap_row(i,i+1)

    def col_row_op(self, m, n):
        self.inc.add_col(m,n)
        self.red.add_row(n,m)

    def vineyard_algo(self,i):
            self.vineyard.append([i,-1])
            if not self.inc[i] and not self.inc[i+1]: # Case 1
                if i in self.red[i+1]:
                    self.red[i+1].remove(i)
                k = -1
                l = -1
                for n in range(len(self)):
                    if self.inc[n] and max(self.inc[n]) == i:
                        k = n
                    if self.inc[n] and max(self.inc[n]) == i+1:
                        l = n
                if k != l and i in self.inc[l]: # Case 1.1
                    if k < l : # Case 1.1.1
                        self.switcheroo(i)
                        self.col_row_op(k,l) # PDP = (PRPV)(VPUP)
                    if l < k : # Case 1.1.2
                        self.switcheroo(i)
                        self.col_row_op(l,k) # PDP = (PRPV)(VPUP)
                        self.vineyard[-1] = [i]
            if self.inc[i] and self.inc[i+1]: # Case 2
                if i in self.red[i+1]: # Case 2.1
                    self.col_row_op(i,i+1)
                    self.switcheroo(i) # PDP = (PRWP)(PWUP)
                    if max(self.inc[i]) == max(self.inc[i+1]): # Case 2.1.2
                        self.col_row_op(i,i+1)
                        self.vineyard[-1] = [i,max(self.inc[i+1]), max(self.inc[i])]
            if self.inc[i] and not self.inc[i+1]: # Case 3
                if i in self.red[i+1]: # Case 3.1
                    self.vineyard[-1] = [i,max(self.inc[i])]
                    self.col_row_op(i,i+1)
                    self.switcheroo(i)
                    self.col_row_op(i,i+1) # PDP = (PRWPW)(WPWUP)
            if not self.inc[i] and self.inc[i+1]: # Case 4
                if i in self.red[i+1]:
                    self.red[i+1].remove(i)

