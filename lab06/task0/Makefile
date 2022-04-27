COMPILER=gcc
CFLAGS  = -std=c99 -g -Wall -O0
OPTIMIZE_FLAGS = -std=c99 -Wall -O3
OPENMP_FLAGS = -std=c99 -g -Wall -O0 -fopenmp
LDLIBS  = -lm

%: %.c
	$(COMPILER) $(CFLAGS) $^ -o $@ $(LDLIBS)

optimize_%: %.c
	$(COMPILER) $(OPTIMIZE_FLAGS) $^ -o $* $(LDLIBS)

openmp_%: %.c
	$(COMPILER) $(OPENMP_FLAGS) $^ -o $* $(LDLIBS)

clean:
	rm -rf task0
	rm -f callgrind.out.*
