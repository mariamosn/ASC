"""
    Basic thread handling exercise:

    Use the Thread class to create and run more than 10 threads which print their name and a random
    number they receive as argument. The number of threads must be received from the command line.

    e.g. Hello, I'm Thread-96 and I received the number 42

"""

from threading import Thread
import sys
import random


def my_concurrent_code(nr, my_nr):
    """ Functie care va fi rulata concurent """
    # print("Hello, I'm Thread-", nr, " and I received the number ", my_nr)
    print("Hello, I'm Thread-%d and I received the number %d." % (nr, my_nr))


# creeaza obiectele corespunzatoare thread-urilor
nr_threads = int(sys.stdin.readline().strip("\n"))
l = []
for i in range(nr_threads):
    t = Thread(target=my_concurrent_code, args=(i, random.randint(0, 100)))
    t.start()
    l.append(t)

for i in range(nr_threads):
    l[i].join()
