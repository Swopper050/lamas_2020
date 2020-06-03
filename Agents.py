#!/usr/bin/env python
# coding: utf-8

import numpy as np
from random import seed
from random import randint

seed(1)

class Agent:
    def __init__(self, vector_prices, config):
        self.possible_prices = vector_prices ## Al the prices the agent consider possible.
        self.sharing_knowledge = [-1, -1] ## This variable will be used to share knowledge with other agents.
        ## The first value indicates the type of information that he will share (1 = less than (for buyers) &
        ## 2 = more than (for sellers)) and the second value the price associated, both of them associated to the last trade.
        self.can_negotiate = True ## If they can trade or not.
        self.last_deal_price = -1 ## The information about the last transaction the agent made.
        self.min_price = config.lowprice
        self.max_price = config.highprice

    ## Adding another price to the possible prices.
    def add_possible_price(self, price):
        self.possible_prices = np.append(self.possible_prices, price)
        self.possible_prices = np.unique(self.possible_prices)
        self.possible_prices = np.sort(self.possible_prices)

    ##Remove a price from the possible prices.
    def remove_possible_price(self, price):
        index = -1
        for i, p in np.ndenumerate(self.possible_prices):
            if price == p:
                index = i
        if index != -1:
            self.possible_prices = np.delete(self.possible_prices, index)
        self.possible_prices = np.sort(self.possible_prices)

    ## Updating the price of the last deal made by the agent
    def update_last_deal(self, price):
         self.last_deal_price = price

    def update_can_negotiate(self, bool_value):
        self.can_negotiate = bool_value


class Buyer(Agent):
    def __init__(self, vector_prices, config):
        Agent.__init__(self, vector_prices, config)
        self.sharing_knowledge = [1,-1]

    ## As a Buyer, if someone made a deal for less price than some of your possible scenarios, you will
    ## remove these ones, to achieve deals for less or equal value than that one (good ones for you).
    def adquire_knowledge(self, new_knowledge):
        for number in range(new_knowledge[1], self.max_price+1):
            self.remove_possible_price(number)

    def update_share_information(self):
        value = randint(self.last_deal_price, self.max_price+1)
        self.sharing_knowledge = [1, value]

    def pick_seller(self, available_sellers):
        """
        A Buyer should select a seller from all available sellers. Given is a list of
        available sellers. Currently simply the first seller is selected, although a
        more sophisticated method might be implemented for this
        """

        return available_sellers[0]

    def negotiation_with_seller(self, seller):
        """
        Negotiate with the given seller. This consists of bargaining about the price and
        eventually come to a transaction if a price is reached which is agreed upon or
        otherwise no trade.
        Currently the sellers offer their highest price, the buyer offer their lowest
        price and they move towards each other. Agents stop raising or lowering their
        price when it is not considered possible in their worlds.
        """

        seller_price_generator = seller.get_price_generator()
        import pdb; pdb.set_trace()
        return x


class Seller(Agent):
    def __init__(self, vector_prices, config):
        Agent.__init__(self, vector_prices, config)
        self.sharing_knowledge = [2, -1]

    ## As a seller, if someone made a deal for more price than some of your possible scenarios, you will
    ## remove these ones, to achieve deals for more or equal value than that one (good ones for you).
    def adquire_knowledge(self, new_knowledge):
        for number in range(self.min_price, new_knowledge[1]):
            self.remove_possible_price(number)

    def update_share_information(self):
        ## based on the number, "randomize" -> second value of knowledge
        value = randint(self.min_price, self.last_deal_price+1)
        self.sharing_knowledge = [2, value]

    def get_price_generator(self):
        """
        Yields prices during negotiation according to some negotiation scheme. These can
        be varied, but for now the most simple negotatiation scheme is used:
            - a decreasing price
        """

        for price in reversed(self.possible_prices):
            yield price
