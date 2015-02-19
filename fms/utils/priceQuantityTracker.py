#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Module to track price and quantity
"""
import  fms.engines.asynchronousrandwreplace


# Price

priceList=[]
quantityList=[]
movingAverage = []
bestBuyOffers = []
bestSellOffers = []

previousBestBuyOffers = []
previousBestSellOffers = []

def updateBuyOffers(bestOffer):
    if len(bestBuyOffers)>0:
        previousBestBuyOffers.append(bestBuyOffers[-1])

    bestBuyOffers.append(bestOffer)


def updateSellOffers(bestOffer):
    if len(bestSellOffers)>0:
        previousBestSellOffers.append(bestSellOffers[-1])
    bestSellOffers.append(bestOffer)



def updatePrice(executedprice):
        priceList.append(executedprice)


def updateQuantity(qty):
        quantityList.append(qty)

def updateMovingAverage():

    priceSum = 0
    movingAverage.append(priceSum)
    if len(priceList)>0:
        for i in range (0, len(priceList)):
            priceSum = priceSum + priceList[i]
        movingAverage[0] = priceSum / len(priceList)

    else:
        movingAverage.append(priceSum)
