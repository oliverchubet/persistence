import itertools

class SortedList():

    def __init__(self, L=None):
        self._L = []
        if L:
            for i in L:
                self.add(i)

    def add(self, item):
        self._L.insert(self._index(item),item)

    def remove(self, item):
        self._L.remove(item)

    def __getitem__(self, index):
        return self._L[index]

    def __contains__(self, item):
        i = self._index(item)
        return i-1 >= 0 and self[i-1] == item

    def _index(self, item):
        L, R = 0, len(self)
        while L < R:
            M = (L+R)//2
            if self[M] > item:
                R = M
            else:
                L = M+1
        return R

    def __len__(self):
        return len(self._L)

    def __iter__(self):
        return iter(self._L)

    def max(self):
        return self[-1]
    
    def min(self):
        return self[0]

    def __str__(self):
        return self._L.__str__()

    def __repr__(self):
        return self._L.__repr__()

    def __eq__(self, other):
        try:
            return self._L == other._L
        except AttributeError:
            return self._L == other

    def __xor__(self, other):
        return SortedList(set(self) ^ set(other))
