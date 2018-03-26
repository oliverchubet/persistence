# README

#### To use the persistence algorithm:

Say you want a persistence diagram for a complex:

* Make a ```PersistenceMatrix```
* Insert a list of simplices as a list of their boundary simplices
* Reduce the ```PersistenceMatrix```

``` python
>>> M = PersistenceMatrix() 
>>> M.insert([],[],[],[0,1],[0,2],[1,2])
>>> M.reduce()
```
* The diagram is stored in ```M.dgm```

``` python
>>> M.dgm
{1: 3, 2: 4}
>>> M.print_dgm()
 |-)
  |-)
```
* The reduced matrix is stored in ```M.R```, and reducing matrix in ```M.U```
* For a visual you can print the matrix with ```print_matrix()```
```python
>>> M.R
[[], [], [], [0, 1], [0, 2], []]
>>> M.R.print_matrix()
0 0 0 1 1 0 
0 0 0 1 0 0 
0 0 0 0 1 0 
0 0 0 0 0 0 
0 0 0 0 0 0 
0 0 0 0 0 0 
>>> M.U
[[0], [1], [2], [3], [4], [3, 4, 5]]
>>> M.U.print_matrix()
1 0 0 0 0 0 
0 1 0 0 0 0 
0 0 1 0 0 0 
0 0 0 1 0 1 
0 0 0 0 1 1 
0 0 0 0 0 1 
```
#### To Use the Cohomology Persistence Algorithm:
* Make a ```CoPersistenceMatrix```
* Insert a list of coboundaries for each simplex
	(the transpose of the boundary matrix)
* Reduce the ```CoPersistenceMatrix```

``` python
>>> C = CoPersistenceMatrix() 
>>> C.insert([3,4],[3,5],[4,5],[],[],[])
>>> C.reduce()
```

* The diagram will be the same using cohomology or homology
* ```CoPersistenceMatrix``` is a subclass of ```PersistenceMatrix``` so all of the previous methods are still available

#### Other Persistence Algorithms Implemented:

* To use a different algorithm, just use the subclass that implements the desired version
* Make note of whether the input is a boundary or coboundary matrix

| Persistence Algorithm | Class Name                | Ref |
| :-------------------: | :-----------------------: | :-: |
| Original              | PersistenceMatrix         | [1] |
| pHrow (cohomology)    | CoPersistenceMatrix       | [2] |
| pCoh (cohomology)     | pCohCoPersistenceMatrix   | [2] |
| Annotations           | AnnotationMatrix          | [3] |
| Spectral sequence     | SpectralPersistenceMatrix | [1] | 
| Row reduction         | FuturePersistenceMatrix   | [4] |

#### To Use The Vineyard Algorithm:

If you already have a persistence diagram, but want to swap two columns, you can update the diagram using the vineyard algorithm.

* Make a ```Vineyard```
* Insert a boundary matrix for you complex
* Reduce the ```Vineyard```
* Call ```vineyard_list``` with a list of indices to swap. For each index ```i``` in the list, columns ```i``` and ```i+1``` will be swapped and the diagram will be updated.

```python
>>> V = Vineyard()
>>> V.insert([],[],[],[0,1],[0,2],[1,2])
>>> V.reduce()
>>> V.dgm
{5: 'inf', 2: 4, 1: 3, 0: 'inf'}
>>> V.print_dgm()

[5, inf)        :     [)
[2, 4)          :  [-)
[1, 3)          : [-)
[0, inf)        :[-----)
>>> V.vineyard_list(0,1,2,4)
>>> V.dgm
{5: 'inf', 1: 4, 3: 2, 0: 'inf'}
>>> V.print_dgm()

[5, inf)        :     [)
[1, 4)          : [--)
[3, 2)          :   [)
[0, inf)        :[-----)
```

#### To run the unittests:

* Run ```python -m unittest```

#### References:

[1] Edelsbrunner, H., & Harer, J. (2010). Computational topology: an introduction. American Mathematical Soc.

[2] De Silva, V., Morozov, D., & Vejdemo-Johansson, M. (2011). Dualities in persistent (co) homology. Inverse Problems, 27(12), 124003.

[3] Boissonnat, J. D., Dey, T. K., & Maria, C. (2015). The compressed annotation matrix: An efficient data structure for computing persistent cohomology. Algorithmica, 73(3), 607-619.

[4] Kerber, M., Sheehy, D. R., & Skraba, P. (2016, January). Persistent homology and nested dissection. In Proceedings of the twenty-seventh annual ACM-SIAM symposium on Discrete algorithms (pp. 1234-1245). Society for Industrial and Applied Mathematics.

[5] Cohen-Steiner, D., Edelsbrunner, H., & Morozov, D. (2006, June). Vines and vineyards by updating persistence in linear time. In Proceedings of the twenty-second annual symposium on Computational geometry (pp. 119-126). ACM.
