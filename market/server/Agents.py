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
        self.sharing_knowledge = ['Empty', -1] ## This variable will be used to share knowledge with other agents.
        ## The first value indicates the type of information that he will share (1 = less than (for buyers) &
        ## 2 = more than (for sellers)) and the second value the price associated, both of them associated to the last trade.
        ## The last value is the sellers name if the buyers are gossiping
        self.last_deal = ['Empty', -1] ## The information about the last transaction the agent made.
        ## The first parameter is the price, the second the name of the agent.

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


class Buyer(Agent):
    def __init__(self, vector_prices, config):
        Agent.__init__(self, vector_prices, config)
        self.type = 'buyer'

        ## Now we create the last_information matrix, that will be all the sellers in the first
        ## column with the last information of their prices in the second. This will allow the
        ## buyer to try to negotiate with the best one for their interest.
        self.last_information = {}
        self.sharing_knowledge = ['Empty', -1]
        self.no_buy_streak = 0

    ## As a Buyer, if someone made a deal for less price than some of your possible scenarios, you will
    ## remove these ones, to achieve deals for less or equal value than that one (good ones for you).
    def acquire_knowledge(self, new_knowledge):
        if new_knowledge[1] == -1:
            return

        for number in np.arange(new_knowledge[1] + self.price_interval, self.max_price, self.price_interval):
            self.remove_possible_price(number)

        self.last_information[new_knowledge[0]] = new_knowledge[1]

    def update_share_information(self):
        if self.last_deal[1] == -1:
            self.sharing_knowledge = [self.last_deal[0], -1]
        else:
            value = round(uniform(self.last_deal[1], self.max_price) * 2) / 2.
            self.sharing_knowledge = [self.last_deal[0], value]

    def pick_seller(self, available_sellers):
        """
        A Buyer should select a seller from all available sellers. Given is a list of
        available sellers. The buyer uses the information available from all of them to
        try to select the best one. If the seller has a negative value of price, that
        means that we dont have any useful information, so he wont be selected. If nothing
        is known about the available sellers, a random seller is chosen.
        """

        selected_seller = None
        if available_sellers:
            for seller in available_sellers:
                if selected_seller is None and seller.name in self.last_information:
                    selected_seller = seller
                elif seller.name in self.last_information:
                    if self.last_information.get(seller.name, np.inf) < self.last_information[selected_seller.name]:
                        selected_seller = seller

            if selected_seller is None or uniform(0., 1.) < .2:
                selected_seller = choice(available_sellers)
        return selected_seller

    ## As a buyer, if you have info of the seller's transactions, you will make offers based on
    ## the beliefs you have of his prices.
    def update_negotiation_price(self, seller, negotiation_prices):
        maximum_seller_price = self.last_information.get(seller.name, np.inf)
        #maximum_seller_price += self.no_buy_streak * self.price_interval
        return negotiation_prices[negotiation_prices <= maximum_seller_price]

    def interaction_with_seller(self, seller, debug=False):
        """
        Negotiate with the given seller. This consists of bargaining about the price and
        eventually come to a transaction if a price is reached which is agreed upon or
        otherwise no trade.
        Currently the sellers offer their highest price, the buyer offer their lowest
        price and they move towards each other. Agents stop raising or lowering their
        price when it is not considered possible in their worlds, making a final offer at
        the boundary of their possibilities.
        """

        buyer_negotiation_prices = self.possible_prices
        buyer_negotiation_prices = self.update_negotiation_price(seller, buyer_negotiation_prices)
        seller_negotiation_prices = seller.possible_prices

        union_prices = set(seller_negotiation_prices) & set(buyer_negotiation_prices)

        self.last_deal = [seller.name, -1]
        seller.last_deal = [self.name, -1]
        if self.market_situation == 'negotiation':
            # If empty, there will be no transaction
            if union_prices:
                union_prices = list(union_prices)
                middle_price = union_prices[len(union_prices) // 2]
                seller.last_deal[1] = self.last_deal[1] = middle_price
        elif self.market_situation == 'grocery_store':
            seller_price = min(seller.possible_prices)
            if seller_price in buyer_negotiation_prices:
                seller.last_deal[1] = self.last_deal[1] = seller_price

        if debug:
            import pdb; pdb.set_trace()

        if self.last_deal[1] == -1:
            self.no_buy_streak += 1
        else:
            self.no_buy_streak = 0
        return self.last_deal

    def update_prices(self):
        """ Updates prices if no transaction was made. """
        if self.last_deal[1] == -1:
            # Add a higher price to the possible prices
            if len(self.possible_prices) != 0:
                self.add_possible_price(self.possible_prices[-1] + self.price_interval)
            else:
                self.add_possible_price(self.min_price)
        elif self.last_deal[1] < max(self.possible_prices) and len(self.possible_prices) > 1:
            self.remove_possible_price(max(self.possible_prices))


class Seller(Agent):
    def __init__(self, vector_prices, config):
        Agent.__init__(self, vector_prices, config)
        self.type = 'seller'
        self.sharing_knowledge = ['Empty', -1]

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
        if self.last_deal[1] == -1:
            self.sharing_knowledge = ['Empty', -1]
        else:
            ## based on the number, "randomize" -> second value of knowledge
            value = round(uniform(self.min_price, self.last_deal[1]) * 2) / 2.
            self.sharing_knowledge = [self.last_deal, value]

    def update_prices(self):
        """ Updates prices if no transaction was made. """
        if self.last_deal[1] == -1:
            # Add a lower price to the possible worlds
            if len(self.possible_prices) != 0:
                self.add_possible_price(self.possible_prices[0] - self.price_interval)
            else:
                self.add_possible_price(self.max_price)
        elif (self.last_deal[1] > min(self.possible_prices) or self.market_situation == 'grocery_store') and len(self.possible_prices) > 1:
            self.remove_possible_price(min(self.possible_prices))
