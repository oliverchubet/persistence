/**** matrix.c ****/

#include "matrix.h"

void init_matrix(matrix * m){
	m->values = (int *)malloc(sizeof(int) * sizeof(int) * 8);
	m->used = 0;
	m->size = sizeof(int) * 8;
}

void copy_matrix(matrix * orig, matrix * copy){
	init_matrix(copy);
	for(int i = 0; i<orig->used; i++){
		insert_col(copy, orig->values[i]);
	}
}

void insert_col(matrix * m, int value){
	if(m->used == m->size){
		fprintf(stderr, "insert_col: Exceeded maximum capacity of matrix...\n");
		return;
	}
	m->values[m->used++] = value;
}

void add_col(matrix * m, int i, int j){ // Adds col i to col j
	m->values[j]=(m->values[j])^(m->values[i]);
}

void set_col(matrix * m, int col, int value){
	if(m->used < col){
		fprintf(stderr, "set_col: That column doesn't exist...\n");
		return;
	}
	m->values[col]=value;
}

void add_row(matrix * m, int i, int j){ // Adds row i to row j.
	if(i>j){
		for(int k = 0; k < m->used; k++){
			m->values[k] ^= (m->values[k] >> i-j) & (1 << j);
		}
	} else {
		for(int k = 0; k < m->used; k++){
			m->values[k] ^= (m->values[k] << j-i) & (1 << j);
		}
	}
}

void free_matrix(matrix * m){
	free(m->values);
	m->values = NULL;
	m->size = 0;
	m->used = 0;
}

bool in_matrix(matrix * m, int value){
	bool found = false;
	for(int i = 0; i < m->used; i++){
		if(m->values[i] == value){
			found = true;
			break;
		}
	}
	return found;
}

void bv_print(matrix * m){
	printf("\t");
	for(int i=0; i<m->used; i++){
		printf("%i ", i);
	}
	printf("\n\t");
	for(int i=0; i<m->used; i++){
		printf("_ ");
	}
	printf("\n");
	for(int i=0; i<m->used; i++){
		printf("%i|\t",i);
		for(int j=0; j<m->used; j++){
			printf("%i ", ((1 << i) & m->values[j]) >> i);
		}
		printf("\n");
	}
	printf("\n");
}

void inv_matrix(matrix * m, matrix * inv){
	init_matrix(inv);
	for(int i=0; i<m->used; i++){
		insert_col(inv, 1<<i);
	}
	for(int i=m->used-1; i>=0; i--){
		int t = m->values[i];
		t &= ~(1 << i);
		int j = low_bit(t);
		while(j>=0){
			add_row(inv, i, j);
			t &= ~(1 << j);
			j = low_bit(t);
		}
	}
}

int lowest(matrix * m, int r){ // Gives index of the lowest 1 in col r of matrix m.
																// Returns -1 if column is empty
	for(int i = m->used-1; i>=0; i--){
		if((m->values[r] & (1 << i)) > 0){
			return i;
		}
	}
	return -1;
}

void simple_mult(matrix * m1, matrix * m2, matrix * r){
															// Multiplies matrix m1 with m2 and stores it in r
	if(m1->used != m2->used){
		fprintf(stderr, "simple_mult: matrices are incompatible sizes. Exiting...");
		return;
	}
	init_matrix(r);	
	r->used = m1->used;
	for(int i=0; i<m1->used; i++){ // For good measure. 	
		r->values[i]=0;
	}
	for(int i=0; i<m1->used; i++){
		for(int j=0; j<m1->used; j++){
			for(int k=0; k<m1->used; k++){
				r->values[j] ^= (((((m1->values[k] >> i) & (m2->values[j]) >> k) & 1) << i));
			}
		}
	}
	
}

void switch_ij(matrix * m, int i, int j){ // Switches rows and columns i and j of matrix m
	if(i<j){ // So bit shifting will be easier
		int l = i;
		i = j;
		j = l;
	}
	int t = m->values[i];
	m->values[i] = m->values[j];
	m->values[j] = t;
	for(int k = 0; k<m->used; k++){
		t = m->values[k];
		m->values[k] = t & ~(1 << i) & ~(1 << j); // Remove ith and jth bits
		m->values[k] ^= (1 << j) & (t >> (i-j)); // Move i to j's place and add it back
		m->values[k] ^= (1 << i) & (t << (i-j)); // Move j to i's place and add it back
	}
}

void vertices_matrix(matrix * m, matrix * v){
	init_matrix(v);
	for (int i = 0; i < m->used; i++){
		if (m->values[i]==1){
			insert_col(v,(1 << i));
		} else {
			int t = 0;
			for (int j = 0; j < i; j++){
				t |= bit(m->values[i],j) * v->values[j];
			}
			insert_col(v,t);
		}
	}
}

void matrix_test(){
	printf("%s\n", "*************** matrix_test ******************");
	matrix m0;
	matrix m1;
	matrix m2;
	
	init_matrix(&m0);
	init_matrix(&m1);
	init_matrix(&m2);
	
	insert_col(&m0, 0x1);
	insert_col(&m0, 0x2);
	insert_col(&m0, 0x4);
	insert_col(&m0, 0x8);

	insert_col(&m1, 0x1);
	insert_col(&m1, 0x2);
	insert_col(&m1, 0x3);

	insert_col(&m2, 0x1);
	insert_col(&m2, 0x2);
	insert_col(&m2, 0x3);
	insert_col(&m2, 0x7);

	if(!in_matrix(&m0, 0x1)){
		fprintf(stderr, "matrix_test: 'in_matrix' not finding value.");
	}
	if(in_matrix(&m0, 0x3)){
		fprintf(stderr, "matrix_test: 'in_matrix' found a value that wasn't inserted.");
	}

	add_col(&m2, 0, 1);
	if(m2.values[1] != 0x3){
		fprintf(stderr, "matrix_test: 'add_col' not giving correct values.");
	}
	if(m2.values[0] != 0x1){
		fprintf(stderr, "matrix_test: 'add_col' not giving correct values.");
	}


	printf("\n%s\n", "Printing bv matrix m2:");
	bv_print(&m2);
	add_row(&m2, 0, 1);
	printf("%s", "Adding row 0 to 1 in matrix 2...\n");
	printf("\n%s\n", "Printing bv matrix m2:");
	bv_print(&m2);
	printf("%s", "Adding row 1 to 0 in matrix 2...\n");
	add_row(&m2, 1, 0);
	bv_print(&m2);

	free_matrix(&m1);

	printf("\n%s\n", "Printing bv matrix m0:");
	bv_print(&m0);
	printf("\n%s\n", "Printing bv matrix m1:");
	bv_print(&m1);
	printf("\n%s\n", "Printing bv matrix m2:");
	bv_print(&m2);

	switch_ij(&m2, 2,3);
	printf("\n%s\n", "Switching row/col 2 and 3 of m2...");
	printf("\n%s\n", "Printing bv matrix m2:");
	bv_print(&m2);

	switch_ij(&m2, 1,2);
	printf("\n%s\n", "Switching row/col 1 and 2 of m2...");
	printf("\n%s\n", "Printing bv matrix m2:");
	bv_print(&m2);

	if(lowest(&m0, 3) != 3){
		fprintf(stderr, "matrix_test: 'lowest' outputting wrong value");
	}

	matrix r;
	init_matrix(&r);
	simple_mult(&m0,&m0,&r);
	printf("\n%s\n", "Printing bv matrix m0*m0:");
	bv_print(&r); // Should be the identity

	simple_mult(&m2,&m0,&r);
	printf("\n%s\n", "Printing bv matrix m2*m0:");
	bv_print(&r); // Should be m2
		
	free_matrix(&m0);
	free_matrix(&m2);
}
