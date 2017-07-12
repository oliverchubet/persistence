/**** matrix.h ****/

#ifndef _MATRIXH_
#define _MATRIXH_

#include "utils.h"

typedef struct matrix {
	int * values;
	size_t used;
	size_t size;
} matrix;

/**** init_matrix ****
 *	Initializes matrix struct.
 *
 * 	From c: 
 * 		Just call on a matrix pointer before you start
 * 		calling functions on the matrix:
 *
 * 			matrix * m;
 * 			init_matrix(m);
 *
 * 			... (stuff) ...
 * 			
 * 			free_matrix(m);
 *
 * 	From python:
 * 		You can create a matrix and then initialize it by passing a
 * 		pointer to it:
 *
 * 			>>> m = pointer(MATRIX())
 * 			>>> md.init_matrix(m)
 *			
 *			... (stuff) ...
 * 			
 * 			>>> md.free_matrix(m)
 */
void init_matrix(matrix * m);

/**** copy_matrix ****
 *	The orig matrix should already be initialized, but copy does not.
 *	This makes a copy of the matrix at orig in the location copy.
 *
 *	Example in c:
 *
 *		matrix * orig;
 *		init_matrix(orig);
 *
 *		... (do stuff to orig) ...
 *
 *		matrix * copy;
 *		copy_matrix(orig, copy);
 *
 *	Example in python:
 *		
 *		>>> orig = pointer(MATRIX())
 *		>>> md.init_matrix(orig)
 *
 *		... (do stuff to orig) ...
 *
 *		>>> copy = pointer(MATRIX())
 *		>>> md.copy_matrix(orig, copy)
 */
void copy_matrix(matrix * orig, matrix * copy);

/**** insert_col ****
 * 	Takes an integer and appends a column to the matrix at m
 * 	which is a bit vector of the integer in binary.
 *	To be explicit you can do something like:
 *		
 *		insert_col(m, 0b101);
 */
void insert_col(matrix * m, int value);

/**** in_matrix ****
 *	Checks if a value (bit vector) is a column of the matrix at m.
 *	Returns 0 if it isn't and 1 if it is.
 */
bool in_matrix(matrix * m, int value);

/**** add_col **** O(1)
 *	Adds column i to j of the matrix at m (uses xor/symmetric difference)
 */
void add_col(matrix * m, int i, int j);

/**** set_col ****
 *	Sets column col of the matrix at m to value
 */
void set_col(matrix * m, int col, int value);

/**** add_row **** O(n)
 *	Adds row i to j of the matrix at m (uses xor/symmetric difference)
 */
void add_row(matrix * m, int i, int j);

/**** free_matrix ****
 *	Frees the memory malloc-ed for the values of your matrix.
 */
void free_matrix(matrix * m);

/**** lowest ****
 *	Will give you the index of the lowest 1 in column r of the matrix at m.
 *	(Lowest is technically the highest valued bit, but it's the lowest when you
 *	print it.) 
 */
int lowest(matrix * m, int r);

/**** inv_matrix ****
 *	Given an upper triangular matrix in m, the inverse will be stored at inv.
 *	The matrix at m must be initialized, but inv just needs to be declared.
 */
void inv_matrix(matrix * m, matrix * inv);

/**** bv_print ****
 *	Prints the matrix at m.
 */
void bv_print(matrix * m);

/**** simple_mult ****
 *	This will exit if m1 and m2 aren't the same size.
 *	Multiples m1*m2 and stores it in r.
 *	m1 and m2 should be initialized (init_matrix), but r doesn't have to be.
 */	
void simple_mult(matrix * m1, matrix * m2, matrix * r);

/**** switch_ij ****
 *	Swaps rows i and j and then swaps columns i and j of the matrix at m.
 */
void switch_ij(matrix * m, int i, int j);

/**** vertices_matrix ****
 *	If you have a matrix representing incidence of boundary simplices
 *	and you want to convert to a matrix representing incidence of 
 *	vertices explicitly, input the boundary matrix at m, and the 
 *	matrix of incident vertices will be stored at v
 */
void vertices_matrix(matrix * m, matrix * v);

/**** matrix_test ****
 *	Just some unit tests from when I wrote this... it could be better.
 *	It might print some stuff to stderr if it thinks something
 *	is wrong.
 */
void matrix_test();

#endif
