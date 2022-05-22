#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include "helper.h"

using namespace std;

__global__ void accessiblePopulation(const int n, float *lats, float *lons,
                                    int *pops, int *res, const float kmRange) {
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

    float *host_lats = 0;
    float *host_lons = 0;
    int *host_pops = 0;
    int *host_res = 0;

    float *device_lats = 0;
    float *device_lons = 0;
    int *device_pops = 0;
    int *device_res = 0;

    int n = countLines(fileIn);
    int i = 0;

    if (n > 200000)
        return;

    ifstream ifs(fileIn);
    ofstream ofs(fileOut);

    host_lats = (float *) malloc(n * sizeof(float));
    host_lons = (float *) malloc(n * sizeof(float));
    host_pops = (int *) malloc(n * sizeof(int));
    host_res = (int *) malloc(n * sizeof(int));

    cudaMalloc((void **) &device_lats, n * sizeof(float));
    cudaMalloc((void **) &device_lons, n * sizeof(float));
    cudaMalloc((void **) &device_pops, n * sizeof(int));
    cudaMalloc((void **) &device_res, n * sizeof(int));

    DIE(host_lats == 0 || host_lons == 0 ||
        host_pops == 0 || host_res == 0 ||
        device_lats == 0 || device_lons == 0 ||
        device_pops == 0 || device_res == 0,
        "malloc failed");

    while(ifs >> geon >> host_lats[i] >> host_lons[i] >> host_pops[i]) {
        host_res[i] = host_pops[i];
        i++;
    }

    n = i;

    cudaMemcpy(device_lats, host_lats, n * sizeof(float),
                cudaMemcpyHostToDevice);
    cudaMemcpy(device_lons, host_lons, n * sizeof(float),
                cudaMemcpyHostToDevice);
    cudaMemcpy(device_pops, host_pops, n * sizeof(int),
                cudaMemcpyHostToDevice);
    cudaMemcpy(device_res, host_res, n * sizeof(int),
                cudaMemcpyHostToDevice);

    int blockSize = 256;
    int numBlocks = n / blockSize;
    if (n % blockSize) {
        numBlocks++;
    }
    accessiblePopulation<<<numBlocks, blockSize>>>(n, device_lats, device_lons,
                                                    device_pops, device_res,
                                                    kmRange);

    cudaDeviceSynchronize();

    cudaMemcpy(host_res, device_res, n * sizeof(int),
    cudaMemcpyDeviceToHost);

    for (i = 0; i < n; i++) {
        ofs << host_res[i] << endl;
    }

    free(host_lats);
    free(host_lons);
    free(host_pops);
    free(host_res);

    cudaFree(device_lats);
    cudaFree(device_lons);
    cudaFree(device_pops);
    cudaFree(device_res);

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
