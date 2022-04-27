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
 * Add your BLAS implementation here
 */
double* my_solver(int N, double *A, double *B) {
	printf("BLAS SOLVER\n");
	return NULL;
}
