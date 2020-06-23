"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
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
        Thread.__init__(self, name=kwargs['name'], daemon=kwargs['daemon'])
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):
        producers_id = self.marketplace.register_producer()
        while True:
            for product in self.products:
                product_id = product[0]
                product_quantity = product[1]
                product_time = product[2]
                while product_quantity > 0:
                    sleep(product_time)
                    while not self.marketplace.publish(producers_id, product_id):
                        sleep(self.republish_wait_time)
                    product_quantity = product_quantity - 1
