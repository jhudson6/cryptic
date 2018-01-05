# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:15:22 2017

@author: Odin
"""

## Hit API of crypto-watch, or others, to pull down desired data
## Manipulate data 

import requests as r
import pandas as pd
import numpy as np

def getOHLC_CW(pair, exchange = None, interval = None, url = None):
    if interval is None:
        interval = 14400
    if exchange is None:
        exchange = 'gdax'
    if url is None:
        url = "https://api.cryptowat.ch/markets/"
    url = url + str(exchange) + "/" + str(pair) + "/ohlc?periods=" + str(interval)
#    print(url)
    req = r.get(url)
    out = req.text
    
    if 'null' in out:
        return(pd.DataFrame(np.reshape([0,0,0,0,0,0,0],[-1,7]),columns = ['TimeStamp','Open','High','Low','Close','Vol','Other']))
    
    out = out[(out.index(':[')+2):(out.index('},')-1)]

    out = out.split(',[')
    out[0] = out[0][1:(len(out[0])-1)]
    for i in range(1,len(out)):
        out[i] = out[i][:(len(out[i])-1)]
        
    for i in range(0,len(out)):
        out[i] = out[i].split(',')
        
    for i in range(0,len(out)):
        out[i] = [float(num_str) for num_str in out[i]]
    
    out = pd.DataFrame.from_records(out,columns = ['TimeStamp','Open','High','Low','Close','Vol','Other'])
    out.Open = pd.to_numeric(out.Open)
    out.High = pd.to_numeric(out.High)
    out.Low = pd.to_numeric(out.Low)
    out.Close = pd.to_numeric(out.Close)
    return out

def listPairs_CW(url = None):
    if url is None:
        url = "https://api.cryptowat.ch/pairs"
    req = r.get(url)
    out = req.text
    out = out[out.index('"symbol"'):out.index('}],"allowance"')]
    out = out.split('},{')
    temp = out
    temp2 = pd.DataFrame(columns = ["x1","x2","x3","x4"])
    for i in range(0, len(temp)):
        tmp1 = temp[i][:temp[i].index('"base"')]
        tmp2 = temp[i][temp[i].index('"base"'):temp[i].index('"quote"')]
        tmp3 = temp[i][temp[i].index('"quote"'):(temp[i].index('},"route"')+2)]
        tmp4 = temp[i][(temp[i].index('},"route"')+2):]
        temp2 = temp2.append(pd.Series([tmp1,tmp2,tmp3,tmp4], index = ["x1","x2","x3","x4"]),ignore_index = True)
    
    temp3 = pd.DataFrame(columns = ["symbol","id"])
    for i in range(0, len(temp2)):
        tmp1 = temp2.x1[i][(temp2.x1[i].index('":"')+3):temp2.x1[i].index('","')]
        tmp2 = temp2.x1[i][(temp2.x1[i].index('d":')+3):(len(temp2.x1[i])-1)]
        temp3 = temp3.append(pd.Series([tmp1, tmp2], index = ["symbol","id"]),ignore_index = True)
        
    temp4 = pd.DataFrame(columns = ["base_id","base_symbol","base_name","base_isFiat","base_route"])
    for i in range(0, len(temp2)):
        tmp1 = temp2.x2[i][(temp2.x2[i].index('id')+4):(temp2.x2[i].index('symbol')-2)]
        tmp2 = temp2.x2[i][(temp2.x2[i].index('symbol')+9):(temp2.x2[i].index('name')-3)]
        tmp3 = temp2.x2[i][(temp2.x2[i].index('name')+7):(temp2.x2[i].index('fiat')-3)]
        tmp4 = temp2.x2[i][(temp2.x2[i].index('fiat')+6):(temp2.x2[i].index('route')-2)]
        tmp5 = temp2.x2[i][(temp2.x2[i].index('route')+8):(len(temp2.x2[i])-3)]
        temp4 = temp4.append(pd.Series([tmp1, tmp2, tmp3, tmp4, tmp5], index = ["base_id","base_symbol","base_name","base_isFiat","base_route"]),ignore_index = True)
        
    temp5 = pd.DataFrame(columns = ["quote_id","quote_symbol","quote_name","quote_isFiat","quote_route"])
    for i in range(0, len(temp2)):
        tmp1 = temp2.x3[i][(temp2.x3[i].index('id')+4):(temp2.x3[i].index('symbol')-2)]
        tmp2 = temp2.x3[i][(temp2.x3[i].index('symbol')+9):(temp2.x3[i].index('name')-3)]
        tmp3 = temp2.x3[i][(temp2.x3[i].index('name')+7):(temp2.x3[i].index('fiat')-3)]
        tmp4 = temp2.x3[i][(temp2.x3[i].index('fiat')+6):(temp2.x3[i].index('route')-2)]
        tmp5 = temp2.x3[i][(temp2.x3[i].index('route')+8):(len(temp2.x3[i])-3)]
        temp5 = temp5.append(pd.Series([tmp1, tmp2, tmp3, tmp4, tmp5], index = ["quote_id","quote_symbol","quote_name","quote_isFiat","quote_route"]),ignore_index = True)
        
    temp6 = pd.DataFrame(columns = ["route"])
    for i in range(0, len(temp2)):
        tmp1 = temp2.x4[i][temp2.x4[i].index('http'):(len(temp2.x4[i])-1)]
        temp6 = temp6.append(pd.Series(tmp1, index = ['route']), ignore_index = True)
        
    out = pd.concat([temp3, temp4, temp5, temp6],axis=1)
    return out

## Need to modify to handle the markets tag at the end of result
def getPair_CW(pair,url=None):
    if url is None:
        url = "https://api.cryptowat.ch/pairs"
    url = url + "/" + pair
    req = r.get(url)
    out = req.text
    out = out[(out.index('"markets"')+12):out.index('}]},"allowance"')]
    out = out.split('},{')
    temp = out
    temp2 = pd.DataFrame(columns = ["id","exchange","pair","active","route"])
    for i in range(0, len(temp)):
        tmp1 = temp[i][(temp[i].index("id")+4):(temp[i].index(',"exc'))]
        tmp2 = temp[i][(temp[i].index(',"exc')+12):(temp[i].index(',"pai'))]
        tmp3 = temp[i][(temp[i].index(',"pai')+8):(temp[i].index(',"act'))]
        tmp4 = temp[i][(temp[i].index(',"act')+10):(temp[i].index(',"rou'))]
        tmp5 = temp[i][(temp[i].index(',"rou')+9):(len(temp[i]))]
        temp2 = temp2.append(pd.Series([tmp1,tmp2,tmp3,tmp4,tmp5],index=["id","exchange","pair","active","route"]),ignore_index = True)
        
    out = temp2
    return out
    

def listMarkets_CW(url=None):
    if url is None:
        url = "https://api.cryptowat.ch/markets"
    req = r.get(url)
    out = req.text
    out = out[(out.index(':[{')+3):out.index('}],"allowance"')]
    out = out.split('},{')
    temp = out
    temp2 = pd.DataFrame(columns=['id','exchange','pair','active','route'])
    for i in range(0,len(temp)):
        tmp1 = temp[i][(temp[i].index("id")+4):(temp[i].index(',"ex'))]
        tmp2 = temp[i][(temp[i].index(',"ex')+13):(temp[i].index(',"pa')-1)]
        tmp3 = temp[i][(temp[i].index("pair")+7):(temp[i].index(',"ac')-1)]
        tmp4 = temp[i][(temp[i].index("active")+8):(temp[i].index(',"ro'))]
        tmp5 = temp[i][(temp[i].index("route")+8):(len(temp[i])-1)]
        temp2 = temp2.append(pd.Series([tmp1,tmp2,tmp3,tmp4,tmp5],index=['id','exchange','pair','active','route']),ignore_index = True)
    out = temp2
    return out

#def getMarket_CW(market, url=None):
    
def listExchanges_CW(url=None):
    if url is None:
        url = "https://api.cryptowat.ch/exchanges"
    req = r.get(url)
    out = req.text
    out = out[(out.index(':[{')+3):out.index('}],"allowance"')]
    out = out.split('},{')
    temp = out
    temp2 = pd.DataFrame(columns=['symbol','name','route','active'])
    for i in range(0,len(temp)):
        tmp1 = temp[i][(temp[i].index("symbol")+9):(temp[i].index(',"na')-1)]
        tmp2 = temp[i][(temp[i].index('name')+7):(temp[i].index(',"ro')-1)]
        tmp3 = temp[i][(temp[i].index("route")+8):(temp[i].index(',"ac')-1)]
        tmp4 = temp[i][(temp[i].index("active")+8):(len(temp[i]))]
        temp2 = temp2.append(pd.Series([tmp1,tmp2,tmp3,tmp4],index=['symbol','name','route','active']),ignore_index = True)
    out = temp2
    return out

#def getExchange_CW(exchange,url=None):
#    if url is None:
#        url = "https://api.cryptowat.ch/exchanges"
#    url = url + "/" + exchange
#    req = r.get(url)
#    out = req.text
#    out = out[(out.index(':[{')+3):out.index('}],"allowance"')]
#    out = out.split('},{')
#    temp = out
#    temp2 = pd.DataFrame(columns=['symbol','name','route','active'])

##This has some good information about asks,bids,etc.:
##https://money.stackexchange.com/questions/1063/can-someone-explain-a-stocks-bid-vs-ask-price-relative-to-current-price
def getOrderBook_CW(pair, exchange=None, url=None):
    if url is None:
        url = "https://api.cryptowat.ch/markets/"
    if exchange is None:
        exchange = "gdax"
    url = url + exchange + "/" + pair + "/orderbook"
    req = r.get(url)
    out = req.text
    asks = out[(out.index('"asks"')+9):(out.index('"bids"')-3)]
    asks = [x.split(',') for x in asks.split('],[')]
    [x.insert(0,'ask') for x in asks];
    bids = out[(out.index('"bids"')+9):(out.index('"allowance"')-4)]
    bids = [x.split(',') for x in bids.split('],[')]
    [x.insert(0,'bid') for x in bids];
    out = pd.DataFrame(asks+bids, columns = ['type','price','amount'])
#    out = out[(out.index(':[[')+3):(out.index('},"allowance"')-2)]
#    out = out.split('],[')
#    temp = out
#    temp2 = pd.DataFrame(columns=['price','amount'])
#    for i in range(0, len(temp)):
#        tmp = temp[i].split(',')
#        temp2 = temp2.append(pd.Series([tmp[0],tmp[1]],index=['price','amount']),ignore_index=True)
#    out = temp2
    out.amount = pd.to_numeric(out.amount)
    out.price = pd.to_numeric(out.price)
    return out

def getTrades_CW(pair, exchange=None, limit = None, url=None):
    #https://api.cryptowat.ch/markets/gdax/btcusd/trades
    if url is None:
        url = "https://api.cryptowat.ch/markets/"
    if exchange is None:
        exchange = "gdax"
    url = url + exchange + "/" + pair + "/trades"
    if limit is not None:
        url = url +"?limit=" + str(limit)
    req = r.get(url)
    out = req.text
    out = out[(out.index(':[[')+3):(out.index(']],"allowance"'))]
    out = out.split('],[')
    temp = out
    temp2 = pd.DataFrame(columns=['ID','timestamp','price','amount'])
    for i in range(0, len(temp)):
        tmp = temp[i].split(',')
        temp2 = temp2.append(pd.Series([tmp[0],tmp[1],tmp[2],tmp[3]],index=['ID','timestamp','price','amount']),ignore_index=True)
    out = temp2
    out.amount = pd.to_numeric(out.amount)
    out.price = pd.to_numeric(out.price)
    out['VolumeUSD'] = pd.Series(out.amount*out.price,index = out.index)
    return out

##Need to make it so can choose 'axis' to get tabulations across different dimensions
def getTradeSummary_CW(pair, exchange = None, limit = None, url = None):
    tradeDF = getTrades_CW(pair=pair,exchange=exchange,limit=limit,url=url)
    tmp1 = pd.crosstab(tradeDF.timestamp,'NumberTrades',values=tradeDF.amount,aggfunc=len)
    tmp2 = pd.crosstab(tradeDF.timestamp,'CoinVolOfTrade',values=tradeDF.amount,aggfunc=sum)
    tmp3 = pd.crosstab(tradeDF.timestamp,'USDVolOfTrade',values=tradeDF.VolumeUSD,aggfunc=sum)
    out = pd.concat([tmp1,tmp2,tmp3],axis=1)
    return out

## FLUX
    ## Need to have flux calculations, but currently do not know how to interpret the trades from api and orderbook properly
    ## Perhaps need to have the trades, which are trades/movements through the exchange between entites (/??), work with the 
    ## orderbook (and something to get current volume or aggregate volume over time T), to  get 'state', with ultimate goal
    ## being the rate of change of state or state transitions.
    
def getPrice_CW(pair = None, exchange=None, url=None):
    if pair is None:
        pair = 'btcusd'
    if exchange is None:
        exchange = 'gdax'
    if url is None:
        url =  'https://api.cryptowat.ch/markets/'
    url = url + exchange + "/" + pair + "/price"
    req = r.get(url)
    out = req.text
    out = float(out[(out.index('"price"')+8):(out.index('},"all'))])
    return out
    
##Order book spread
def getOrderBookSpread_CW(pair = None, maxSpread = 5, exchange=None, orderBook = None, url=None):
    if orderBook is None:
        if pair is None:
            raise ValueError('pair must be provided if orderbook is not')
        orderBook = getOrderBook_CW(pair = pair, exchange = exchange, url = url)
    price = getPrice_CW(pair = pair, exchange = exchange, url = url)
    asks = orderBook[orderBook.type == 'ask']
    bids = orderBook[orderBook.type == 'bid']
    supremumSpread = min(len(asks),len(bids))
    if maxSpread > supremumSpread:
        print('maxSpread too large, setting to supremumSpread:',supremumSpread)
        maxSpread = supremumSpread
    spreads = pd.DataFrame(columns = ['bid_price','ask_price','bid_amount','ask_amount','Vol_Shift_Pot','CoinPrice'])
    for i in range(0,maxSpread):
        indicator = bids.price.values[i]*bids.amount.values[i] - asks.price.values[i]*asks.amount.values[i] 
        tmp = pd.Series([bids.price.values[i], asks.price.values[i], bids.amount.values[i], 
                         asks.amount.values[i], indicator, price], index = ['bid_price','ask_price','bid_amount','ask_amount','Vol_Shift_Pot','CoinPrice'])
        spreads = spreads.append(tmp, ignore_index = True)
    return spreads

# https://api.cryptowat.ch/markets/gdax/btcusd/price

