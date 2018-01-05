# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 11:37:06 2018

@author: jhudson
"""

import numpy as np
import pandas as pd

def MACD(data,a,b,c):
    ewmaA = data.ewm(span=a).mean()
    ewmaB = data.ewm(span=b).mean()
    macdSeries = (ewmaA - ewmaB)
    signal = macdSeries.ewm(span=c).mean()
    divergence = macdSeries - signal
    return pd.concat([macdSeries, signal, divergence],axis=1)

def WilliamsPercentR(data,N):
    lastClose = data.Close.loc[len(data.Close)-1]
    NDayHigh = max(data.High.loc[(len(data.High)-(N+1)):])
    NDayLow = min(data.Low.loc[(len(data.Low)-(N+1)):])
    WPR = (NDayHigh - lastClose)/(NDayHigh - NDayLow)*(-100)
    return WPR

def UltOsc(data):
    lenn = len(data)
    tmp = pd.Series(data.Close)
    tmp.index = np.arange(1,lenn+1)
    tmp = tmp.set_value(0,0)
    tmp = tmp.drop(500,0)
    trueLow = tmp.combine(data.Low,min,0)
    trueHigh = tmp.combine(data.High,max,0)
    ##Currently do not know how to prevent the tmp.index assignment from changing the index in data
    data.Close.index = np.arange(0,lenn)
    bp = data.Close - trueLow
    tr = trueHigh - trueLow
    avg7 = sum(bp[(lenn-7):])/sum(tr[(lenn-7):])
    avg14 = sum(bp[(lenn-14):])/sum(tr[(lenn-14):])
    avg28 = sum(bp[(lenn-28):])/sum(tr[(lenn-28):])
    ultOsc = 100 * (4*avg7 + 2*avg14 + avg28)/7
    return ultOsc

def PPO(data,a,b,c):
    ewmaA = data.ewm(span=a).mean()
    ewmaB = data.ewm(span=b).mean()
    ppoSeries = (ewmaA - ewmaB)/ewmaB
    signal = ppoSeries.ewm(span=c).mean()
    divergence = ppoSeries - signal
    return pd.concat([ppoSeries, signal, divergence],axis=1)

