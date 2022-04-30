/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"

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
 * Add your optimized implementation here
 */
double* my_solver(int N, double *A, double* B) {
	printf("OPT SOLVER\n");

	// calcul B x A
	// Obs. A = matrice superior triunghiulară
	double *BxA = calloc(N * N, sizeof(double));
	DIE(BxA == NULL, "BxA calloc error");

	for (int i = 0; i < N; i++) {
		register int ixN = i * N;
		for (int j = 0; j < N; j++) {
			register double sum = 0.0;
			for (int k = 0; k <= j; k++) {
				sum += B[ixN + k] * A[k * N + j];
			}
			BxA[ixN + j] = sum;
		}
	}

	// calcul (B x A) x A_T
	// Obs. A_T = matrice inferior triunghiulară
	// Obs. A_T[i][j] = A[j][i]
	double *BxAxA_T = calloc(N * N, sizeof(double));
	DIE(BxAxA_T == NULL, "BxAxA_T calloc error");

	for (int i = 0; i < N; i++) {
		register int ixN = i * N;
		for (int j = 0; j < N; j++) {
			register double sum = 0.0;
			register int jxN = j * N;
			for (int k = j; k < N; k++) {
				sum += BxA[ixN + k] * A[jxN + k];
			}
			BxAxA_T[ixN + j] = sum;
		}
	}

	free(BxA);

	// calcul B_T x B
	// Obs. B_T[i][j] = B[j][i]
	double *B_TxB = calloc(N * N, sizeof(double));
	DIE(B_TxB == NULL, "B_TxB calloc error");

	for (int i = 0; i < N; i++) {
		register int ixN = i * N;
		for (int j = 0; j < N; j++) {
			register double sum = 0.0;
			for (int k = 0; k < N; k++) {
				// B_T este B parcurs pe coloane
				sum += B[k * N + i] * B[k * N + j];
			}
			B_TxB[ixN + j] = sum;
		}
	}

	// calcul B x A x A_T + B_T x B
	double *C = BxAxA_T;

	for (int i = 0; i < N; i++) {
		register int ixN = i * N;
		for (int j = 0; j < N; j++) {
			C[ixN + j] += B_TxB[ixN + j];
		}
	}

	free(B_TxB);

	return C;	
}
