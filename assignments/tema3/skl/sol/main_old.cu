#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include "helper.h"

using namespace std;

__global__ void accessiblePopulation(int n, float *lats, float *lons,
                                    int *pops, int *res, float kmRange) {
    register unsigned int index = threadIdx.x + blockDim.x * blockIdx.x;
    register float crt_lat = lats[index];
    register float crt_lon = lons[index];
    register int crt_pop = pops[index];

    for (register int i = index + 1; i < n; i++) {
        float phi1 = (90.f - crt_lat) * DEGREE_TO_RADIANS;
        float phi2 = (90.f - lats[i]) * DEGREE_TO_RADIANS;

        float theta1 = crt_lon * DEGREE_TO_RADIANS;
        float theta2 = lons[i] * DEGREE_TO_RADIANS;

        float cs = sin(phi1) * sin(phi2) * cos(theta1 - theta2) +
                    cos(phi1) * cos(phi2);
        if (cs > 1) {
            cs = 1;
        } else if (cs < -1) {
            cs = -1;
        }

        float dist = 6371.f * acos(cs);

        if (dist <= kmRange) {
            // res[index] += pops[i];
            // res[i] += crt_pop;
            atomicAdd(&res[index], pops[i]);
            atomicAdd(&res[i], crt_pop);
        }
    }
}

int countLines(const char* fileIn)
{
    register int cnt = 0;
    register string line;

    register ifstream ifs(fileIn);

    while(getline(ifs, line)) {
        cnt++;
    }

    ifs.close();

    return cnt;
}

void compute(float kmRange, const char* fileIn, const char* fileOut) {
    string geon;
    float lat;
    float *lats;
    float lon;
    float *lons;
    int pop;
    int *pops;
    int *res;

    int n = countLines(fileIn);
    int i = 0;

    ifstream ifs(fileIn);
    ofstream ofs(fileOut);

    cudaMallocManaged(&lats, n * sizeof(float));
    cudaMallocManaged(&lons, n * sizeof(float));
    cudaMallocManaged(&pops, n * sizeof(int));
    cudaMallocManaged(&res, n * sizeof(int));

    while(ifs >> geon >> lat >> lon >> pop) {
        lats[i] = lat;
        lons[i] = lon;
        pops[i] = pop;
        res[i] = pop;
        i++;
    }

    n = i;

    int blockSize = 256;
    int numBlocks = (n + blockSize - 1) / blockSize;
    accessiblePopulation<<<numBlocks, blockSize>>>(n, lats, lons, pops, res,
                                                    kmRange);

    cudaDeviceSynchronize();

    for (i = 0; i < n; i++) {
        ofs << res[i] << endl;
    }

    cudaFree(lats);
    cudaFree(lons);
    cudaFree(pops);
    cudaFree(res);

    ifs.close();
    ofs.close();
}

int main(int argc, char** argv) {
    DIE( argc == 1,
         "./accpop <kmrange1> <file1in> <file1out> ...");
    DIE( (argc - 1) % 3 != 0,
         "./accpop <kmrange1> <file1in> <file1out> ...");

    for(int argcID = 1; argcID < argc; argcID += 3) {
        float kmRange = atof(argv[argcID]);
        compute(kmRange, argv[argcID + 1], argv[argcID + 2]);
    }
}
