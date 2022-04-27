/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include <stdio.h>
#include <string.h>

#include "utils.h"
#include "cblas.h"

#define DIE(assertion, call_description)				\
	do {								\
		if (assertion) {					\
			fprintf(stderr, "(%s, %d): ",			\
					__FILE__, __LINE__);		\
			perror(call_description);			\
			exit(EXIT_FAILURE);				\
		}							\
	} while (0)

/* 
 * Add your BLAS implementation here
 */
double* my_solver(int N, double *A, double *B) {
	printf("BLAS SOLVER\n");

	// calcul B x A
	// Obs. A = matrice superior triunghiulară
	double *BxA = calloc(N * N, sizeof(double));
	DIE(BxA == NULL, "BxA calloc error");

	memcpy(BxA, B, N * N * sizeof(double));

	// inițial BxA = B,
	// după efectuarea înmulțirii, BxA = B x A
	cblas_dtrmm(
		CblasRowMajor,
		// ordinea în care se înmulțesc A și B (B x A)
		CblasRight,
		// A este superior triunghiulară
		CblasUpper,
		CblasNoTrans,
		CblasNonUnit,
		// număr de linii
		N,
		// număr de coloane
		N,
		1,
		A, N,
		BxA, N
	);

	// calcul (B x A) x A_T
	// Obs. A_T = matrice inferior triunghiulară
	double *BxAxA_T;

	cblas_dtrmm(
		CblasRowMajor,
		// ordinea în care se înmulțesc B x A și A_T ((B x A) x A_T)
		CblasRight,
		// A este superior triunghiulară
		CblasUpper,
		// înmulțirea se face cu A_T
		CblasTrans,
		CblasNonUnit,
		// număr de linii
		N,
		// număr de coloane
		N,
		1,
		A, N,
		BxA, N
	);

	BxAxA_T = BxA;

	// calcul B_T x B + B x A x A_T
	cblas_dgemm(
		CblasRowMajor,
		// B_T
		CblasTrans,
		// B
		CblasNoTrans,
		N, N, N,
		1,
		B, N,
		B, N,
		1,
		BxAxA_T, N
	);

	double *C = BxAxA_T;

	return C;
}
