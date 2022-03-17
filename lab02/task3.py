"""
Coffee Factory: A multiple producer - multiple consumer approach

Generate a base class Coffee which knows only the coffee name
Create the Espresso, Americano and Cappuccino classes which inherit the base class knowing that
each coffee type has a predetermined size.
Each of these classes have a get message method

Create 3 additional classes as following:
    * Distributor - A shared space where the producers puts coffees and the consumers takes them
    * CoffeeFactory - An infinite loop, which always sends coffees to the distributor
    * User - Another infinite loop, which always takes coffees from the distributor

The scope of this exercise is to correctly use threads, classes and synchronization objects.
The size of the coffee (ex. small, medium, large) is chosen randomly everytime.
The coffee type is chosen randomly everytime.

Example of output:

Consumer 65 consumed espresso
Factory 7 produced a nice small espresso
Consumer 87 consumed cappuccino
Factory 9 produced an italian medium cappuccino
Consumer 90 consumed americano
Consumer 84 consumed espresso
Factory 8 produced a strong medium americano
Consumer 135 consumed cappuccino
Consumer 94 consumed americano
"""

from threading import Semaphore, Thread
import random

class Coffee:
    """ Base class """
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_name(self):
        """ Returns the coffee name """
        return self.name

    def get_size(self):
        """ Returns the coffee size """
        return self.size

class Espresso(Coffee):
    def __init__(self, size):
        super().__init__('espresso', size)

    def get_message(self):
        return "a nice " + self.get_size() + " " + self.get_name()

class Americano(Coffee):
    def __init__(self, size):
        super().__init__('americano', size)

    def get_message(self):
        return "a strong " + self.get_size() + " " + self.get_name()

class Cappuccino(Coffee):
    def __init__(self, size):
        super().__init__('cappuccino', size)

    def get_message(self):
        return "an italian " + self.get_size() + " " + self.get_name()

class ExampleCoffee:
    """ Espresso implementation """
    def __init__(self, size):
        pass

    def get_message(self):
        """ Output message """
        raise NotImplementedError

class Distributor:
    def __init__(self, capacity_max):
        self.capacity = capacity_max
        self.coffees = []
        self.sem_full = Semaphore(0)
        self.sem_empty = Semaphore(self.capacity)

    def status(self):
        print("Status:")
        print(self.coffees)

    def produce(self, coffee, factory):
        self.sem_empty.acquire()
        self.coffees.append(coffee)
        print("Factory %d produced %s" % (factory, coffee.get_message()))
        # print("Factory " + factory + " produced " + coffee.get_name())
        self.sem_full.release()

    def consume(self, consumer):
        self.sem_full.acquire()
        print("Consumer %d consumed %s" % (consumer, self.coffees.pop().get_name()))
        # print("Consumer " + consumer + " consumed " + self.coffees.pop().get_name())
        self.sem_empty.release()

class CoffeeFactory:
    def __init__(self, number, distributor):
        self.number = number
        self.distributor = distributor

    def do(self):
        while True:
        #for i in range(5):
            x = random.randint(1, 3)
            sz = random.randint(1, 3)
            if sz == 1:
                coffee_size = 'small'
            elif sz == 2:
                coffee_size = 'medium'
            else:
                coffee_size = 'large'
            if x == 1:
                coffee = Espresso(size=coffee_size)
            elif x == 2:
                coffee = Americano(size=coffee_size)
            else:
                coffee = Cappuccino(size=coffee_size)
            self.distributor.produce(coffee, self.number)

class User:
    def __init__(self, number, distributor):
        self.number = number
        self.distributor = distributor

    def do(self):
        while True:
        # for i in range(5):
            self.distributor.consume(self.number)

if __name__ == '__main__':
    FACTORIES = 5
    CONSUMERS = 5
    DISTRIBUTOR = Distributor(10)
    THREADS = []

    for i in range(CONSUMERS):
        cons = User(number=i, distributor=DISTRIBUTOR)
        th = Thread(target=cons.do)
        THREADS.append(th)

    for i in range(FACTORIES):
        fact = CoffeeFactory(number=i, distributor=DISTRIBUTOR)
        th = Thread(target=fact.do)
        THREADS.append(th)

    for i in range(len(THREADS)):
        THREADS[i].start()

    for i in range(len(THREADS)):
        THREADS[i].join()
