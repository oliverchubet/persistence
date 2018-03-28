/**** utils.h ****/

#ifndef _UTILSH_  
#define _UTILSH_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SWAP(a,b)	(a^=b, b^=a, a^=b);

typedef enum { false, true } bool;

/**** odd_bits ****	
 *	Takes an integer and gives you a boolean value where 1
 *	corresponds to the binary representation of that number
 *	having an odd number of bits
 *
 *	ex:
 *	odd_bits(0)=0, odd_bits(0b111)=1, odd_bits(10)=0, etc...
 */
bool odd_bits(int bv);

/**** num_bits ****
 * Takes an integer and gives you an integer of the number of bits
 * in the binary representation of the integer you gave
 *
 * ex:
 * num_bits(10) = num_bits(0xa) = num_bits(0b1010) = 2
 */
int num_bits(int bv);

/**** low_bit ****
 *	Gives the place of the lowest (highest-value) bit of the integer in binary
 */
int low_bit(int r);

/**** bit ****
 *	Returns whether the jth bit of n is 1.
 *	(Returns 1 if it is, and 0 if it's not)
 */
bool bit(int n, int j);

/**** utils_test ****
 *	Just some unit tests from when I wrote this... it could be better.
 *	It might print some stuff to stderr if it thinks something
 *	is wrong.
 */
void utils_test();

#endif
