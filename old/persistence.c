/**** persistence.c ****/

#include "persistence.h"

void init_persistence(persistence * p, matrix * inc, matrix * red){
	init_matrix(inc);
	init_matrix(red);
	p->inc = inc;
	p->red = red;
}

void free_persistence(persistence * p){
	free_matrix(p->inc);
	free_matrix(p->red);
}

void insert_simplex(persistence * p, int sim){
	if(sim > (1 << p->inc->used)){
		fprintf(stderr, "Error: Simplex invalid. Exiting fucntion...\n");
		return;	// Depends on a simplex that wasn't added yet.
	}
	insert_col(p->inc,sim);
	insert_col(p->red, (1 << p->red->used)); // Adds a 1 to the diagonal of the reducing matrix for the new simplex.
}

void set_simplex(persistence * p, int index, int sim){
	p->inc->values[index] = sim;
}

void reduce(persistence * p){	// Uses persistence algorithm to reduce inc matrix and record red matrix 
	for(int i = p->inc->used-1; i>=0; i--){
		for(int j = i+1; j<p->inc->used; j++){
			if(lowest(p->inc, i) == lowest(p->inc, j)){
				add_col(p->inc, i, j);
				add_col(p->red, i, j);
			}
		}
	}
}

void vineyard(persistence * p, int i){ // Switches col/row i and i+1 then will fix the RU decomposition (supposedly)

																						// ie. the input should be p->inc is PRP, and p->red is PUP
																						// Hold on to your socks, this one's a ride.
	matrix inv;
	init_matrix(&inv);
	inv_matrix(p->red, &inv);
	copy_matrix(&inv, p->red);
	switch_ij(p->red, i, i+1);
	switch_ij(p->inc, i, i+1);
	if(p->inc->values[i] | p->inc->values[i+1] == 0){ // Col i, i+1 are zero ie. positive simplices
		p->red->values[i] &= ~(1<<i+1);
		int k=-1;
		int l=-1;
		for(int j = 0; j<p->inc->used; j++){
			int t = p->inc->values[j];
			if(((1<<i)-1) < t && t < (1 << i+1)) k = j; // equivalent to lowR(k) = i
			if((1<<i+1)-1 < t && t < (1 << i+2)) l = j; // equivalent to lowR(l) = i+1
		}
		if(k==l || ~((p->inc->values[l] >> i) & 1)){ 	// Supposedly this means it's already an RU decomposition.
										// (They won't be equal unless they're both -1)
										// The second condition is from Case 1.1: R[i,l]=1
		} else {
		 		if(k<l){
					add_col(p->inc, k, l);
					add_row(p->red, l, k);
				} else {
					add_col(p->inc, l, k);
					add_row(p->red, k, l);
				}
		}
	}
	else if(p->inc->values[i] & p->inc->values[i+1] == 1){ // Col i, i+1 are both 1, ie negative simplices
		if(p->red->values[i]>>i+1 ==1){ // U[i,i+1]=1 from the paper (but we're looking at PUP at this point)
			switch_ij(p->inc, i, i+1);
			switch_ij(p->red, i, i+1); // So that I can apply W to R and U instead of PRP and PUP to get PRWP and PWUP
			add_row(p->red, i+1, i); // WU
			add_col(p->inc, i, i+1); // RW
			switch_ij(p->inc, i, i+1); // PRWP
			switch_ij(p->red, i, i+1); // PWUP

			if(p->inc->values[i] > p->inc->values[i+1]){ // checks if lowR(i)>lowR(i+1). If so, PRWP should be PRWPW and PWUP should be WPWUP
																										// The condition should be equivalent assuming lowR(i) != lowR(i+1), which I don't think it can be.
				add_row(p->red, i+1, i); // WPWUP
				add_col(p->inc, i, i+1); // PRWPW
			}
		}
	}
	else if(p->inc->values[i] == 1){ // col i negative, col i+1 is positive
		if(p->red->values[i]>>i+1 ==1){
			switch_ij(p->red, i, i+1); // U
			switch_ij(p->inc, i, i+1); // R
			add_row(p->red, i+1, i); // WU
			add_col(p->inc, i, i+1); // RW
			switch_ij(p->red, i, i+1); // PWUP
			switch_ij(p->inc, i, i+1); // PRWP
			add_row(p->red, i+1, i); //WPWUP
			add_col(p->inc, i, i+1); //PRWPW		
		}
	}
	else { // col i is positive, col i+1 is negative
		if(p->red->values[i]>>i+1 ==1){
			switch_ij(p->red, i+1, i); // U
			switch_ij(p->inc, i+1, i); // R
			add_row(p->red, i, i+1); // WU
			add_col(p->inc, i+1, i); // RW
			switch_ij(p->red, i+1, i); // PWUP
			switch_ij(p->inc, i+1, i); // PRWP
			add_row(p->red, i, i+1); //WPWUP
			add_col(p->inc, i+1, i); //PRWPW		
		}
	}

}

void birth_death(persistence * p){
	int pairs[p->inc->used];
	for(int i = 1; i<p->inc->used; i++){
		pairs[i] = 0;
	}
	pairs[0]=1;
	for(int i = 1; i<p->inc->used; i++){
		if(p->inc->values[i] != 0){
			printf("(%i,%i)\n", low_bit(p->inc->values[i]), i);
//		bds->births[i-1]=low_bit(p->inc->values[i]);
//		bds->deaths[i-1]=i;
			pairs[low_bit(p->inc->values[i])]=1;
			pairs[i]=1;
		}
	}
	for(int i = 0; i<p->inc->used; i++){
		if (pairs[i]==0){
			printf("(%i,inf)\n", i);
		}
	}
}

void printp(persistence * p){
	printf("Incidence matrix:\n");
	bv_print(p->inc);
	printf("Reducing matrix:\n");
	bv_print(p->red);
}

void persistence_test(){
	printf("%s\n", "*************** persistence_test ******************");
	persistence r;
	matrix rinc;
	matrix rred;

	init_persistence(&r, &rinc, &rred);

	insert_simplex(&r, 0x0);
	insert_simplex(&r, 0x0);
	insert_simplex(&r, 0x0);
	insert_simplex(&r, 0x0);
	insert_simplex(&r, 0x0);
	insert_simplex(&r, 0x3);
	insert_simplex(&r, 0x5);
	insert_simplex(&r, 0x6);
	insert_simplex(&r, 0x9);
	insert_simplex(&r, 0b11100000);
	insert_simplex(&r, 0b101100000);

	printp(&r);

	printf("%s\n", "Reducing r");	
	reduce(&r);

	printp(&r);

	birth_death(&r);

	printf("%s\n","Running vineyards algo");
	vineyard(&r, 8);

	printp(&r);

}
