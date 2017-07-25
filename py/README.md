## Most of the interesting stuff is in Matrix.py:

### Matrix

* A Matrix is just a list of SortedLists. Each SortedList represents a simplex, where the indices in the SortedList are the indices of the simplices that the simplex is comprised of.

* Addition of simplices is just symmetric difference, so if you see ^ that's what that is. Although I also just have a function called 'add_col', so idk, maybe I should be more consistent.

### PersistenceMatrix

* A PersistenceMatrix is actually two matrices and a persistence diagram. It keeps the reducing matrix around.

* I guess the columns of the reducing matrix represent coefficients for a linear combination of whatever simplices the corresponding column is currently comprised of, including the original simplex that was there. So for example, before reduction it's just the identity matrix because each column has only itself, and nothing's been added to it yet.

* You don't actually need the reducing matrix for any persistence algorithm, but you do need it for the vineyard algorithm.

### CoPersistenceMatrix

* A CoPersistenceMatrix is just to have a seperate class to use the cohomology algorithm. It has lows which is a dictionary where the values are sets of indices of columns whose lowest ones are equal to the key. You have to update lows whenever you do a column or row operation otherwise when you accesses lows it could be using old information.

#### pHrow

* The reduce algorithm (pHrow) in the CoPersistenceMatrix class comes from the paper, Dualities in persistent (co)homology - Silva, Morozov, and Johansson. I don't update dgm in this one because lows reduces to the persistence diagram.

#### pCoh

* The cohomology algorithm (pCoh) is from the same paper. The matrix R should be the transpose of the incidence matrix. 

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
