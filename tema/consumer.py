"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
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
        :param retry_wait_time: the number of seconds that a consumer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, name=kwargs['name'])
        self.marketplace = marketplace
        self.carts = carts
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            carts_id = self.marketplace.new_cart()
            for cart_entry in cart:
                cart_entry_type = cart_entry['type']
                cart_entry_quantity = cart_entry['quantity']
                cart_entry_product = cart_entry['product']
                if cart_entry_type == 'add':
                    while cart_entry_quantity > 0:
                        while not self.marketplace.add_to_cart(carts_id, cart_entry_product):
                            sleep(self.retry_wait_time)
                        cart_entry_quantity = cart_entry_quantity - 1
                elif cart_entry_type == 'remove':
                    while cart_entry_quantity > 0:
                        self.marketplace.remove_from_cart(carts_id, cart_entry_product)
                        cart_entry_quantity = cart_entry_quantity - 1
            products = self.marketplace.place_order(carts_id)
            for product in products:
                print('{} bought {}'.format(self.name, product))
