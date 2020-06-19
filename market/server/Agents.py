#!/usr/bin/env python
# coding: utf-8

import numpy as np
from random import seed
from random import randint, uniform, choice
from itertools import zip_longest
import names

seed(1)

class Agent:
    def __init__(self, vector_prices, vector_negotiation, config):
        self.possible_prices = vector_prices ## Al the prices the agent consider possible.
        self.negotiation_prices = vector_negotiation ## All the prices that the agent will offer in a negotiation.
        self.sharing_knowledge = [-1, -1, 'Empty'] ## This variable will be used to share knowledge with other agents.
        ## The first value indicates the type of information that he will share (1 = less than (for buyers) &
        ## 2 = more than (for sellers)) and the second value the price associated, both of them associated to the last trade.
        ## The last value is the sellers name if the buyers are gossiping
        self.can_negotiate = True ## If they can trade or not.
        self.last_deal = [-1,'Empty'] ## The information about the last transaction the agent made.
        ## The first parameter is the price, the second the name of the agent.
    
        
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
        
    ## Adding another price to the possible prices.
    def add_negotiation_price(self, price):
        if price < self.min_price or price > self.max_price:
            return
        self.negotiation_prices = np.append(self.negotiation_prices, price)
        self.negotiation_prices = np.unique(self.negotiation_prices)
        self.negotiation_prices = np.sort(self.negotiation_prices)

    ##Remove a price from the possible prices.
    def remove_negotiation_price(self, price):
        index = -1
        for i, p in np.ndenumerate(self.negotiation_prices):
            if price == p:
                index = i
        if index != -1:
            self.negotiation_prices = np.delete(self.negotiation_prices, index)
        self.negotiation_prices = np.sort(self.negotiation_prices)

    ## Updating the price of the last deal made by the agent
    def update_last_deal(self, name, price):
         self.last_deal = [price,name]

    def update_can_negotiate(self, bool_value):
        self.can_negotiate = bool_value


class Buyer(Agent):
    def __init__(self, vector_prices, config):
        Agent.__init__(self, vector_prices, config)
        self.type = 'buyer'
        
        ## Now we create the last_information matrix, that will be all the sellers in the first
        ## column with the last information of their prices in the second. This will allow the
        ## buyer to try to negotiate with the best one for their interest.
        dtype = [('name',np.unicode_,16),('price',np.int)]
        for seller in config.nsellers:
            if  self.last_information == []:
                self.last_information = [('Empty',-1)]
                self.last_information = np.array(self.last_information, dtype=dtype)
                
            else:
                new_information = [('Empty',-1)]
                new_information = np.array(self.new_information, dtype=dtype)
                self.last_information = np.vstack((self.last_information,new_information))      
        
        self.sharing_knowledge = [1, -1, 'Empty']
        
    ## Function to update the last information matrix given the price of a seller (name)
    def update_last_information(self,name,price):
        seller_found = False
        ## If we find the seller in our list, we update the price
        for seller in self.last_information:
            if seller[0][0] == name:
                seller[0][1] = price
                seller_found = True
        ## If we dont find the seller, we create the seller in a empty space        
        if (seller_found == False):
            for seller in self.last_information:
                if seller[0][0] == 'Empty':
                    seller[0][0] = name
                    seller[0][1] = price
                    break
                
    def get_last_information(self,name):
        for seller in self.last_information:
            if seller[0][0] == name:
                return seller
        return -1

    ## As a Buyer, if someone made a deal for less price than some of your possible scenarios, you will
    ## remove these ones, to achieve deals for less or equal value than that one (good ones for you).
    def acquire_knowledge(self, new_knowledge):
        if new_knowledge[1] == -1:
            return

        for number in np.arange(new_knowledge[1] + self.price_interval, self.max_price, self.price_interval):
            self.remove_possible_price(number)
            
        self.update_last_information(new_knowledge[2],new_knowledge[1])
        

    def update_share_information(self):
        if self.last_deal[1] == -1:
            self.sharing_knowledge = [1, -1, self.last_deal[2]]
        else:
            value = round(uniform(self.last_deal[0], self.max_price) * 2) / 2.
            self.sharing_knowledge = [1, value, self.last_deal[2]]

    def pick_seller(self, available_sellers):
        """
        A Buyer should select a seller from all available sellers. Given is a list of
        available sellers. The buyer uses the information available from all of them to
        try to select the best one. If the seller has a negative value of price, that
        means that we dont have any useful information, so he wont be selected.
        """
        selected_seller = []
        if available_sellers:
            for seller in available_sellers:
                info = self.get_last_information(seller.name)
                if selected_seller == []:
                    if info[1] > 0:
                        selected_seller = seller
                else:
                    prev_info = self.get_last_information(selected_seller.name)
                    if prev_info[1] > 0:
                        if info[1] < prev_info[1]:
                            selected_seller = seller
                        
            if selected_seller == []:
                return choice(available_sellers)
            else:
                return selected_seller
            
        return None
    
    ## As a buyer, if you have info of the seller's transactions, you will make offers based on
    ## the beliefs you have of his prices.
    def update_negotiation_price(self, seller):
        seller_info = self.get_last_information(seller.name)
        maximum_price = seller_info[1]
        if maximum_price > 0:
            if len(self.possible_prices) > 2:
                if maximum_price > max(self.possible_prices):
                    maximum_price = max(self.possible_prices)
                for number in np.arange(maximum_price - self.price_interval, self.max_price, self.price_interval):
                    self.remove_negotiation_price(number)

    def negotiation_with_seller(self, seller):
        """
        Negotiate with the given seller. This consists of bargaining about the price and
        eventually come to a transaction if a price is reached which is agreed upon or
        otherwise no trade.
        Currently the sellers offer their highest price, the buyer offer their lowest
        price and they move towards each other. Agents stop raising or lowering their
        price when it is not considered possible in their worlds, making a final offer at
        the boundary of their possibilities.
        """
        
        self.negotiation_prices = self.possible_prices
        seller.negotiation_prices = seller.possible_prices
        self.update_negotiation_price(seller)
        seller.update_negotiation_price()

        union_prices = set(seller.negotiation_prices) & set(self.negotiation_prices)

        # If empty, there will be no transaction
        if not union_prices:
            if min(seller.negotiation_prices) in self.possible_prices:
                self.last_deal[0] = seller.last_deal[0] = min(seller.negotiation_prices)
            elif max(self.negotiation_prices) in seller.possible_prices:
                self.last_deal[0] = seller.last_deal[0] = max(self.negotiation_prices)
            else:
                self.last_deal[0] = seller.last_deal[0] = -1
        else:
            union_prices = list(union_prices)
            middle_price = union_prices[len(union_prices) // 2]
            seller.last_deal[0] = self.last_deal[0] = middle_price
            
        self.last_deal[1] = seller.name
        
        return self.last_deal

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
        self.sharing_knowledge = [2, -1, 'Empty']

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
            self.sharing_knowledge = [1, -1, 'Empty']
        else:
            ## based on the number, "randomize" -> second value of knowledge
            value = round(uniform(self.min_price, self.last_deal[0]) * 2) / 2.
            self.sharing_knowledge = [2, value, 'Empty']

    def update_prices(self):
        """ Updates prices if no transaction was made. """
        if self.last_deal_price == -1:
            # Add a lower price to the possible worlds
            if len(self.possible_prices) != 0:
                self.add_possible_price(self.possible_prices[0] - self.price_interval)
            else:
                self.add_possible_price(self.max_price)
                
    ## As a seller, you won't make offers close to your minimum possible price, so you will
    ## remove prices close to it from your negotiation prices.
    def update_negotiation_price(self):
        for number in np.arange(self.min_price, min(self.possible_prices) + 3 * self.price_interval, self.price_interval):
            if len(self.possible_prices) > 3:  # We do not want to delete the last price
                self.remove_negotiation_price(number)