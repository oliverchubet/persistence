/**** persistence.h ****/

#ifndef _PERSISTENCEH_
#define _PERSISTENCEH_

#include "matrix.h"

typedef struct persistence{
	matrix * inc;
	matrix * red;
} persistence;


/**** init_persistence ****
 *	Initializes a persistence struct.
 *
 *	Warning: don't give it a matrix that already has stuff in it that you
 *	expect it to have after initialization, because it will get eaten.
 *
 *	If you want to use a matrix that's already populated, you can use
 *	the copy_matrix function, and then fix the reducing matrix manually,
 *	although, in general simplices are meant to be added by insert_simplex.
 *	Maybe I'll make a function to do that later, because it seems like
 *	a probable future issue.
 *
 *	From c:
 *
 *		persistence * p;
 *		matrix * inc;
 *		matrix * red;
 *		peristence_init(p, inc, red);
 *	
 *		... (stuff) ...
 *	
 *		free_persistence(p);
 *
 *	From python:
 *
 *		>>> p = pointer(PERSISTENCE())
 *		>>> inc = pointer(MATRIX())
 *		>>> red = pointer(MATRIX())
 *		>>> md.init_persistence(p, inc, red)
 *		
 *		... (stuff) ...
 *		
 *		>>> md.free_persistence(p)
 */
void init_persistence(persistence * p, matrix * inc, matrix * red);

/**** free_persistence ****
 *	Frees memory malloc-ed for the two matrices in the persistence struct.
 */
void free_persistence(persistence * p);

/**** insert_simplex ****
 *	Inserts sim as a column of the incidence matrix, and adds a column with a 1
 *	on the diagonal to the reducing matrix.
 *	This function will give an error if you try to add a simplex that depends
 *	on simplices that havent been added yet.
 */
void insert_simplex(persistence * p, int sim);

/**** set_simplex ****
 *	Set a simplex at the index. Changes whatever was there previously.
 *	Only for changing, not for inserting new.
 */
void set_simplex(persistence * p, int index, int sim);

/**** reduce ****
 *	Persistence algorithm. Takes a persistence struct. Reduces the incidence
 *	matrix and keeps track of the operations in the reducing matrix.
 */
void reduce(persistence * p);

/**** vineyard ****
 *	Takes a persistence struct. Assumes i and i+1 have been switched 
 *	with switch_ij(p,i,i+1). It inverts the reducing matrix since that's
 *	what the vineyard algorithm uses.
 */
void vinyard(persistence * p, int i);

/**** printp ****
 *	Prints inc and red matrices of p.
 */
void printp(persistence * p);

/**** birth_death ****
 *	Prints out birth-death pairs for a reduced persistence struct
 */
void birth_death(persistence * p);

/**** persistence_test ****
 *	Just some unit tests from when I wrote this... it could be better.
 *	It might print some stuff to stderr if it thinks something
 *	is wrong.
 */
void persistence_test();

#endif
