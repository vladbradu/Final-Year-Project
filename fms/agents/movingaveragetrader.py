#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Module defining MovingAverageTrader agent class.
"""

import random

from fms import agents
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter
import fms.utils.priceQuantityTracker
from fms.utils.priceQuantityTracker import priceList, movingAverage


class MovingAverageTrader(agents.Agent):
    """
    Simulate an agent taking some decisions

    This agent subclass should have two keys in the
    args dict :
    - maxprice : maximum order price (float)
    - maxbuy : maximum quantity to buy (int)
    If any of those parameters is missing, a MissingParameter
    exception is raised.
    >>> from fms.agents import movingaveragetrader
    >>> params = {'agents': [{'money':10000, 'stocks':200}]}
    >>> agent = movingaveragetrader.MovingAverageTrader(params)
    Traceback (most recent call last):
        ...
    MissingParameter: maxprice
    >>> params = {'agents': [{'money':10000, 'stocks':200, 'args':[999]}]}
    >>> agent = movingaveragetrader.MovingAverageTrader(params)
    Traceback (most recent call last):
        ...
    MissingParameter: maxbuy
    >>> params = {'agents': [{'money':10000, 'stocks':200, 'args':[999, 100]}]}
    >>> agent = movingaveragetrader.MovingAverageTrader(params)
    >>> print agent.state()
    Agent ... - owns $10000.00 and    200 securities
    >>> print agent.maxprice
    999
    >>> print agent.maxbuy
    100

    The ZeroIntelligenceTrader acts by returning a
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

        if len(priceList) > 0:

            if movingAverage[0] > priceList[-1]:
                direction = BUY
            elif movingAverage[0] < priceList[-1] and self.stocks > 0:
                direction = SELL
            else: direction = BUY
        else:
            choice = random.randint(0, 1)
            if choice==0:
                direction = BUY
            else:
                direction = SELL

        #if self.maxprice > priceList[-1]:

        if len(priceList) > 0:
            if direction == SELL:
                price = float("{0:.2f}".format(random.uniform(99.96, 100.00) * priceList[-1] / 100))
            else:
                price = float("{0:.2f}".format(random.uniform(100.00, 100.04) * priceList[-1] / 100))
        else:
            price = 100.0

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
