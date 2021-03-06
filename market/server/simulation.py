import argparse
import copy
from itertools import chain
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
from os.path import dirname, abspath
import random
from server.Agents import Buyer, Seller


def enumerate2(xs, start=0, step=1):
    for x in xs:
        yield (start, x)
        start += step


def simulation(config):
    """ Runs the simulation using the configurations given
    Config should be a namespace containing the following fields:
        config.market_situation
        config.ndays
        config.nbuyers
        config.nsellers
        config.lowprice
        config.highprice
        config.nbuyerinteractions
        config.nsellerinteractions
    """

    buyers, sellers = initialize_agents(config)

    av_buyer_prices = []
    av_seller_prices = []
    av_transaction_prices = []
    std_transaction_prices = []

    for day in range(config.ndays):

        for agent in chain(buyers, sellers):
            agent.last_deal = ['Empty', -1]

        # Make all trades during day
        random.shuffle(buyers)  # Let buyers pick sellers in random order
        available_sellers = copy.copy(sellers)
        day_transactions = []

        for buyer in buyers:
            # Let a buyer pick a seller, if no more sellers are available, None is returned
            seller = buyer.pick_seller(available_sellers)

            if seller is not None:
                # Negotiate with the selected seller and remember the transaction price
                debug = True if day > 200 else False
                debug=False
                transaction = buyer.interaction_with_seller(seller, debug=debug)
                if transaction[1] != -1:  # There was a deal
                    day_transactions.append(transaction)
                    available_sellers.remove(seller)

        # Update prices --> If an agent had no transaction, add more prices
        # Setup knowledge for sharing knowledge
        for agent in chain(buyers, sellers):
            agent.update_prices()
            agent.update_share_information()

        # Let buyers interact with buyers and sellers with sellers (pairs are selected randomly)
        agent_interactions(buyers, n_interactions=config.nbuyer_interactions)
        agent_interactions(sellers, n_interactions=config.nseller_interactions)
        # Store averages during the day for plotting
        av_day_price = np.mean([transaction[1] for transaction in day_transactions])
        std_day_price = np.std([transaction[1] for transaction in day_transactions])
        std_transaction_prices.append(std_day_price)
        if np.isfinite(av_day_price) and not av_day_price == -1:
            av_transaction_prices.append(av_day_price)
        else:
            if np.all([av_price == np.nan for av_price in av_transaction_prices]):
                av_transaction_prices.append(np.nan)
            else:
                av_transaction_prices.append(av_transaction_prices[-1])
        av_seller_prices.append(np.mean([min(seller.possible_prices) for seller in sellers]))
        av_buyer_prices.append(np.mean([max(buyer.possible_prices) for buyer in buyers]))

    # Plot the simulation
    fig, ax = plt.subplots()
    ax.plot(av_seller_prices, label="Average seller price")
    ax.plot(av_buyer_prices, label="Average buyer price")
    #ax.plot(av_transaction_prices, label="Average transaction price")

    markers, caps, bars = ax.errorbar(
        list(range(len(av_transaction_prices))),
        av_transaction_prices,
        std_transaction_prices,
        color='green',
        label='Average transaction price',
    )

    [bar.set_alpha(.05) for bar in bars]

    ax.set_xlabel("Days")
    ax.set_ylabel("Price")
    ax.legend()
    base_dir = dirname(dirname(abspath(__file__)))
    save_dir = os.path.join(base_dir, 'static/plots/simulation_fig.png')
    print(base_dir)
    print(save_dir)
    plt.savefig(save_dir)
    #plt.show()
    plt.clf()
    plt.close()
    return av_transaction_prices, av_seller_prices, av_buyer_prices


def initialize_agents(config):
    """
    Initializes agents using the config files. Does 2 things:
    Makes a list of buyers, all buyers have a random price range from (lowest - random number)
    Makes a list of sellers, all sellers have a random price range from (random number - highest)
    """

    buyer_prices = [np.arange(config.lowprice, get_random_high_buyer(config.lowprice, config.highprice), .50)
                    for _ in range(config.nbuyers)]
    seller_prices = [np.arange(get_random_low_seller(config.lowprice, config.highprice), config.highprice + .5, .50)
                     for _ in range(config.nsellers)]

    buyers = [Buyer(prices, config) for prices in buyer_prices]
    sellers = [Seller(prices, config) for prices in seller_prices]
    return buyers, sellers


def get_random_high_buyer(lowprice, highprice):
    """ Generates a random price (upper range) for a buyer. Used when initializing prices """
    diff = highprice - lowprice
    return round(random.uniform(lowprice, lowprice + .75 * diff) * 2) / 2.


def get_random_low_seller(lowprice, highprice):
    """ Generates a random price (lower range) for a seller. Used when initializing prices """
    diff = highprice - lowprice
    return round(random.uniform(lowprice + .25 * diff, highprice) * 2) / 2.


def agent_interactions(agents, n_interactions=10):
    """
    Accepts a list with agents and makes them interact. Random agents are selected
    to interact with each other, up to a number of interactions
    """

    n_agents = len(agents)
    if n_agents < 2:
        return
    for _ in range(n_interactions):
        # Select two random agents
        agent1_idx, agent2_idx = random.sample(range(n_agents), 2)
        agent1 = agents[agent1_idx]
        agent2 = agents[agent2_idx]
        #print(f"{agent1.type} {agent1.name} exchanges knowledge with {agent2.type} {agent2.name}")
        #print(f"{agent1.name} shares {agent1.sharing_knowledge}")
        #print(f"{agent2.name} shares {agent2.sharing_knowledge}")
        #print(f"{agent1.name} first has possible worlds {agent1.possible_prices}")
        agent1.acquire_knowledge(agent2.sharing_knowledge)
        agent2.acquire_knowledge(agent1.sharing_knowledge)
        #print(f"{agent1.name} now has possible worlds {agent1.possible_prices}")
        #print(f"{agent1.name} with last_information {agent1.last_information}")


if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description="Run market simulation with epistemic logic."
    )
    parser.add_argument('-m', '--market_situation',
                        type=str,
                        default='negotiation',
                        help='Type of market situation to use in the simulation')
    parser.add_argument('-n', '--ndays',
                        type=int,
                        default=10,
                        help='Number of days to run the simulation')
    parser.add_argument('-s', '--nsellers',
                        type=int,
                        default=5,
                        help='Number of sellers that participate in the simulation')
    parser.add_argument('-b', '--nbuyers',
                        type=int,
                        default=5,
                        help='Number of buyers that participate in the simulation')
    parser.add_argument('-minp', '--lowprice',
                        type=float,
                        default=1.0,
                        help='Lowest price possible in the complete simulation')
    parser.add_argument('-maxp', '--highprice',
                        type=float,
                        default=10.0,
                        help='Highest price possible in the complete simulation')
    config = parser.parse_args()
    #print("\n\n\n\n\n")
    simulation(config)
