#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define N 500

double A[N][N], B[N][N], C[N][N];

#define MULT_REORDER(i, j, k, ii, jj, kk) \
	for (ii = 0; ii < N; ii++) \
		for (jj = 0; jj < N; jj++) \
			for (kk = 0; kk < N; kk++) \
				C[i][j] += A[i][k] * B[k][j];  

int main(int argc, char** argv) {
	int i, j, k;
	
	if (argc != 2) {
		printf("Usage: %s mode\n", argv[0]);
		return -1;
	}
	
	switch(argv[1][0]) {
		case '2':
			MULT_REORDER(i, j, k, i, k, j);
			break;
		case '3':
			MULT_REORDER(i, j, k, j, k, i);
			break;
		case '1':
		default :
			MULT_REORDER(i, j, k, i, j, k);
			break;
	}

	return 0;
}
