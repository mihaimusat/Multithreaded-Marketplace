"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Lock

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

        self.carts = {}
        self.carts_id = 0
        self.carts_lock = Lock()

        self.producers = {}
        self.producers_id = 0
        self.producers_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producers_lock.acquire()
        self.producers_id = self.producers_id + 1
        producer_id = self.producers_id
        self.producers[producer_id] = []
        self.producers_lock.release()
        return self.producers_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        products = self.producers[producer_id]
        if len(products) < self.queue_size_per_producer:
            products.append(product)
        else:
            return False
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.carts_lock.acquire()
        self.carts_id = self.carts_id + 1
        cart_id = self.carts_id
        self.carts[cart_id] = []
        self.carts_lock.release()
        return self.carts_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for producer_id in self.producers:
            products = self.producers[producer_id]
            if product not in products:
                continue
            if product in products:
                self.carts[cart_id].append((producer_id, product))
                self.producers[producer_id].remove(product)
                return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        for producer_id, product_name in self.carts[cart_id]:
            if product != product_name:
                continue
            if product == product_name:
                self.carts[cart_id].remove((producer_id, product_name))
                self.producers[producer_id].append(product)
                break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        products = [product_name for producer_id, product_name in self.carts[cart_id]]
        return products
