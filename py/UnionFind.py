class UnionFind():
    def __init__(self, L):
        self._parent = {item : item for item in L}

    def _root(self, item):
        root = item
        while root is not self._parent[root]:
            root = self._parent[root]
            self._compress(item, root) 
        return root

    def _compress(self, item, newroot):
        while item is not newroot:
            item, self._parent[item] = self._parent[item], newroot

    def find(self, a, b):
        return self._root(a) is self._root(b)

    def union(self, a, b):
        if not self.find(a,b):
            self._parent[self._root(b)] = self._root(a)
