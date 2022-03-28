import concurrent.futures
import random
from threading import *
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

dna_options = ['A', 'T', 'G', 'C']
dna_samples = []
dna_chosen = []
subseq = []

random.seed(1)


def setup():
    for i in range(100):
        dna_seq = []
        for j in range(10000):
            seq = random.choice(dna_options)
            dna_seq.append(seq)
        dna_samples.append(dna_seq)

    aux = dna_samples[random.randint(0, 99)]
    start = random.randint(0, 9989)

    for i in range(10):
        subseq.append(aux[start + i])


def work(index):
    sample = dna_samples[index]
    # print(sample)
    for i in range(9989):
        ok = 1
        for j in range(10):
            if sample[i + j] != subseq[j]:
                ok = 0
                break
        if ok == 1:
            return "DNA sequence found in sample " + str(index)
    return "Missing"


def main():
    setup()

    with ThreadPoolExecutor(max_workers=30) as executor:
        results = []
        for i in range(100):
            results.append(executor.submit(work, index=i))
        #results = executor.map(work, dna_samples)

    for result in concurrent.futures.as_completed(results):
        print(result.result())


if __name__ == '__main__':
    main()
