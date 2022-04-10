"""
Maria Moșneag
333CA

This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
April 2022
"""
import time
import unittest
from threading import Lock
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    handlers=[RotatingFileHandler('./marketplace.log', maxBytes=2000, backupCount=5)],
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(funcName)s:%(lineno)d] %(message)s"
)
logging.Formatter.converter = time.gmtime

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.next_cart_id = 0
        self.next_producer_id = 0
        self.producers = {}
        self.carts = {}
        self.producers_stock = {}

        self.producer_reg_lock = Lock()
        self.new_cart_lock = Lock()
        self.products_lock = Lock()
        self.print_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        logging.info('register_producer was called')
        self.producer_reg_lock.acquire()
        new_producer_id = str(self.next_producer_id)
        self.next_producer_id = self.next_producer_id + 1
        self.producer_reg_lock.release()

        self.producers[new_producer_id] = []
        self.producers_stock[new_producer_id] = 0

        logging.info("register_producer done: id = %s", new_producer_id)
        return new_producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        logging.info("publish was called: producer_id = %s; \
                    prod = %s", producer_id, str(product))

        if self.producers_stock[producer_id] >= self.queue_size_per_producer:
            logging.info("publish done")
            return False

        self.producers[producer_id].append(product)
        self.producers_stock[producer_id] = self.producers_stock[producer_id] + 1

        logging.info("publish done")
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        logging.info("new_cart was called")
        self.new_cart_lock.acquire()
        my_id = self.next_cart_id
        self.next_cart_id = self.next_cart_id + 1
        self.new_cart_lock.release()

        self.carts[my_id] = []
        logging.info("new_cart done: id = %s", str(my_id))
        return my_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        logging.info("add_to_cart was called: cart_id = %s; \
                    prod = %s", str(cart_id), str(product))
        if cart_id not in self.carts:
            return False

        self.products_lock.acquire()
        for producer in self.producers:
            for crt_prod in self.producers[producer]:
                if crt_prod == product:
                    self.carts[cart_id].append((product, producer))
                    self.producers[producer].remove(crt_prod)
                    self.products_lock.release()
                    logging.info("add_to_cart done: True")
                    return True
        self.products_lock.release()
        logging.info("add_to_cart done: False")
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        logging.info("remove_from_cart was called: cart_id = %s; \
                        product = %s", str(cart_id), str(product))
        if cart_id not in self.carts:
            logging.info("remove_from_cart done")
            return

        for (prod, producer) in self.carts[cart_id]:
            if prod == product:
                self.products_lock.acquire()
                self.producers[producer].append(prod)
                self.products_lock.release()
                self.carts[cart_id].remove((prod, producer))
                break
        logging.info("remove_from_cart done")

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        logging.info("place_order called")
        result = []

        if cart_id not in self.carts:
            logging.info("place_order done: %s", result)
            return result

        for (prod, producer) in self.carts[cart_id]:
            result.append(prod)
            self.products_lock.acquire()
            self.producers_stock[producer] = self.producers_stock[producer] - 1
            self.products_lock.release()

        logging.info("place_order done: %s", result)
        return result

class TestMarketplace(unittest.TestCase):
    """
    Unittest class
    """
    def setUp(self):
        """
        Setup for testing.
        """
        self.marketplace = Marketplace(2)

    def test_register_producer(self):
        """
        Test register_producer method.
        """
        for i in range(1000):
            self.assertEqual(self.marketplace.register_producer(), str(i))

    def test_publish(self):
        """
        Test publish method.
        """
        self.marketplace.register_producer()
        for i in range(2):
            self.assertEqual(self.marketplace.publish("0", str(i)), True)
        for i in range(2):
            self.assertEqual(self.marketplace.publish("0", str(i)), False)

        self.marketplace.register_producer()
        for i in range(2):
            self.assertEqual(self.marketplace.publish("1", str(i)), True)
        for i in range(2):
            self.assertEqual(self.marketplace.publish("1", str(i)), False)

    def test_new_cart(self):
        """
        Test new_cart method.
        """
        for i in range(1000):
            self.assertEqual(self.marketplace.new_cart(), i)

    def test_add_to_cart(self):
        """
        Test add_to_cart method.
        """
        for i in range(10):
            self.assertEqual(self.marketplace.new_cart(), i)
            self.assertEqual(self.marketplace.register_producer(), str(i))
        for i in range(10):
            self.assertEqual(self.marketplace.publish(str(i), str(i + 1000)), True)
        for i in range(10):
            self.assertEqual(self.marketplace.add_to_cart(i, str(i + 1000)), True)
        for i in range(10):
            self.assertEqual(self.marketplace.add_to_cart(i, str(i + 1000)), False)

    def test_remove_from_cart(self):
        """
        Test remove_from_cart method.
        """
        self.assertEqual(self.marketplace.new_cart(), 0)
        self.assertEqual(self.marketplace.register_producer(), "0")
        self.assertEqual(self.marketplace.publish("0", "00"), True)
        self.assertEqual(self.marketplace.publish("0", "01"), True)
        self.assertEqual(self.marketplace.add_to_cart(0, "00"), True)
        self.assertEqual(self.marketplace.add_to_cart(0, "01"), True)
        self.assertEqual(self.marketplace.add_to_cart(0, "00"), False)
        self.marketplace.remove_from_cart(0, "00")
        self.assertEqual(self.marketplace.add_to_cart(0, "00"), True)

    def test_place_order(self):
        """
        Test place_order method.
        """
        self.assertEqual(self.marketplace.new_cart(), 0)
        self.assertEqual(self.marketplace.register_producer(), "0")
        self.assertEqual(self.marketplace.publish("0", "00"), True)
        self.assertEqual(self.marketplace.publish("0", "01"), True)
        self.assertEqual(self.marketplace.add_to_cart(0, "00"), True)
        self.assertEqual(self.marketplace.add_to_cart(0, "01"), True)
        self.marketplace.remove_from_cart(0, "01")
        self.marketplace.remove_from_cart(0, "02")
        self.assertEqual(self.marketplace.add_to_cart(0, "00"), False)
        self.marketplace.remove_from_cart(0, "00")
        self.assertEqual(self.marketplace.add_to_cart(0, "01"), True)
        self.assertEqual(self.marketplace.add_to_cart(0, "00"), True)
        self.assertEqual(self.marketplace.place_order(0), ["01", "00"])
