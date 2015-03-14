#!/usr/bin/env python
"""
Asynchronous random with replace engine
"""

import random
import logging

from fms.engines import Engine
from fms.markets.continuousorderdriven import bestBids, bestOffers, averagePrice
from fms.utils.priceQuantityTracker import priceList

logger = logging.getLogger('fms.engines.asynchronousrandwreplace')

class AsynchronousRandWReplace(Engine):
    """
    Asynchronous engine, random sampling of agents,
    with replacement.
    """

    def __init__(self, parameters=None, offset=0):
        """
        Constructor. Takes parameters from config.
        Seeds ramdom engine from parameter.randomseed, if any.
        """
        Engine.__init__(self, parameters, offset)
        self.params = parameters
        self.rank = offset
        if parameters:
            random.seed(parameters['randomseed'])

    def run(self, world, agents, market):
        """
        Sample agents (with replacement) and let them speak on market.   
        As market is asynchronous, as soon as an agent speaks, do_clearing
        is called to execute any possible transaction immediately.
        """
        market.sellbook = world.state()['sellbook']
        logger.debug("Starting with sellbook %s" % market.sellbook)
        market.buybook = world.state()['buybook']
        logger.debug("Starting with buybook %s" % market.buybook)
        for day in range(self.days):
            for time in range(self.daylength):
                agt = random.randint(0, len(agents)-1)

                order = market.sanitize_order(agents[agt].speak())

                #check if the sellbook and buybook are maintained correctly
                #update the best offer lists


                if market.is_valid(agents[agt], order):
                    if self.params.orderslogfile:
                        self.output_order(order)



                    market.record_order(order, world.tick,
                            self.unique_by_agent)

                    if len(market.buybook)>0:
                        bestBids.append(market.buybook[-1][0])

                    else:
                        if len(bestBids)>0:
                            bestBids.append(bestBids[-1])

                    if len(market.sellbook)>0:
                        bestOffers.append(market.sellbook[0][0])

                    else:
                        if len(bestOffers)>0:
                            bestOffers.append(bestBids[-1])

                    #print "Bids buybook is: ", market.buybook
                    #print "Offers buybook is:", market.sellbook


                    if self.showbooks:
                        market.output_books(world.tick)



                    market.do_clearing(world.tick)
                    world.lastmarketinfo.update(
                            {'sellbook':market.sellbook, 'buybook':market.buybook})
                world.tick +=1

                if len(bestBids) > 0 and len(bestOffers) > 0:
                    if len(averagePrice) > 0:
                        averagePrice[0] = (bestBids[-1] + bestOffers[-1]) / 2.0
                    else:
                        averagePrice.append((bestBids[-1] + bestOffers[-1]) / 2.0)
                elif len(bestBids) > 0 and len(bestOffers) == 0:
                    if len(averagePrice) > 0:
                        averagePrice[0] = bestBids[-1]
                    else:
                        averagePrice.append(bestBids[-1])

                elif len(bestBids) == 0 and len(bestOffers) > 0:
                    if len(averagePrice) > 0:
                        averagePrice[0] = bestOffers[-1]
                    else:
                        averagePrice.append(bestOffers[-1])
                else:
                    averagePrice[0] = 100

                if len(bestBids)>0 :
                    print "Last Bid is: ", bestBids[-1]
                if len(bestOffers)>0:
                    print "Last Offers is: ", bestOffers[-1]
                #print "buybook", bestBids
                #print "sellbook", bestOffers


                if self.params['timer']:
                    world.show_time(day, time, self.days*self.daylength)
            if self.clearbooksateod:
                market.clear_books()
        logger.debug("Ending with sellbook %s" % market.sellbook)
        logger.debug("Ending with buybook %s" % market.buybook)

if __name__ == '__main__':
    print AsynchronousRandWReplace()
