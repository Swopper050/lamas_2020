#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from random import seed
from random import randint

seed(1)

MAX_PRICE = 9
MIN_PRICE = 1


# In[2]:


class Agent:
    def __init__(self, vector_prices):
        self.possible_prices = vector_prices ## Al the prices the agent consider possible.
        self.sharing_knowledge = [-1,-1] ## This variable will be used to share knowledge with other agents.
        ## The first value indicates the type of information that he will share (1 = less than (for buyers) &
        ## 2 = more than (for sellers)) and the second value the price associated, both of them associated to the last trade.
        self.can_negotiate = True ## If they can trade or not.
        self.last_deal_price = -1 ## The information about the last transaction the agent made.

    ## Adding another price to the possible prices.
    def add_possible_price(self,price):
        self.possible_prices = np.append(self.possible_prices,price)
        self.possible_prices = np.unique(self.possible_prices)
        self.possible_prices = np.sort(self.possible_prices)
        
    ##Remove a price from the possible prices.
    def remove_possible_price(self,price):
        index = -1
        for i,p in np.ndenumerate(self.possible_prices):
            if price == p:
                index = i
        if index != -1:
            self.possible_prices = np.delete(self.possible_prices,index)
        self.possible_prices = np.sort(self.possible_prices)
    
    ## Updating the price of the last deal made by the agent
    def update_last_deal(self,price):
         self.last_deal_price = price
            
    def update_can_negotiate(self,bool_value):
        self.can_negotiate = bool_value


# In[3]:


class Buyer(Agent):
    def __init__(self, vector_prices):
        Agent.__init__(self,vector_prices)
        self.sharing_knowledge = [1,-1]
    
    ## As a Buyer, if someone made a deal for less price than some of your possible scenarios, you will
    ## remove these ones, to achieve deals for less or equal value than that one (good ones for you).
    def adquire_knowledge(self,new_knowledge):
        for number in range(new_knowledge[1],MAX_PRICE+1):
            self.remove_possible_price(number)
            
    def update_share_information(self):
        value = randint(self.last_deal_price,MAX_PRICE+1)
        self.sharing_knowledge = [1,value]


# In[4]:


class Seller(Agent):
    def __init__(self, vector_prices):
        Agent.__init__(self,vector_prices)
        self.sharing_knowledge = [2,-1]
        
    ## As a seller, if someone made a deal for more price than some of your possible scenarios, you will
    ## remove these ones, to achieve deals for more or equal value than that one (good ones for you).
    def adquire_knowledge(self,new_knowledge):
        for number in range(MIN_PRICE,new_knowledge[1]):
            self.remove_possible_price(number)
            
    def update_share_information(self):
        ## based on the number, "randomize" -> second value of knowledge
        value = randint(MIN_PRICE,self.last_deal_price+1)
        self.sharing_knowledge = [2,value]


# In[21]:





# In[22]:





# In[ ]:




