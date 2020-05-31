from agents.BaseAgent import BaseAgent

class Buyer(BaseAgent):

    def __init__(self, init_method):
        self.worlds = list(range(1, 10))

    def negotiation_with_seller(self, seller):
        return

    def pick_seller(self, available_sellers):
        return available_sellers[-1]

    def knowledge_exchange(self, agent):
        return

    def update_worlds(self):
        return

    def gossip(self):
        return
