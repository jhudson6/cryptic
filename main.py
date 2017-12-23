# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:26:53 2017

@author: Odin
"""

## Front end for crypto stuff

#reset

import cryptoFunctions as cf
import pandas as pd
import time as t
import random as rand
import tensorflow as tf

t1 = t.time()

##List Pairs
pairs = cf.listPairs_CW()

##List Exchanges
exchanges = cf.listExchanges_CW()

##List Markets
markets = cf.listMarkets_CW()

##Get Orderbook
btcusdOrderBook = cf.getOrderBook_CW('btcusd')

##Get CandleStick/OHLC Data
btcusdOHLC = cf.getOHLC_CW('btcusd')
ethusdOHLC = cf.getOHLC_CW('ethusd')
ltcusdOHLC = cf.getOHLC_CW('ltcusd')
xrpusdOHLC = cf.getOHLC_CW('xrpusd',url = "https://api.cryptowat.ch/markets/bitfinex/")
rnd_ind = rand.randint(0,len(pairs.symbol))
url = "https://api.cryptowat.ch/markets/" + str(markets.exchange.values[markets.pair == pairs.symbol[rnd_ind]][0]) + "/"
randOHLC = cf.getOHLC_CW(pairs.symbol.values[rnd_ind],url=url)

t2 = t.time()

print("Loaded Following Data Sets:\n\n -Pairs\n -Exchanges\n -Markets\n -OrderBook:\n     -btcusd\n -OHLC:\n     -btcusd\n     -ethusd\n     -ltcusd\n     -xrpusd\n     -",pairs.symbol.values[rnd_ind],"\n\n In ",t2-t1," Seconds.\n",sep='')



























#temp = pairs[pairs.index('"symbol"'):pairs.index('}],"allowance"')]
#temp = temp.split('},{')

#temp2 = pd.DataFrame(columns = ["symbol","id","base-id","base-symbol","base-name","base-isFiat","base-route","quote-id","quote-symbol","quote-name","quote-isFiat","quote-route","route"])
#temp2 = pd.DataFrame(columns = ["x1","x2","x3","x4"])
#for i in range(0, len(temp)):
#    tmp1 = temp[i][:temp[i].index('"base"')]
#    tmp2 = temp[i][temp[i].index('"base"'):temp[i].index('"quote"')]
#    tmp3 = temp[i][temp[i].index('"quote"'):(temp[i].index('},"route"')+2)]
#    tmp4 = temp[i][(temp[i].index('},"route"')+2):]
#    temp2 = temp2.append(pd.Series([tmp1,tmp2,tmp3,tmp4], index = ["x1","x2","x3","x4"]),ignore_index = True)
#
#temp3 = pd.DataFrame(columns = ["symbol","id"])
#for i in range(0, len(temp2)):
#    tmp1 = temp2.x1[i][(temp2.x1[i].index('":"')+3):temp2.x1[i].index('","')]
#    tmp2 = temp2.x1[i][(temp2.x1[i].index('d":')+3):(len(temp2.x1[i])-1)]
#    temp3 = temp3.append(pd.Series([tmp1, tmp2], index = ["symbol","id"]),ignore_index = True)
#    
#temp4 = pd.DataFrame(columns = ["base-id","base-symbol","base-name","base-isFiat","base-route"])
#for i in range(0, len(temp2)):
#    tmp1 = temp2.x2[i][(temp2.x2[i].index('id')+4):(temp2.x2[i].index('symbol')-2)]
#    tmp2 = temp2.x2[i][(temp2.x2[i].index('symbol')+9):(temp2.x2[i].index('name')-3)]
#    tmp3 = temp2.x2[i][(temp2.x2[i].index('name')+7):(temp2.x2[i].index('fiat')-3)]
#    tmp4 = temp2.x2[i][(temp2.x2[i].index('fiat')+6):(temp2.x2[i].index('route')-2)]
#    tmp5 = temp2.x2[i][(temp2.x2[i].index('route')+8):(len(temp2.x2[i])-3)]
#    temp4 = temp4.append(pd.Series([tmp1, tmp2, tmp3, tmp4, tmp5], index = ["base-id","base-symbol","base-name","base-isFiat","base-route"]),ignore_index = True)
#    
#temp5 = pd.DataFrame(columns = ["quote-id","quote-symbol","quote-name","quote-isFiat","quote-route"])
#for i in range(0, len(temp2)):
#    tmp1 = temp2.x3[i][(temp2.x3[i].index('id')+4):(temp2.x3[i].index('symbol')-2)]
#    tmp2 = temp2.x3[i][(temp2.x3[i].index('symbol')+9):(temp2.x3[i].index('name')-3)]
#    tmp3 = temp2.x3[i][(temp2.x3[i].index('name')+7):(temp2.x3[i].index('fiat')-3)]
#    tmp4 = temp2.x3[i][(temp2.x3[i].index('fiat')+6):(temp2.x3[i].index('route')-2)]
#    tmp5 = temp2.x3[i][(temp2.x3[i].index('route')+8):(len(temp2.x3[i])-3)]
#    temp5 = temp5.append(pd.Series([tmp1, tmp2, tmp3, tmp4, tmp5], index = ["quote-id","quote-symbol","quote-name","quote-isFiat","quote-route"]),ignore_index = True)
#    
#temp6 = pd.DataFrame(columns = ["route"])
#for i in range(0, len(temp2)):
#    tmp1 = temp2.x4[i][temp2.x4[i].index('http'):(len(temp2.x4[i])-1)]
#    temp6 = temp6.append(pd.Series(tmp1, index = ['route']), ignore_index = True)
#    
#out = pd.concat([temp3, temp4, temp5, temp6],axis=1)