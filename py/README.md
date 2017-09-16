## Most of the interesting stuff is in Matrix.py:

### Matrix

* A Matrix is just a list of SortedLists. Each SortedList represents a simplex, where the indices in the SortedList are the indices of the simplices that the simplex is comprised of.

* Addition of simplices is just symmetric difference, so if you see ^ that's what that is. Although I also just have a function called 'add_col', so idk, maybe I should be more consistent.

### PersistenceMatrix

* A PersistenceMatrix is actually two matrices and a persistence diagram. It keeps the reducing matrix around.

* I guess the columns of the reducing matrix represent coefficients for a linear combination of whatever simplices the corresponding column is currently comprised of, including the original simplex that was there. So for example, before reduction it's just the identity matrix because each column has only itself, and nothing's been added to it yet.

* You don't actually need the reducing matrix for any persistence algorithm, but it keeps track of the column additions done and you do need it for the vineyard algorithm.

## iso_reordering

* If you want an order to add simplices such that your homology is always of minimum dimension. Although right now this method returns the order backwards. It uses the simplices that have no coboundary and does DFS downwards (via boundary operator).

Comes from paper, The Compressed Annotation Matrix: An Efficient Data Structure for Computing Persistent Homology - Boissonnat, Dey, Maria

### spectral_reduce:

* Reduces from the diagonal out. I don't acturally understand the connection to spectral sequences, but you get the same diagram as the normal persistence algorithm.

Comes from Edelsbrunner and Harer textbook.

### future_reduce:

Comes from paper, Persistent Homology and Nested Dissection - Kerber, Sheehy, Skraba

### CoPersistenceMatrix

* A CoPersistenceMatrix is just to have a seperate class to use cohomology algorithms. The difference is the functions expect self.R to be a coboundary matrix.

#### pHrow and pCoh

* Comes from the paper, Dualities in persistent (co)homology - Silva, Morozov, and Johansson.

### annotations:

* Supposedly you can make this better by putting the columns with the same annotation in a union-find structure, but I don't think I have a good data structure or fast algorithm for determining the rows with the same annotations, so this doesn't implement union-find.

Comes from paper, The Compressed Annotation Matrix: An Efficient Data Structure for Computing Persistent Homology - Boissonnat, Dey, Maria

### Vineyard

* A Vineyard stores the change in diagrams over a sequence of swaps in the filtration.

* The vineyard algorithm comes from the paper, Vines and vineyards by updating persistence in linear time - Steiner, Edelsbrunner, and Morozov

* Interpreting the vineyard is weird, but it was the best I could come up with. For an index i, if the next thing in the list is:

	* [i, -1] : Simplices i and i+1 were swapped in the filtration and there's no change to the diagram.

	* [i,k,l] : Simplices i and i+1 were swapped and there was a pairing (k,i), (l,i+1) which is now (k,i+1), (l,i)

	* [i]			: Simplices i and i+1 were swapped and the pairing (i,k), (i+1,l) is now (i+1,k), (i,l)

	* [i,l]		: Simplices i and i+1 were swapped and the pairing (i,k), (l,i+1) is now (i+1,l), (l,i)

* The reason I did it this way is because the diagram is a dictionary so I wanted to keep the keys for the dictionary around. I don't know if it'll become useful in some post-processing or something or if there's a better way to do it, but it works for now. I mean. It's better than storing however many diagrams (maybe), I figure if you can just recreate the same info if you have to then it's good enough.

### Everything else

* Yah, I don't know, that's all I got.

* Oh yah, SortedList is exactly what you'd expect (I hope) and you can (probably) test things with:
`python -m unittest`
