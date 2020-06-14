#!/usr/bin/env python
# coding: utf-8

import numpy as np
from random import seed
from random import randint, uniform, choice
from itertools import zip_longest
import names

seed(1)

class Agent:
    def __init__(self, vector_prices, config):
        self.possible_prices = vector_prices ## Al the prices the agent consider possible.
        self.sharing_knowledge = [-1, -1] ## This variable will be used to share knowledge with other agents.
        ## The first value indicates the type of information that he will share (1 = less than (for buyers) &
        ## 2 = more than (for sellers)) and the second value the price associated, both of them associated to the last trade.
        self.can_negotiate = True ## If they can trade or not.
        self.last_deal_price = -1 ## The information about the last transaction the agent made.
        self.market_situation = config.market_situation
        self.min_price = config.lowprice
        self.max_price = config.highprice
        self.price_interval = 0.50
        self.name = names.get_first_name()

    ## Adding another price to the possible prices.
    def add_possible_price(self, price):
        if price < self.min_price or price > self.max_price:
            return
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
        self.type = 'buyer'
        self.sharing_knowledge = [1, -1]

    ## As a Buyer, if someone made a deal for less price than some of your possible scenarios, you will
    ## remove these ones, to achieve deals for less or equal value than that one (good ones for you).
    def acquire_knowledge(self, new_knowledge):
        if new_knowledge[1] == -1:
            return

        for number in np.arange(new_knowledge[1] + self.price_interval, self.max_price, self.price_interval):
            self.remove_possible_price(number)

    def update_share_information(self):
        if self.last_deal_price == -1:
            self.sharing_knowledge = [1, -1]
        else:
            value = round(uniform(self.last_deal_price, self.max_price) * 2) / 2.
            self.sharing_knowledge = [1, value]

    def pick_seller(self, available_sellers):
        """
        A Buyer should select a seller from all available sellers. Given is a list of
        available sellers. Currently simply a random seller is selected, although a
        more sophisticated method might be implemented for this
        """
        if available_sellers:
            return choice(available_sellers)
        return None

    def interaction_with_seller(self, seller, market_sit):
        """
        Negotiate with the given seller. This consists of bargaining about the price and
        eventually come to a transaction if a price is reached which is agreed upon or
        otherwise no trade.
        Currently the sellers offer their highest price, the buyer offer their lowest
        price and they move towards each other. Agents stop raising or lowering their
        price when it is not considered possible in their worlds.
        """

        union_prices = set(seller.possible_prices) & set(self.possible_prices)

        # If empty, there will be no transaction
        if not union_prices:
            self.last_deal_price = seller.last_deal_price = -1
        else:
            union_prices = list(union_prices)
            middle_price = union_prices[len(union_prices) // 2]
            seller.last_deal_price = self.last_deal_price = middle_price

        return self.last_deal_price

    def update_prices(self):
        """ Updates prices if no transaction was made. """
        if self.last_deal_price == -1:
            # Add a higher price to the possible prices
            if len(self.possible_prices) != 0:
                self.add_possible_price(self.possible_prices[-1] + self.price_interval)
            else:
                self.add_possible_price(self.min_price)


class Seller(Agent):
    def __init__(self, vector_prices, config):
        Agent.__init__(self, vector_prices, config)
        self.type = 'seller'
        self.sharing_knowledge = [2, -1]

    def acquire_knowledge(self, new_knowledge):
        """As a seller, if someone made a deal for more price than some of your possible scenarios, you will
        remove these ones, to achieve deals for more or equal value than that one (good ones for you)."""
        if new_knowledge[1] == -1:
            return

        for number in np.arange(self.min_price, new_knowledge[1] + self.price_interval, self.price_interval):
            if len(self.possible_prices) > 1:  # We do not want to delete the last price
                self.remove_possible_price(number)

    def update_share_information(self):
        """
        Updates information this agent have about the last deal. If no deal was made,
        the agent will share no information (setting it to -1)
        """
        if self.last_deal_price == -1:
            self.sharing_knowledge = [1, -1]
        else:
            ## based on the number, "randomize" -> second value of knowledge
            value = round(uniform(self.min_price, self.last_deal_price) * 2) / 2.
            self.sharing_knowledge = [2, value]

    def update_prices(self):
        """ Updates prices if no transaction was made. """
        if self.last_deal_price == -1:
            # Add a lower price to the possible worlds
            if len(self.possible_prices) != 0:
                self.add_possible_price(self.possible_prices[0] - self.price_interval)
            else:
                self.add_possible_price(self.max_price)
