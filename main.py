# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:26:53 2017

@author: Odin
"""

## Front end for crypto stuff

#reset

import os
os.chdir('C:\\Users\\jhudson\\Documents\\time-series exploration')
import cryptoFunctions as cf
import pandas as pd
import time as t
import random as rand
import tensorflow as tf
import numpy as np
import numpy.random as rnd
from sklearn.preprocessing import normalize
import matplotlib as mplt
from matplotlib import pyplot as plt
import LSTM_TF as lstm

#t1 = t.time()

##List Pairs
pairs = cf.listPairs_CW()
#
###List Exchanges
exchanges = cf.listExchanges_CW()
#
###List Markets
markets = cf.listMarkets_CW()
#
###Get Orderbook
#btcusdOrderBook = cf.getOrderBook_CW('btcusd')

##Get CandleStick/OHLC Data
btcusdOHLC = cf.getOHLC_CW('btcusd')
ethusdOHLC = cf.getOHLC_CW('ethusd')
ltcusdOHLC = cf.getOHLC_CW('ltcusd')
xrpusdOHLC = cf.getOHLC_CW('xrpusd','bitfinex')
#xrpusdOHLC = cf.getOHLC_CW('xrpusd',url = "https://api.cryptowat.ch/markets/bitfinex/")
rnd_ind = rand.randint(0,len(pairs.symbol))
#url = "https://api.cryptowat.ch/markets/" + str(markets.exchange.values[markets.pair == pairs.symbol[rnd_ind]][0]) + "/"
randOHLC = cf.getOHLC_CW(pairs.symbol.values[rnd_ind],markets.exchange.values[markets.pair == pairs.symbol[rnd_ind]][0])

##Get Trades
#gDaxTrades = cf.getTrades_CW('btcusd','gdax',100)
#gDaxOrderBook = cf.getOrderBook_CW('btcusd','gdax')
#gDaxTrades.amount = pd.to_numeric(gDaxTrades.amount)
#gDaxTrades.price = pd.to_numeric(gDaxTrades.price)
#gDaxTrades['VolumeUSD'] = pd.Series(gDaxTrades.price * gDaxTrades.amount, index=gDaxTrades.index)

#t2 = t.time()

#print("Loaded Following Data Sets:\n\n -Pairs\n -Exchanges\n -Markets\n -OrderBook:\n     -btcusd\n -OHLC:\n     -btcusd\n     -ethusd\n     -ltcusd\n     -xrpusd\n     -",pairs.symbol.values[rnd_ind],"\n\n In ",t2-t1," Seconds.\n",sep='')

#tmp1 = pd.crosstab(gDaxTrades.timestamp,'NumberTrades',values=gDaxTrades.amount,aggfunc=len)
#tmp2 = pd.crosstab(gDaxTrades.timestamp,'CoinVolOfTrade',values=gDaxTrades.amount,aggfunc=sum)
#tmp3 = pd.crosstab(gDaxTrades.timestamp,'USDVolOfTrade',values=gDaxTrades.VolumeUSD,aggfunc=sum)
#
#tradeSummarygDax = pd.concat([tmp1, tmp2, tmp3],axis=1)
#
#gDaxTradeSummary_BTCUSD = cf.getTradeSummary_CW('btcusd','gdax',100)

gDaxSpreads = cf.getOrderBookSpread_CW('btcusd')

preX = pd.concat([btcusdOHLC.Open, ethusdOHLC.Open, ltcusdOHLC.Open, xrpusdOHLC.Open, randOHLC.Open],axis=1)
preY = btcusdOHLC.Close.values.reshape(-1,1)

X_data, y_data = lstm.prepData(preX,preY,100)
myFit = lstm.fitLSTM(X_data,y_data)
















