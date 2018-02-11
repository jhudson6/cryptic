# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 13:58:32 2018

@author: Odin
"""

"""Module contains functions to load into, query from and create data tables in a mySQL instance
    Functions:
        insertData: insert the supplied data into the supplied table
        getData: get the data stored in the supplied table
        checkTables: checks that the tables exist for the supplied pairs and exchange
        createTable: used to create a single table named Table
        createTables: used to check if tables for supplied pairs and single exchange exist and if the dont create them."""


import pyodbc as pyo
import pandas as pd
import numpy as np

def insertData(data,Table):
    conn = pyo.connect(r'DRIVER={MySQL ODBC 5.3 ANSI Driver};SERVER=localhost;DATABASE=crypto;USER=root;PASSWORD=mellon;OPTION=3;')
    curr = conn.cursor()
    tmp = data.columns
#    statement = 'insert into btcusd("{}") values (?, ?, ?, ?, ?, ?, ?)'.format('","'.join(tmp))
    statement = 'insert into btcusd values (?, ?, ?, ?, ?, ?, ?)'.format('","'.join(tmp))
    for i in range(len(data)):
        curr = curr.execute(statement, int(data.timespan.values[i]),str(data.TimeStamp[i]),data.Open.values[i],data.High.values[i],data.Low.values[i],data.Close.values[i],data.Vol.values[i])
        curr.commit()
    curr.close()
    return

def getData(Table,whereClause=None):
    conn = pyo.connect(r'DRIVER={MySQL ODBC 5.3 ANSI Driver};SERVER=localhost;DATABASE=crypto;USER=root;PASSWORD=mellon;OPTION=3;')
    curr = conn.cursor()
    if whereClause is None:
        query = 'Select * from {}'.format(str(Table))
    else:
        query = 'Select * from {} where '.format(str(Table),str(whereClause))
    data = curr.execute(query).fetchall()
    cols = np.array(list(curr.columns()))
    data = pd.DataFrame(np.array(list(data)), columns = [cols[i,3] for i in range(len(cols))])
    curr.close()
    return data

def checkTables(pairs,exchange):
    conn = pyo.connect(r'DRIVER={MySQL ODBC 5.3 ANSI Driver};SERVER=localhost;DATABASE=crypto;USER=root;PASSWORD=mellon;OPTION=3;')
    curr = conn.cursor()
    query = 'Select table_name from information_schema.tables where table_schema = "crypto"'
    curr = curr.execute(query)
    data = curr.fetchall()
    data = data[0]
    if isinstance(pairs,list) | isinstance(pairs,pd.core.series.Series):
        names = [pair+'_'+exchange for pair in pairs]
        if any([name not in list(data) for name in names]):
            return False
        else:
            return True
    elif isinstance(pairs,str):
        name = pairs+'_'+exchange
        if name not in list(data):
            return True
        else:
            return False

def createTable(Table):
    conn = pyo.connect(r'DRIVER={MySQL ODBC 5.3 ANSI Driver};SERVER=localhost;DATABASE=crypto;USER=root;PASSWORD=mellon;OPTION=3;')
    curr = conn.cursor()
    query = 'create table {}(timespan int(11) not null, timestamp datetime not null, open float not null, high float not null, low float not null, close float not null, vol float not null)'.format(Table)
    curr.execute(query)
    conn.commit()
    conn.close()

def createTables(pairs, exchange):
    if not isinstance(pairs,pd.core.series.Series):
        pairs = pd.Series(pairs)
    if not checkTables(pairs, exchange):
        tmp = pairs[np.where([checkTables(pair,exchange) for pair in pairs])[0]]
        toCreate = [pair+'_'+exchange for pair in tmp]
        print('Creating Tables: {}'.format(', '.join(toCreate)))
        [createTable(Table) for Table in toCreate]
    else:
        print('All tables listed already exist.')
        return
    
