import fms.engines.asynchronousrandwreplace
import fms.worlds.nullworld
import fms.agents.zerointelligencetrader
import fms.agents.randomtrader
import fms.agents.someintelligencetrader
import fms.markets.continuousorderdriven
from fms.utils.priceQuantityTracker import CURRENT_PRICE, CURRENT_QUANTITY

class EngineParams(dict):
    def __init__ (self) :
        self.orderslogfile = None
    pass

engine_params= EngineParams()
engine_params.orderslogfile = open('log.txt', 'w')

engine_params['engines'] = [
        {
            'days':1,
            'daylength':24,
            'clearbooksateod':True
        }
    ]
engine_params['timer'] = True
engine_params['csvdelimiter']=','
engine_params['show_books']=True
engine_params['unique_by_agent']=True
engine_params['randomseed']=1

engine = fms.engines.asynchronousrandwreplace.AsynchronousRandWReplace(engine_params)

zero_agent_params = {'agents': [{'money':10000, 'stocks':200, 'args':[999, 100]}]}
some_agent_params = {'agents': [{'money':10000, 'stocks':200, 'args':[999, 100]}]}
random_agent_params = {'agents': [{'money':10000, 'stocks':200, 'args':[100,20,200]}]}

agentslist = [
fms.agents.zerointelligencetrader.ZeroIntelligenceTrader(zero_agent_params),
    fms.agents.randomtrader.RandomTrader(random_agent_params),
    fms.agents.someintelligencetrader.SomeIntelligenceTrader(some_agent_params)
    ]

print (agentslist[0])

world = fms.worlds.nullworld.NullWorld()

market = fms.markets.continuousorderdriven.ContinuousOrderDriven()

engine.run(world,agentslist, market)

print "Agents:"
print "Zero Intelligence Trader: ", agentslist[0]
print "Stocks: ", agentslist[0].stocks
print "Money: ", agentslist[0].money

print "Some Intelligence Trader: ", agentslist[1]
print "Stocks: ", agentslist[1].stocks
print "Money: ", agentslist[1].money

print "Random Intelligence Trader: ", agentslist[2]
print "Stocks: ", agentslist[2].stocks
print "Money: ", agentslist[2].money

print "Current Price is: ", CURRENT_PRICE
print "Current Quantity is: ", CURRENT_QUANTITY