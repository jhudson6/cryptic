# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 16:25:50 2018

@author: jhudson
"""
import pandas as pd
import numpy as np
import cryptoFunctions as cf

def load(markets,pairs,get='Open'):
    tmp = pairs[pairs.symbol.isin(markets.pair.unique())]
    print(tmp.symbol.unique())
    for i in tmp.symbol:
        tmpdat = cf.getOHLC_CW(i,markets.exchange.values[markets.pair == i][0],interval = 86400)
#        print([list(markets.exchange.values[markets.pair == tmp.symbol[i]]),i])
        print(i)