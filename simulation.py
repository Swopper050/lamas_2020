import argparse
import copy
from itertools import chain
import random

from agents import Buyer, Seller


def simulation(config):
    """ Runs the simulation using the configurations given """

    buyers = [Buyer(config.init) for _ in range(config.nbuyers)]
    sellers = [Seller(config.init) for _ in range(config.nsellers)]

    for day in range(config.ndays):
        # Make all trades during day
        random.shuffle(buyers)  # Let buyers pick sellers in random order
        available_sellers = copy.copy(sellers)
        for buyer in buyers:
            seller = buyer.pick_seller(available_sellers)
            buyer.negotiation_with_seller(seller)
            available_sellers.remove(seller)

        agent_interactions(buyers, n_interactions=2)
        agent_interactions(sellers, n_interactions=2)
        for agent in chain(buyers, sellers):
            agent.update_worlds()


def agent_interactions(agents, n_interactions=10):
    """
    Accepts a list with agents and makes them interact. Random agents are selected
    to interact with each other, up to a number of interactions
    """

    n_agents = len(agents)
    for _ in range(n_interactions):
        # Select two random agents
        agent1_idx, agent2_idx = random.sample(range(n_agents), 2)
        agent1 = agents[agent1_idx]
        agent2 = agents[agent2_idx]
        agent1.knowledge_exchange(agent2)


if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description="Run market simulation with epistemic logic."
    )
    parser.add_argument('-n', '--ndays',
                        type=int,
                        default=10,
                        help='Number of days to run the simulation')
    parser.add_argument('-s', '--nsellers',
                        type=int,
                        default=1,
                        help='Number of sellers that participate in the simulation')
    parser.add_argument('-b', '--nbuyers',
                        type=int,
                        default=1,
                        help='Number of buyers that participate in the simulation')
    parser.add_argument('-i', '--init',
                        type=str,
                        default='default',
                        choices=['default'],
                        help='Price belief initialization method')
    config = parser.parse_args()
    simulation(config)
