#! /bin/python

from structs import *
md = cdll.LoadLibrary('/home/shpew12/git/sheehy_is_2017/c/libtest.so')
md

####
# Converts a matrix struct to SimplicialComplex instance
####

m = MATRIX()

m.insert_col(0)
m.insert_col(1)
m.insert_col(1)
m.insert_col(1)
m.insert_col(0b110)
m.insert_col(0b1100)
m.insert_col(0b1010)
m.insert_col(0b1110000)

sc = m.to_sc()
#m.print()
v = m.vertices_matrix()
#v.print()



s=[*sc.iter_ordered()]

#print(s)

####
# Making sure it works with peristence structs too
####

inc = MATRIX()
red = MATRIX()
p = PERSISTENCE(inc,red)
p.insert_simplex(0)
p.insert_simplex(1)
p.insert_simplex(1)
p.insert_simplex(1)
p.insert_simplex(0b110)
p.insert_simplex(0b1100)
p.insert_simplex(0b1010)
p.insert_simplex(0b1110000)

sc2 = p.inc.contents.to_sc()

#print([*sc2.iter_ordered(key=filtration(max))])


####
# Compare Oliver's algorithm to mine to make sure we get the same thing
####
pm = PersistenceMatrix(*sc2.iter_ordered(key=filtration(max)))

#print("\n")

#print(pm.get_births_deaths())

p.reduce()
#p.birth_death()

####
# Tetrahedron
####


