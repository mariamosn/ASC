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
 * Add your unoptimized implementation here
 */

double* my_solver(int N, double *A, double* B) {

	printf("NEOPT SOLVER\n");

	// calcul B x A
	// Obs. A = matrice superior triunghiulară
	double *BxA = calloc(N * N, sizeof(double));
	DIE(BxA == NULL, "BxA calloc error");

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			for (int k = 0; k <= j; k++) {
				BxA[i * N + j] += B[i * N + k] * A[k * N + j];
			}
		}
	}

	// calcul (B x A) x A_T
	// Obs. A_T = matrice inferior triunghiulară
	// Obs. A_T[i][j] = A[j][i]
	double *BxAxA_T = calloc(N * N, sizeof(double));
	DIE(BxAxA_T == NULL, "BxAxA_T calloc error");

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			for (int k = j; k < N; k++) {
				BxAxA_T[i * N + j] += BxA[i * N + k] * A[j * N + k];
			}
		}
	}

	free(BxA);

	// calcul B_T x B
	// Obs. B_T[i][j] = B[j][i]
	double *B_TxB = calloc(N * N, sizeof(double));
	DIE(B_TxB == NULL, "B_TxB calloc error");

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			for (int k = 0; k < N; k++) {
				// B_T este B parcurs pe coloane
				B_TxB[i * N + j] += B[k * N + i] * B[k * N + j];
			}
		}
	}

	// calcul B x A x A_T + B_T x B
	double *C = BxAxA_T;

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			C[i * N + j] += B_TxB[i * N + j];
		}
	}

	free(B_TxB);

	return C;
}


/* super basic
double* my_solver(int N, double *A, double* B) {

	printf("NEOPT SOLVER\n");

	// calcul B x A
	// Obs. A = matrice superior triunghiulară
	double *BxA = calloc(N * N, sizeof(double));
	DIE(BxA == NULL, "BxA calloc error");

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			BxA[i * N + j] = 0;
			for (int k = 0; k < N; k++) {
				BxA[i * N + j] += B[i * N + k] * A[k * N + j];
			}
		}
	}

	// calcul A_T, B_T
	double *A_T = calloc(N * N, sizeof(double));
	DIE(A_T == NULL, "A_T calloc error");
	double *B_T = calloc(N * N, sizeof(double));
	DIE(B_T == NULL, "B_T calloc error");

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			A_T[i * N + j] = A[j * N + i];
			B_T[i * N + j] = B[j * N + i];
		}
	}

	// calcul (B x A) x A_T
	// Obs. A_T = matrice inferior triunghiulară
	double *BxAxA_T = calloc(N * N, sizeof(double));
	DIE(BxAxA_T == NULL, "BxAxA_T calloc error");

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			BxAxA_T[i * N + j] = 0;
			for (int k = 0; k < N; k++) {
				BxAxA_T[i * N + j] += BxA[i * N + k] * A_T[k * N + j];
			}
		}
	}

	// calcul B_T x B
	double *B_TxB = calloc(N * N, sizeof(double));
	DIE(B_TxB == NULL, "B_TxB calloc error");

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			B_TxB[i * N + j] = 0;
			for (int k = 0; k < N; k++) {
				// B_T este B parcurs pe coloane
				B_TxB[i * N + j] += B_T[i * N + k] * B[k * N + j];
			}
		}
	}

	// calcul B x A x A_T + B_T x B
	double *C = BxAxA_T;

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			C[i * N + j] += B_TxB[i * N + j];
		}
	}

	free(BxA);
	free(A_T);
	free(B_T);
	free(B_TxB);

	return C;
}
*/