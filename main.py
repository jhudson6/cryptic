# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:26:53 2017

@author: Odin
"""

## Front end for crypto stuff

"""Cryptic Modules:
    Main:
        used to create books of coins and call class functions within book to pull and save data, prepare data set for fitting and fit models
    Classes:
        Defines two classes: Coins and Books
        Coin:
            Coin contains information about a coin such as the table name of the coin (btcusd_gdax), the pair (e.g. btcusd), the exchange (e.g. gdax) and 
            other relevent information such as the data and relevent interval for OHLC data
        Book:
            A book is created with a list of pairs and a specific exchange.  This book will then contain the coins in its wallet.  Contains
            functions to load data, save data to MySQL, etc.
    cryptoFunctions:
        Contains the functions to pull relevant data from the cryptowat.ch api as pandas dataframes.
        Contains functions to pull features from orderbook spreads
    mySQLFunctions:
        contains the functions neccessary to:
            check for needed tables,
            create missing tables,
            load data into tables,
            pull data from tables
    LSTM_TF:
        contains functions to prepare data and fit and predict a LSTM
    feedparser and rss:
        Intended to pull titles from google news feed following cryptocurrency and generate features, currently can only pull titles.
    myMappings:
        contains functions for feature mappings such as minmax and zNormalization."""

import os
os.chdir('C:\\Users\\Odin\\Documents\\Python Scripts\\CryptoMarketAnalytics')
import classes as cn

pairs = ['btcusd','ethusd','ltcusd']
book = cn.Book(pairs,exchange='gdax')












#import importlib as il
#import pandas as pd
#import time as t
#import random as rand
##import tensorflow as tf #Currently not set-up
#import numpy as np
#import numpy.random as rnd
#from sklearn.preprocessing import normalize
#import matplotlib as mplt
#from matplotlib import pyplot as plt

#import LSTM_TF as lstm
#import mySQLFunctions as mysql
#import cryptoFunctions as cf

\