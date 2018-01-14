# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 15:02:59 2017

@author: Odin
"""
import numpy as np

def myMinMaxMap(inVec, low = 0, high = 1):
    dmax = np.max(inVec)
    dmin = np.min(inVec)
    out = (high - low)*(inVec - dmin)/(dmax - dmin) + low
    return out


def myZNorm(inVec):
    out = (inVec - np.mean(inVec))/(np.std(inVec))
    return out