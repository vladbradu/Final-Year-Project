#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Module defining NoIntelligenceTrader agent class.
"""

import random


from fms import agents
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter
from fms.utils.priceQuantityTracker import priceList, bestBuyOffers, bestSellOffers, previousBestSellOffers, previousBestBuyOffers
from fms.markets.continuousorderdriven import bestOffers, bestBids, averagePrice






class NoIntelligenceTrader(agents.Agent):
    """
    Simulate an agent taking some decisions

    This agent subclass should have two keys in the
    args dict :
    - maxprice : maximum order price (float)
    - maxbuy : maximum quantity to buy (int)
    If any of those parameters is missing, a MissingParameter
    exception is raised.
    >>> from fms.agents import nointelligencetrader
    >>> params = {'agents': [{'money':10000, 'stocks':200}]}
    >>> agent = nointelligencetrader.NoIntelligenceTrader(params)
    Traceback (most recent call last):
        ...
    MissingParameter: maxprice
    >>> params = {'agents': [{'money':10000, 'stocks':200, 'args':[999]}]}
    >>> agent = nointelligencetrader.NoIntelligenceTrader(params)
    Traceback (most recent call last):
        ...
    MissingParameter: maxbuy
    >>> params = {'agents': [{'money':10000, 'stocks':200, 'args':[999, 100]}]}
    >>> agent = nointelligencetrader.NoIntelligenceTrader(params)
    >>> print agent.state()
    Agent ... - owns $10000.00 and    200 securities
    >>> print agent.maxprice
    999
    >>> print agent.maxbuy
    100

    The NoIntelligenceTrader acts by returning a
    dict with (direction, price, quantity) keys.
    The 3 elements of the dict are randomly chosen,
    in uniform distributions.
    >>> len(agent.act())
    3

    - direction is buy or sell
    - price is a %.2f float in [0.01,maxprice]
    - quantity is an int in :
      - if direction==BUY, [1,self.maxbuy]
      - if direction==SELL, [1,self.stocks]
    Thus, shortselling is not allowed.
    """

    def __init__(self, params, offset=0):
        agents.Agent.__init__(self, params, offset)
        try:
            self.maxprice = self.args[0]
        except (AttributeError, IndexError):
            raise MissingParameter, 'maxprice'
        try:
            self.maxbuy = self.args[1]
        except IndexError:
            raise MissingParameter, 'maxbuy'
        del self.args
    def act(self, world=None, market=None):
        """
        Return random order as a dict with keys in (direction, price, quantity).

        To avoid short selling as far as possible, if # of stocks
        is zero or negative, force BUY direction.
        """
       #if 0 < self.stocks <= 2000:
            #direction = random.choice((BUY, SELL))
       # elif self.stocks > 2000:
            #direction = SELL
        #if self.stocks > 0:
         #   direction = random.choice((BUY, SELL))
        #else:
            # stocks<=0, short selling is forbidden
        direction = SELL

        # if this is the first bid, initialise market with 100


        if len(averagePrice) >0:
            print "Agent trying to buy at average price: ", averagePrice[0]

        if direction == BUY:

            if len(bestBids) == 0:
                price = 100.00
            else:
                price = float("{0:.2f}".format(random.uniform(99.97, 100.01) * averagePrice[0] / 100.0))

        if direction == SELL:
            if len(bestOffers) == 0:
                price = 100.00
            else:
                price = float("{0:.2f}".format(random.uniform(99.99, 100.03) * averagePrice[0] / 100.0))



        if direction:
            quantity = random.randint(1, self.stocks)
        else:
            quantity = random.randint(1, self.maxbuy)
        return {'direction':direction, 'price':price, 'quantity':quantity}


def _test():
    """
    Run tests in docstrings
    """
    import doctest
    doctest.testmod(optionflags=+doctest.ELLIPSIS)

if __name__ == '__main__':
    _test()
uthor__ = 'Vlad'
