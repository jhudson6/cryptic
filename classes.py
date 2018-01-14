# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 12:34:23 2018

@author: Odin
"""

##Define a 'coin' class to contain and get candle stick data, list exchanges, do functions, etc.

"""Classes contains two classes: Coin and Book
    Coin:
        Self values:
            name: the name exchange pair defining the market of the coin
            interval: the interval used for pulling OHLC data
            data: the OHLC data pulled by cryptofunctions
            pair: the pair of the coin, e.g. btcusd
            exchange: the exchange where the pair is traded, e.g. gdax
            source: where the data came from, currently only CW, will change as more API's are integrated
            table: where the data will be saved in MySql, e.g. btcusd_gdax
            orderbook: where any orderbook data will be stored
            trades: where any trades data will be stored
        Functions/Methods:
            getData_CW: load the OHLC data using the cryptofunctions module
            insertData_SQL: insert the current data, if loaded, into the MySql cryptic database
            loadData_SQL: load the OHLC data from the mySQL database
            fitLSTM: will be used to create and store a LSTM model
            getOrderBook: calls the getOrderBook_CW function from cryptoFunctions and stores in self.orderbook
            getTrades: same as getOrderBook but with trades
        
    Book:
        Self Values:
            name: user defined name of book
            pairs: the coin pairs contained in the book
            exchange: the exchange the book is defined on
            wallet: where all coins are stored
            count: number of coins contained in self.wallet
            interval: the interval that the OHLC data for each coin in self.wallet is defined over
            allowance: the allowance remaining on the API after the last call
            models: list of any trained and defined models on the coins
        Functions/Methods:
            listCoins: list all the coin names contained in the wallet
            getCoinData_CW: if data is not loaded for the coins, load the data
            saveData: save all the existing data for the coins in self.wallet and checks if MySql tables exist, if they dont it
                creates them
            createModel: will be used to create a model and save to self.models list"""

class Coin:
    """Coin Class for Holding Data and Executing Functions for Cleaning, Modeling, etc."""
    
    
    def __init__(self, pair, exchange, interval, Source = 'CW'): ##Source will later be used to define which API to use
        self.name = '{}:{}'.format(pair,exchange)
        self.interval = interval
#        self.data.per60 = []        #1 minute
#        self.data.per900 = []       #15 minutes
#        self.data.per1800 = []      #30 minutes
#        self.data.per3600 = []      #60 minutes
#        self.data.per21600 = []     #6 hours
#        self.data.per43200 = []     #12 hours
#        self.data.per86400 = []     #1 day
#        self.data.perUserDef = []   #User defined interval
#        self.data.userInterval = 0
        self.data = []
        self.pair = str(pair)
        self.exchange = str(exchange)
        self.source = Source
        self.table = '{}_{}'.format(pair,exchange)
        self.orderbook = []
        self.trades = []
        
    ##def __iter__(self):
        ##return self
    ##def __next__(self):
        ##if self.index == 0:
            ##raise StopIteration
        ##self.index = self.index - 1.....
        ##return self.data[self.index]
        
    ##Method to load data from crypto functions module
    def getData_CW(self,interval, verbose = False):
        import cryptoFunctions as cf
        self.data = cf.getOHLC_CW(self.pair, exchange = self.exchange, interval = self.interval, verbose = verbose)
#        if interval == 60:
#            self.data.per60 = cf.getOHLC_CW(self.name, exchange = self.exchange, interval = interval, verbose = verbose)
#        elif interval == 900:
#            self.data.per900 = cf.getOHLC_CW(self.name, exchange = self.exchange, interval = interval, verbose = verbose)
#        elif interval == 1800:
#            self.data.per1800 = cf.getOHLC_CW(self.name, exchange = self.exchange, interval = interval, verbose = verbose)
#        elif interval == 3600:
#            self.data.per3600 = cf.getOHLC_CW(self.name, exchange = self.exchange, interval = interval, verbose = verbose)
#        elif interval == 21600:
#            self.data.per21600 = cf.getOHLC_CW(self.name, exchange = self.exchange, interval = interval, verbose = verbose)
#        elif interval == 43200:
#            self.data.per43200 = cf.getOHLC_CW(self.name, exchange = self.exchange, interval = interval, verbose = verbose)
#        elif interval == 86400:
#            self.data.per86400 = cf.getOHLC_CW(self.name, exchange = self.exchange, interval = interval, verbose = verbose)
#        else:
#            self.data.perUserDef = cf.getOHLC_CW(self.name, exchange = self.exchange, interval = interval, verbose = verbose)
#            self.data.userInterval = interval
            
    def insertData_SQL(self):
        import mySQLFunctions as mysql
        if self.data == []:
            print('No Data To Insert Into Database!')
            return
        else:
            mysql.insertData(data = self.data, Table = self.table)
            return
    
    def loadData_SQL(self,whereClause=None):
        import mySQLFunctions as mysql
        if self.data != []:
            print("Data Already Loaded!")
            return
        else:
            self.data = mysql.getData(Table = self.table, whereClause = whereClause)

            
    def fitLSTM(self):
        import LSTM_TF as lstm
        print('Under Construction')
        return
    
    def getOderBook(self):
        import cryptoFunctions as cf
        if self.orderBook != []:
            print('OderBook Already Loaded!')
            return
        else:
            self.orderBook = cf.getOrderBook_CW(self.name,exchange = self.exchange,allowance=True,verbose=False)
            return
        
    def getTrades(self, limit = None):
        import cryptoFunctions as cf
        if self.trades != []:
            print('Trades Already Loaded!')
            return
        else:
            self.trades = cf.getTrades_CW(self.pair, self.exchange, limit = limit)
            return
    
    
        
    
class Book:
    """Book class for holding coin classess.  Coin classess can be loaded automatically or added manually."""
    
    def __init__(self,name = 'Coin Book',pairs=None,exchange=None,Table = None, loadCoins = True, interval = 86400):
        import cryptoFunctions as cf
        import pandas as pd
        self.name = name
        self.pairs = pairs
        self.exchange = exchange
        if pairs is None:
            self.wallet = []
        else:
            if isinstance(pairs,list):
                pairs = pd.Series(pairs)
            if exchange is None:
                exchange = 'gdax'
            elif ~isinstance(exchange,str) != -2:
                raise ValueError('exchange must be single string')
            self.wallet = [Coin(pair=pair,exchange=exchange,interval=interval) for pair in pairs.values]
        self.count = len(self.wallet)
        self.interval = interval
        if loadCoins:
            for i in range(self.count):
                self.wallet[i].getData_CW(interval = interval, verbose = True)
        self.allowance = cf.getAllowance()
        self.models = []
        
#    def __iter__(self):
#        return self
    
    def listCoins(self):
        print([coin.name for coin in self.wallet])
        return
    
    def getCoinData_CW(self,verbose=False):
        [self.wallet[i].getData_CW(interval = interval, verbose = verbose)]
        return
        
    def saveData(self):
        for coin in self.wallet:
            if not mysql.checkTables(coin.pair,coin.exchange):
                mysql.createTable(coin.table)
            if coin.data != []:
                print('No data for: {}'.format(coin))
            else:
                coin.saveData_SQL()
        return
    
    def createModel(self, pairs, useOrderBook=False, otherData = None,time_steps = 20, normType = 'minmax'):
        import pandas as pd
        import numpy as np
        import LSTM_TF as lstm
        if not isinstance(pairs, pd.core.series.Series):
            pairs = pd.Series(pairs)
        import LSTM_TF as lstm
        if any([pair not in [coin.pair for coin in self.wallet] for pair in pairs.values]):
            print('Not all pairs provided are contained in the wallet.')
            return
        else:
            modidx = len(self.models)
            self.models.append(newModel())
            tmpDataX = pd.concat([pair.data.open for pair in [self.wallet[i] for i in np.where([pair.pair in pairs.values for pair in self.wallet])[0]]], axis = 1, ignore_index=True)
            tmpDataX = tmpDataX.rename(columns = pairs)
            idx = np.where([coin.pair == pairs[0] for coin in self.wallet])[0]
            tmpDataY = self.wallet[idx[0]].data.close
            X_data, y_data = lstm.prepData(Xin = tmpDataX, yin = tmpDataY, time_steps = time_steps,normType = normType)
            self.models[modidx].X_data = X_data
            self.models[modidx].y_data = y_data
        return
                
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        