"""
Maria Moșneag
333CA

This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
April 2022
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

    def safe_add_to_cart(self, cart_id, product):
        """
        Safe way to add a product to the cart. Try to add and, if the operation
        fails, wait and try again after a specified time.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart
        """
        while not self.marketplace.add_to_cart(cart_id, product):
            sleep(self.retry_wait_time)

    def run(self):
        for cart in self.carts:
            my_cart = self.marketplace.new_cart()

            for crt_op in cart:
                if crt_op["type"] == "add":
                    for _ in range(crt_op["quantity"]):
                        self.safe_add_to_cart(my_cart, crt_op["product"])
                elif crt_op["type"] == "remove":
                    for _ in range(crt_op["quantity"]):
                        self.marketplace.remove_from_cart(my_cart, crt_op["product"])
                else:
                    print("[Error] No such operation")

            ordered_prods = self.marketplace.place_order(my_cart)
            for prod in ordered_prods:
                self.marketplace.print_lock.acquire()
                print(self.name, "bought", prod)
                self.marketplace.print_lock.release()
