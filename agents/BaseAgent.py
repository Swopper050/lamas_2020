from abc import ABC, abstractmethod

class BaseAgent(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def gossip(self):
        """ Exhanging knowledge  """
        pass

    @abstractmethod
    def knowledge_exchange(self, agent):
        """ Exhange knowledge with another agent """
        pass

    @abstractmethod
    def update_worlds(self):
        pass
