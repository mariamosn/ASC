===== Exercitii =====

**Task 0**  - Folosit valgrind pentru ''task0.c'' urmarind TODO-uri pentru teste.
    * ''make task0'' pentru versiunea seriala
    * ''make openmp_task0'' pentru versiunea paralelizata
    * <code sh>
[@fep7-1 ]$ srun --x11 -p hpsl--pty /bin/bash
[@hpsl-wn01 ~]$ singularity run docker://gitlab.cs.pub.ro:5050/asc/asc-public/c-labs:1.3.1 /bin/bash
Singularity> make task0
Singularity> valgrind --tool=callgrind -v --dump-every-bb=10000000 ./task0
Singularity> kcachegrind 
Singularity> make clean
Singularity> make openmp_task0
Singularity> valgrind --tool=callgrind -v --dump-every-bb=10000000 ./task0
Singularity> kcachegrind 
</code>

**Task 1**  - Analizati aplicatia Tachyon.
    * Rulati scriptul ''task1.sh'' pentru a descarca si compila Tachyon.
    * Varianta seriala ''tachyon_find_hotspots''
    * Varianta paralelizata ''tachyon_analyze_locks''
    * <code sh>
[@fep7-1 ]$ srun --x11 -p hpsl--pty /bin/bash
[@hpsl-wn01 ~]$ singularity run docker://gitlab.cs.pub.ro:5050/asc/asc-public/c-labs:1.3.1 /bin/bash
Singularity> ./task1.sh
Singularity> cd tachyon
Singularity> valgrind --tool=callgrind --collect-jumps=yes --dump-instr=yes --collect-systime=yes -- ./tachyon_find_hotspots dat/balls.dat
Singularity> valgrind --tool=callgrind --collect-jumps=yes --dump-instr=yes --collect-systime=yes -- ./tachyon_analyze_locks dat/balls.dat
</code>
    * Analizati cu perf


**Task 2**  - Folositi tool-ul cachegrind din valgrind pentru a analiza codul care realizeaza inmultirea de matrice folosind diferite reordonari ale buclelor.
    * Compilati si rulati ''task2.c''
    * Notati observatiile voastre legate de numarul de I refs, D refs, D1 misses, branches si mispredicts.
    * <code sh>
[@fep7-1 ]$ srun --x11 -p hpsl--pty /bin/bash
[@hpsl-wn01 ~]$ singularity run docker://gitlab.cs.pub.ro:5050/asc/asc-public/c-labs:1.3.1 /bin/bash
Singularity> make task2
Singularity> valgrind --tool=cachegrind --branch-sim=yes ./mult_reorder 1
Singularity> valgrind --tool=cachegrind --branch-sim=yes ./mult_reorder 2
Singularity> valgrind --tool=cachegrind --branch-sim=yes ./mult_reorder 3
</code>