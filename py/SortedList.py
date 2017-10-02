class SortedList(list):

    def __init__(self, L=None):
        if L:
            for i in L:
                self.add(i)

    def add(self, item):
        self.insert(self._index(item),item)

    def append(self, item):
        self.add(item)

    def extend(self, other):
        for i in other:
            self.add(i)

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

    def max(self):
        return self[-1]

    def min(self):
        return self[0]

    def __xor__(self, other):
        return SortedList(set(self) ^ set(other))

    def __sub__(self, other):
        temp = []
        otemp = list(other)
        while self and otemp:
            slast, olast = self.pop(), otemp.pop()
            if slast > olast:
                temp.append(slast)
                otemp.append(olast)
            elif slast < olast:
                temp.append(olast)
                self.append(slast)
        while temp:
            self.append(temp.pop())
        self.extend(otemp)
