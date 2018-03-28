/**** utils.c ****/

#include "utils.h"

bool odd_bits(int bv){ // Returns 0 if bv has an even number of bits, 1 if odd
	for(int i = sizeof(int) * 8; i > 0; i--){
		bv ^= bv >> 2^i;
	}
	return (bool) (bv & 1);
}

int num_bits(int bv){ // Returns the number of 1 bits in the vector.
	int c =0;
	for(int i=0; i<sizeof(int)*8; i++){
		if (1 & (bv>>i)) c++;
	}
	return c;
}

int low_bit(int r){ // Gives index of the lowest 1 in int r
																// Returns -1 if r is 0
	for(int i = sizeof(int)*8-1; i>=0; i--){
		if((r & (1 << i)) > 0){
			return i;
		}
	}
	return -1;
}

bool bit(int n, int j){ // Returns 1 if the jth bit of n is 1, and 0 otherwise
		return (n >> j) & 1;
}

void utils_test(){

	printf("%s\n", "*************** utils_test ******************");
	if(0){
		fprintf(stderr, "zero is true\n"); // For my sanity only
	}
	if(!odd_bits(0x1)){
		fprintf(stderr, "utils_test: 'odd_bits' outputting wrong value\n");
	}
	if(odd_bits(0x2)){
		fprintf(stderr, "utils_test: 'odd_bits' outputting wrong value\n");
	}
	if(odd_bits(0x1212)){
		fprintf(stderr, "utils_test: 'odd_bits' outputting wrong value\n");
	}
}
