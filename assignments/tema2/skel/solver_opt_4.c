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

	// int blockSize = 100;

	// calcul B x A
	// Obs. A = matrice superior triunghiulară
	double *BxA = calloc(N * N, sizeof(double));
	DIE(BxA == NULL, "BxA calloc error");
/*
	for (int bi = 0; bi < N; bi += blockSize)
        for (int bj = 0; bj < N; bj += blockSize)
            for (int bk = 0; bk < N; bk += blockSize) {
                for (int i = 0; i < blockSize; i++) {
                    for (int j = 0; j < blockSize; j++) {
                        for (int k = 0; k < blockSize; k++) {
                            BxA[(bi + i) * N + (bj + j)] += B[(bi + i) * N + (bk + k)] * A[(bk + k) * N + (bj + j)];
						}
					}
				}
			}
*/

	register double *pBxA = BxA;
	for (register int i = 0; i < N; i++) {
		register double *orig_pB = &B[i * N];
		for (register int j = 0; j < N; j++) {
			register double *pB = orig_pB;
			register double *pA = &A[j];
			register double sum = 0.0;
			for (register int k = 0; k <= j; k++) {
				// sum += B[i * N + k] * A[k * N + j];
				sum += *pB * *pA;
				pB++;
				pA += N;
			}
			// BxA[ixN + j] = sum;
			*pBxA = sum;
			pBxA++;
		}
	}

	// calcul (B x A) x A_T
	// Obs. A_T = matrice inferior triunghiulară
	// Obs. A_T[i][j] = A[j][i]
	double *BxAxA_T = calloc(N * N, sizeof(double));
	DIE(BxAxA_T == NULL, "BxAxA_T calloc error");

	register double *pBxAxA_T = BxAxA_T;
	for (register int i = 0; i < N; i++) {
		register double *orig_pBxA = &BxA[i * N];
		for (register int j = 0; j < N; j++) {
			register double *pBxA = orig_pBxA + j;
			register double *pA = &A[j * N + j];
			register double sum = 0.0;
			// register int jxN = j * N;
			for (register int k = j; k < N; k++) {
				// sum += BxA[ixN + k] * A[jxN + k];
				sum += *pBxA * *pA;
				pBxA++;
				pA++;
			}
			// BxAxA_T[ixN + j] = sum;
			*pBxAxA_T = sum;
			pBxAxA_T++;
		}
	}

	free(BxA);

	// calcul B_T x B
	// Obs. B_T[i][j] = B[j][i]
	double *B_TxB = calloc(N * N, sizeof(double));
	DIE(B_TxB == NULL, "B_TxB calloc error");

	register double *pB_TxB = B_TxB;
	for (register int i = 0; i < N; i++) {
		register double *orig_pB_T = &B[i];
		for (register int j = 0; j < N; j++) {
			register double *pB_T = orig_pB_T;
			register double *pB = &B[j];
			register double sum = 0.0;
			for (register int k = 0; k < N; k++) {
				// B_T este B parcurs pe coloane
				// sum += B[k * N + i] * B[k * N + j];
				sum += *pB_T * *pB;
				pB_T += N;
				pB += N;
			}
			// B_TxB[ixN + j] = sum;
			*pB_TxB = sum;
			pB_TxB++;
		}
	}

	// calcul B x A x A_T + B_T x B
	double *C = BxAxA_T;

	register double *pC = C;
	pB_TxB = B_TxB;
	for (register int i = 0; i < N * N; i++) {
		*pC += *pB_TxB;
		pC++;
		pB_TxB++;
	}

	free(B_TxB);

	return C;	
}
