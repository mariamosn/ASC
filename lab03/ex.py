"""
from threading import *


class SimpleBarrier():
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.count_threads = self.num_threads  # contorizeaza numarul de thread-uri ramase
        self.count_lock = Lock()  # protejeaza accesarea/modificarea contorului
        self.threads_event = Event()  # blocheaza thread-urile ajunse

    def wait(self):
        with self.count_lock:
            self.count_threads -= 1
            if self.count_threads == 0:  # a ajuns la bariera si ultimul thread
                self.threads_event.set()  # deblocheaza toate thread-urile
        self.threads_event.wait()  # num_threads-1 threaduri se blocheaza aici
        # ultimul thread nu se va bloca deoarece event-ul a fost setat


class MyThread(Thread):
    def __init__(self, tid, barrier):
        Thread.__init__(self)
        self.tid = tid
        self.barrier = barrier

    def run(self):
        print("I'm Thread " + str(self.tid) + " before\n")
        self.barrier.wait()
        print("I'm Thread " + str(self.tid) + " after barrier\n")

b = SimpleBarrier(2)
t1 = MyThread(1, b)
t2 = MyThread(2, b)

t1.start()
t2.start()

t1.join()
t2.join()

"""

"""
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from threading import current_thread
import time, random

data = ["lab1", "lab2", "lab3"]


def modify_msg(msg):
    time.sleep(random.randint(1, 5))
    return "Completed: [" + msg.title() + "] in thread " + str(current_thread())


def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(modify_msg, data)

    for result in results:
        print(result)


if __name__ == '__main__':
    main()
"""

"""
from threading import *


class SimpleBarrier():
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.count_threads = self.num_threads  # contorizeaza numarul de thread-uri ramase
        self.count_lock = Lock()  # protejeaza accesarea/modificarea contorului
        self.threads_sem = Semaphore(0)  # blocheaza thread-urile ajunse

    def wait(self):
        with self.count_lock:
            self.count_threads -= 1
            if self.count_threads == 0:  # a ajuns la bariera si ultimul thread
                for i in range(self.num_threads):
                    self.threads_sem.release()  # incrementarea semaforului va debloca num_threads thread-uri
        self.threads_sem.acquire()  # num_threads-1 threaduri se blocheaza aici
        # contorul semaforului se decrementeaza de num_threads ori


class MyThread(Thread):
    def __init__(self, tid, barrier):
        Thread.__init__(self)
        self.tid = tid
        self.barrier = barrier

    def run(self):
        print("I'm Thread " + str(self.tid) + " before\n")
        self.barrier.wait()
        print("I'm Thread " + str(self.tid) + " after barrier\n")

b = SimpleBarrier(2)
t1 = MyThread(1, b)
t2 = MyThread(2, b)

t1.start()
t2.start()

t1.join()
t2.join()
"""

"""
from threading import *


class ReusableBarrier():
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.count_threads1 = [self.num_threads]
        self.count_threads2 = [self.num_threads]
        self.count_lock = Lock()  # protejam accesarea/modificarea contoarelor
        self.threads_sem1 = Semaphore(0)  # blocam thread-urile in prima etapa
        self.threads_sem2 = Semaphore(0)  # blocam thread-urile in a doua etapa

    def wait(self):
        self.phase(self.count_threads1, self.threads_sem1)
        self.phase(self.count_threads2, self.threads_sem2)

    def phase(self, count_threads, threads_sem):
        with self.count_lock:
            count_threads[0] -= 1
            if count_threads[0] == 0:  # a ajuns la bariera si ultimul thread
                for i in range(self.num_threads):
                    threads_sem.release()  # incrementarea semaforului va debloca num_threads thread-uri
                count_threads[0] = self.num_threads  # reseteaza contorul
        threads_sem.acquire()  # num_threads-1 threaduri se blocheaza aici
        # contorul semaforului se decrementeaza de num_threads ori


class MyThread(Thread):
    def __init__(self, tid, barrier):
        Thread.__init__(self)
        self.tid = tid
        self.barrier = barrier

    def run(self):
        for i in range(10):
            self.barrier.wait()
            print("I'm Thread " + str(self.tid) + " after barrier, in step " + str(i) + "\n")

b = ReusableBarrier(2)
t1 = MyThread(1, b)
t2 = MyThread(2, b)

t1.start()
t2.start()

t1.join()
t2.join()
"""

"""
from threading import *


class ReusableBarrier():
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.count_threads = self.num_threads  # contorizeaza numarul de thread-uri ramase
        self.cond = Condition()  # blocheaza/deblocheaza thread-urile
        # protejeaza modificarea contorului

    def wait(self):
        self.cond.acquire()  # intra in regiunea critica
        self.count_threads -= 1;
        if self.count_threads == 0:
            self.cond.notify_all()  # deblocheaza toate thread-urile
            self.count_threads = self.num_threads  # reseteaza contorul
        else:
            self.cond.wait();  # blocheaza thread-ul eliberand in acelasi timp lock-ul
        self.cond.release();  # iese din regiunea critica


class MyThread(Thread):
    def __init__(self, tid, barrier):
        Thread.__init__(self)
        self.tid = tid
        self.barrier = barrier

    def run(self):
        for i in range(10):
            self.barrier.wait()
            print("I'm Thread " + str(self.tid) + " after barrier, in step " + str(i) + "\n")

b = ReusableBarrier(2)
t1 = MyThread(1, b)
t2 = MyThread(2, b)

t1.start()
t2.start()

t1.join()
t2.join()
"""
