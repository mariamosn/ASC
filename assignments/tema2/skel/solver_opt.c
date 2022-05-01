/*
 * Tema 2 ASC
 * 2022 Spring
 * Maria Moșneag
 * 333CA
 */
#include "utils.h"
#include <stdio.h>
#include <string.h>

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
 * Implementarea optimizată.
 */
double* my_solver(int N, double *A, double* B) {
	printf("OPT SOLVER\n");

	int blockSize = 50;


	// calcul B x A
	// Obs. A = matrice superior triunghiulară
	double *BxA = calloc(N * N, sizeof(double));
	DIE(BxA == NULL, "BxA calloc error");

	for (register int bi = 0; bi < N; bi += blockSize) {
		double *orig_orig_pBxA = &BxA[bi * N];
		double *orig_orig_pB = &B[bi * N];

        for (register int bj = 0; bj < N; bj += blockSize) {
			register double *orig_pBxA = orig_orig_pBxA + bj;

            for (register int bk = 0; bk <= bj; bk += blockSize) {
				register double *orig_pB = orig_orig_pB + bk;
				register double *pA = &A[bk * N + bj];

                for (register int k = 0; k < blockSize; k++) {
					register double *pBxA = orig_pBxA;
					register double *pB = orig_pB + k;

                    for (register int i = 0; i < blockSize; i++) {

                        for (register int j = 0; j < blockSize; j += 10) {
                            // BxA[(bi + i) * N + (bj + j)] += B[(bi + i) * N + (bk + k)] * A[(bk + k) * N + (bj + j)];
							// loop unrolling
							*pBxA += *pB * *pA;
							pBxA++;
							pA++;

							*pBxA += *pB * *pA;
							pBxA++;
							pA++;

							*pBxA += *pB * *pA;
							pBxA++;
							pA++;

							*pBxA += *pB * *pA;
							pBxA++;
							pA++;

							*pBxA += *pB * *pA;
							pBxA++;
							pA++;

							*pBxA += *pB * *pA;
							pBxA++;
							pA++;

							*pBxA += *pB * *pA;
							pBxA++;
							pA++;

							*pBxA += *pB * *pA;
							pBxA++;
							pA++;

							*pBxA += *pB * *pA;
							pBxA++;
							pA++;

							*pBxA += *pB * *pA;
							pBxA++;
							pA++;
						}
						pBxA += N - blockSize;
						pB += N;
						pA -= blockSize;
					}
					pA += N;
				}
			}
		}
	}


	// calcul (B x A) x A_T
	// Obs. A_T = matrice inferior triunghiulară
	// Obs. A_T[i][j] = A[j][i]
	double *BxAxA_T = calloc(N * N, sizeof(double));
	DIE(BxAxA_T == NULL, "BxAxA_T calloc error");

	for (register int bi = 0; bi < N; bi += blockSize) {
		double *orig_orig_pBxAxA_T = &BxAxA_T[bi * N];
		double *orig_orig_pBxA = &BxA[bi * N];

        for (register int bj = 0; bj < N; bj += blockSize) {
			register double *orig_pBxAxA_T = orig_orig_pBxAxA_T + bj;
			register double *orig_orig_pA_T = &A[bj * N];

            for (register int bk = bj; bk < N; bk += blockSize) {
				register double *orig_pBxA = orig_orig_pBxA + bk;
				register double *orig_pA_T = orig_orig_pA_T + bk;

                for (register int k = 0; k < blockSize; k++) {
					register double *pBxAxA_T = orig_pBxAxA_T;
					register double *pBxA = orig_pBxA + k;

                    for (register int i = 0; i < blockSize; i++) {
						register double *pA_T = orig_pA_T + k;

                        for (register int j = 0; j < blockSize; j += 2) {
							// BxAxA_T[(bi + i) * N + bj + j] += BxA[(bi + i) * N + bk + k] * A[(bj + j) * N + bk + k];
							// loop unrolling
							*pBxAxA_T += *pBxA * *pA_T;
							pBxAxA_T++;
							pA_T += N;

							*pBxAxA_T += *pBxA * *pA_T;
							pBxAxA_T++;
							pA_T += N;
						}
						pBxAxA_T += N - blockSize;
						pBxA += N;
					}
				}
			}
		}
	}


	// calcul B_T x B
	// Obs. B_T[i][j] = B[j][i]
	double *B_TxB = BxA;
	memset(B_TxB, 0, N * N * sizeof(double));

	for (register int bk = 0; bk < N; bk += blockSize) {

		for (register int bi = 0; bi < N; bi += blockSize) {
			double *orig_orig_pB_TxB = &B_TxB[bi * N];

			for (register int bj = 0; bj < N; bj += blockSize) {
			register double *orig_pB_TxB = orig_orig_pB_TxB + bj;

                for (register int k = 0; k < blockSize; k++) {
					register double *pB_TxB = orig_pB_TxB;
					register double *pB = &B[(bk + k) * N];
					register double *pB_T = pB + bi;
					pB += bj;

                    for (register int i = 0; i < blockSize; i++) {

                        for (register int j = 0; j < blockSize; j++) {
							// B_TxB[(bi + i) * N + bj + j] += B[(bk + k) * N + bi + i] * B[(bk + k) * N + bj + j];
							// loop unrolling
							*pB_TxB += *pB_T * pB[j];
							pB_TxB++;
							j++;

							*pB_TxB += *pB_T * pB[j];
							pB_TxB++;
							j++;

							*pB_TxB += *pB_T * pB[j];
							pB_TxB++;
							j++;

							*pB_TxB += *pB_T * pB[j];
							pB_TxB++;
							j++;

							*pB_TxB += *pB_T * pB[j];
							pB_TxB++;
						}
						pB_TxB += N - blockSize;
						pB_T++;
					}
				}
			}
		}
	}


	// calcul B x A x A_T + B_T x B
	double *C = BxAxA_T;

	register double *pC = C;
	register double *pB_TxB = B_TxB;
	for (register int i = 0; i < N * N; i++) {
		*pC += *pB_TxB;
		pC++;
		pB_TxB++;
	}

	free(B_TxB);

	return C;	
}
