from threading import *

class Master(Thread):
    def __init__(self, max_work, available):
        Thread.__init__(self, name = "Master")
        self.max_work = max_work
        self.available = available
    
    def set_worker(self, worker):
        self.worker = worker
    
    def run(self):
        for i in range(self.max_work):
            with self.available:
                # generate work
                self.work = i
                print("master worked")
                self.available.notify_all()
                # get result
                self.available.wait()
                if self.get_work() + 1 != self.worker.get_result():
                    print ("oops")
                print ("%d -> %d" % (self.work, self.worker.get_result()))

    def get_work(self):
        return self.work

class Worker(Thread):
    def __init__(self, terminate, available):
        Thread.__init__(self, name = "Worker")
        self.terminate = terminate
        self.available = available

    def set_master(self, master):
        self.master = master
    
    def run(self):
        while(True):
            with self.available:
                # wait work
                self.available.wait()
                print("worker working")
                if (terminate.is_set()): break
                # generate result
                self.result = self.master.get_work() + 1
                # notify master
                self.available.notify_all()
    
    def get_result(self):
        return self.result

if __name__ ==  "__main__":
    # create shared objects
    terminate = Event()
    available = Condition()
    
    # start worker and master
    w = Worker(terminate, available)
    m = Master(10, available)
    w.set_master(m)
    m.set_worker(w)
    w.start()
    m.start()

    # wait for master
    m.join()

    # wait for worker
    terminate.set()
    print("should be done")
    with available:
        available.notify_all()
    w.join()

    # print running threads for verification
    print(enumerate())

