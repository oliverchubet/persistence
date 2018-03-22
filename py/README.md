# README

#### To use the persistence algorithm:

Say you want a persistence diagram for the following complex:

<svg width="250" height="70">
        <line x1="25" y1="25" x2="75" y2="25" style="stroke:rgb(0,0,255);stroke-width:2;opacity:0.75" />
        <line x1="125" y1="50" x2="75" y2="25" style="stroke:rgb(0,0,255);stroke-width:2;opacity:0.75" />
        <line x1="25" y1="25" x2="125" y2="50" style="stroke:rgb(0,0,255);stroke-width:2;opacity:0.75" />
        <circle cx="75" cy="25" r="4" stroke="green" stroke-width="2" fill="yellow" />
        <text x="75" y="17" font-family="sans-serif" font-size="20px" text-anchor="middle" fill="red">2</text>     <circle cx="125" cy="50" r="4" stroke="green" stroke-width="2" fill="yellow" />
        <text x="125" y="37" font-family="sans-serif" font-size="20px" text-anchor="middle" fill="red">1</text>    <circle cx="25" cy="25" r="4" stroke="green" stroke-width="2" fill="yellow" />
        <text x="25" y="16" font-family="sans-serif" font-size="20px" text-anchor="middle" fill="red">0</text></svg>

* Make a ```PersistenceMatrix```
* Insert simplices as a list of their boundary simplices
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
