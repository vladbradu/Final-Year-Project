import fms.engines.asynchronousrandwreplace
import fms.worlds.nullworld
import fms.agents.zerointelligencetrader
import fms.agents.randomtrader
import fms.agents.someintelligencetrader
import fms.agents.movingaveragetrader
import fms.agents.biginvestmenttrader
import fms.agents.nointelligencetrader
import fms.markets.continuousorderdriven
from fms.utils.priceQuantityTracker import priceList, quantityList, movingAverage
from fms.markets.continuousorderdriven import bestBids, bestOffers
import csv
import os.path

save_path = 'C:/Python27/'

class EngineParams(dict):
    def __init__ (self) :
        self.orderslogfile = None
    pass

engine_params= EngineParams()
engine_params.orderslogfile = open('log.txt', 'w')

engine_params['engines'] = [
        {
            'days':1,
            'daylength':1000,
            'clearbooksateod':True
        }
    ]
engine_params['timer'] = True
engine_params['csvdelimiter']=','
engine_params['show_books']=True
engine_params['unique_by_agent']=True
engine_params['randomseed']=1

engine = fms.engines.asynchronousrandwreplace.AsynchronousRandWReplace(engine_params)

some_agent1_params = {'agents': [{'money':10000, 'stocks':500, 'args':[999, 100]}]}
some_agent2_params = {'agents': [{'money':10000, 'stocks':500, 'args':[999, 100]}]}
some_agent3_params = {'agents': [{'money':10000, 'stocks':500, 'args':[999, 100]}]}
movingAverage_agent1_params = {'agents': [{'money':10000, 'stocks':200, 'args':[999, 100]}]}
bigInvestment_agent1_params = {'agents': [{'money':100000, 'stocks':500, 'args':[999, 100]}]}

numberOfagents = 100
agentslist=[]
#agentslist.append(fms.agents.biginvestmenttrader.BigInvestmentTrader(bigInvestment_agent1_params))

for i in range (0, 100):
    agentslist.append(fms.agents.nointelligencetrader.NoIntelligenceTrader(some_agent1_params))

#for i in range (0, 300):
    #agentslist.append(fms.agents.someintelligencetrader.SomeIntelligenceTrader(some_agent1_params))

#for i in range (0, 200):
   #agentslist.append(fms.agents.movingaveragetrader.MovingAverageTrader(movingAverage_agent1_params))

#for i in range (0, numberOfagents/3):
 #   agentslist.append(fms.agents.movingaveragetrader.MovingAverageTrader(movingAverage_agent1_params))
#agentslist.append(fms.agents.biginvestmenttrader.BigInvestmentTrader(bigInvestment_agent1_params))

"""
agentslist = [

    fms.agents.someintelligencetrader.SomeIntelligenceTrader(some_agent1_params),
    fms.agents.someintelligencetrader.SomeIntelligenceTrader(some_agent2_params),
    fms.agents.someintelligencetrader.SomeIntelligenceTrader(some_agent3_params),
    #fms.agents.movingaveragetrader.MovingAverageTrader(movingAverage_agent1_params),
    #fms.agents.biginvestmenttrader.BigInvestmentTrader(bigInvestment_agent1_params)

    ]
"""
print (agentslist[0])

world = fms.worlds.nullworld.NullWorld()

market = fms.markets.continuousorderdriven.ContinuousOrderDriven()

engine.run(world,agentslist, market)


#print "Big Investment Trader 1: ", agentslist[0]
#print "Stocks: ", agentslist[0].stocks
#print "Money: ", agentslist[0].money

"""
print "Agents:"
for i in range (0, numberOfagents):
    print "Some Intelligence Trader ", i, ": ", agentslist[i]
    print "Stocks: ", agentslist[i].stocks
    print "Money: ", agentslist[i].money

print "Big Investment Trader 1: ", agentslist[numberOfagents]
print "Stocks: ", agentslist[numberOfagents].stocks
print "Money: ", agentslist[numberOfagents].money


print "Some Intelligence Trader 2: ", agentslist[1]
print "Stocks: ", agentslist[1].stocks
print "Money: ", agentslist[1].money

print "Some Intelligence Trader 3: ", agentslist[2]
print "Stocks: ", agentslist[2].stocks
print "Money: ", agentslist[2].money
"""
"""
print "Moving Average Trader 1: ", agentslist[3]
print "Stocks: ", agentslist[3].stocks
print "Money: ", agentslist[3].money


"""
"""
print "Current Price is: ", priceList[-1]
print "Current Quantity is: ", quantityList[-1]
"""
print "List of prices is: ", priceList

csvFile = os.path.join(save_path, "Results.csv")
csvBids = os.path.join(save_path, "Bids.csv")
csvOffers = os.path.join(save_path, "Offers.csv")
out = csv.writer(open(csvFile, 'wb'), delimiter=',', quoting=csv.QUOTE_ALL)
for price in priceList:
    out.writerow([price])
out = csv.writer(open(csvBids, 'wb'), delimiter=',', quoting=csv.QUOTE_ALL)
for bid in bestBids:
    out.writerow([bid])
out = csv.writer(open(csvOffers, 'wb'), delimiter=',', quoting=csv.QUOTE_ALL)
for Offer in bestOffers:
    out.writerow([Offer])
#print "List of quantities is", quantityList

#print "Moving Average is: ", movingAverage[0]