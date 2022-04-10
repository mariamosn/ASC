"""
Maria Moșneag
333CA

This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
April 2022
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def safe_publish(self, product, producer_id):
        """
        Safe way to publish a product to the market. Try to publish and, if the
        operation fails, wait and try again after a specified time.

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace
        """
        while not self.marketplace.publish(producer_id, product):
            sleep(self.republish_wait_time)

    def run(self):
        my_id = self.marketplace.register_producer()

        while True:
            for (id_prod, quantity_prod, wait_time_prod) in self.products:
                sleep(wait_time_prod)

                for _ in range(quantity_prod):
                    self.safe_publish(id_prod, my_id)
