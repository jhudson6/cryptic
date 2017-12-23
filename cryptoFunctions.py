# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:15:22 2017

@author: Odin
"""

## Hit API of crypto-watch, or others, to pull down desired data
## Manipulate data 

import requests as r
import pandas as pd

def getOHLC_CW(pair, interval = None, url = None):
    if interval is None:
        interval = 14400
    if url is None:
        url = "https://api.cryptowat.ch/markets/gdax/" + pair + "/ohlc?periods=" + str(interval)
    else:
        url = url + str(pair) + "/ohlc?periods=" + str(interval)
    print(url)
    req = r.get(url)
    out = req.text
    
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
        
    temp4 = pd.DataFrame(columns = ["base-id","base-symbol","base-name","base-isFiat","base-route"])
    for i in range(0, len(temp2)):
        tmp1 = temp2.x2[i][(temp2.x2[i].index('id')+4):(temp2.x2[i].index('symbol')-2)]
        tmp2 = temp2.x2[i][(temp2.x2[i].index('symbol')+9):(temp2.x2[i].index('name')-3)]
        tmp3 = temp2.x2[i][(temp2.x2[i].index('name')+7):(temp2.x2[i].index('fiat')-3)]
        tmp4 = temp2.x2[i][(temp2.x2[i].index('fiat')+6):(temp2.x2[i].index('route')-2)]
        tmp5 = temp2.x2[i][(temp2.x2[i].index('route')+8):(len(temp2.x2[i])-3)]
        temp4 = temp4.append(pd.Series([tmp1, tmp2, tmp3, tmp4, tmp5], index = ["base-id","base-symbol","base-name","base-isFiat","base-route"]),ignore_index = True)
        
    temp5 = pd.DataFrame(columns = ["quote-id","quote-symbol","quote-name","quote-isFiat","quote-route"])
    for i in range(0, len(temp2)):
        tmp1 = temp2.x3[i][(temp2.x3[i].index('id')+4):(temp2.x3[i].index('symbol')-2)]
        tmp2 = temp2.x3[i][(temp2.x3[i].index('symbol')+9):(temp2.x3[i].index('name')-3)]
        tmp3 = temp2.x3[i][(temp2.x3[i].index('name')+7):(temp2.x3[i].index('fiat')-3)]
        tmp4 = temp2.x3[i][(temp2.x3[i].index('fiat')+6):(temp2.x3[i].index('route')-2)]
        tmp5 = temp2.x3[i][(temp2.x3[i].index('route')+8):(len(temp2.x3[i])-3)]
        temp5 = temp5.append(pd.Series([tmp1, tmp2, tmp3, tmp4, tmp5], index = ["quote-id","quote-symbol","quote-name","quote-isFiat","quote-route"]),ignore_index = True)
        
    temp6 = pd.DataFrame(columns = ["route"])
    for i in range(0, len(temp2)):
        tmp1 = temp2.x4[i][temp2.x4[i].index('http'):(len(temp2.x4[i])-1)]
        temp6 = temp6.append(pd.Series(tmp1, index = ['route']), ignore_index = True)
        
    out = pd.concat([temp3, temp4, temp5, temp6],axis=1)
    return out

## Need to modify to handle the markets tag at the end of result
#def getPair_CW(pair,url=None):
#    if url is None:
#        url = "https://api.cryptowat.ch/pairs"
#    url = url + "/" + pair
#        req = r.get(url)
#    out = req.text
#    out = out[out.index('"symbol"'):out.index('}],"allowance"')]
#    out = out.split('},{')
#    temp = out
#    temp2 = pd.DataFrame(columns = ["x1","x2","x3","x4"])
#    for i in range(0, len(temp)):
#        tmp1 = temp[i][:temp[i].index('"base"')]
#        tmp2 = temp[i][temp[i].index('"base"'):temp[i].index('"quote"')]
#        tmp3 = temp[i][temp[i].index('"quote"'):(temp[i].index('},"route"')+2)]
#        tmp4 = temp[i][(temp[i].index('},"route"')+2):]
#        temp2 = temp2.append(pd.Series([tmp1,tmp2,tmp3,tmp4], index = ["x1","x2","x3","x4"]),ignore_index = True)
#    
#    temp3 = pd.DataFrame(columns = ["symbol","id"])
#    for i in range(0, len(temp2)):
#        tmp1 = temp2.x1[i][(temp2.x1[i].index('":"')+3):temp2.x1[i].index('","')]
#        tmp2 = temp2.x1[i][(temp2.x1[i].index('d":')+3):(len(temp2.x1[i])-1)]
#        temp3 = temp3.append(pd.Series([tmp1, tmp2], index = ["symbol","id"]),ignore_index = True)
#        
#    temp4 = pd.DataFrame(columns = ["base-id","base-symbol","base-name","base-isFiat","base-route"])
#    for i in range(0, len(temp2)):
#        tmp1 = temp2.x2[i][(temp2.x2[i].index('id')+4):(temp2.x2[i].index('symbol')-2)]
#        tmp2 = temp2.x2[i][(temp2.x2[i].index('symbol')+9):(temp2.x2[i].index('name')-3)]
#        tmp3 = temp2.x2[i][(temp2.x2[i].index('name')+7):(temp2.x2[i].index('fiat')-3)]
#        tmp4 = temp2.x2[i][(temp2.x2[i].index('fiat')+6):(temp2.x2[i].index('route')-2)]
#        tmp5 = temp2.x2[i][(temp2.x2[i].index('route')+8):(len(temp2.x2[i])-3)]
#        temp4 = temp4.append(pd.Series([tmp1, tmp2, tmp3, tmp4, tmp5], index = ["base-id","base-symbol","base-name","base-isFiat","base-route"]),ignore_index = True)
#        
#    temp5 = pd.DataFrame(columns = ["quote-id","quote-symbol","quote-name","quote-isFiat","quote-route"])
#    for i in range(0, len(temp2)):
#        tmp1 = temp2.x3[i][(temp2.x3[i].index('id')+4):(temp2.x3[i].index('symbol')-2)]
#        tmp2 = temp2.x3[i][(temp2.x3[i].index('symbol')+9):(temp2.x3[i].index('name')-3)]
#        tmp3 = temp2.x3[i][(temp2.x3[i].index('name')+7):(temp2.x3[i].index('fiat')-3)]
#        tmp4 = temp2.x3[i][(temp2.x3[i].index('fiat')+6):(temp2.x3[i].index('route')-2)]
#        tmp5 = temp2.x3[i][(temp2.x3[i].index('route')+8):(len(temp2.x3[i])-3)]
#        temp5 = temp5.append(pd.Series([tmp1, tmp2, tmp3, tmp4, tmp5], index = ["quote-id","quote-symbol","quote-name","quote-isFiat","quote-route"]),ignore_index = True)
#        
#    temp6 = pd.DataFrame(columns = ["route"])
#    for i in range(0, len(temp2)):
#        tmp1 = temp2.x4[i][temp2.x4[i].index('http'):(len(temp2.x4[i])-1)]
#        temp6 = temp6.append(pd.Series(tmp1, index = ['route']), ignore_index = True)
#        
#    out = pd.concat([temp3, temp4, temp5, temp6],axis=1)
#    return out
    

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

def getOrderBook_CW(pair, exchange=None, url=None):
    if url is None:
        url = "https://api.cryptowat.ch/markets/"
    if exchange is None:
        exchange = "gdax"
    url = url + exchange + "/" + pair + "/orderbook"
    req = r.get(url)
    out = req.text
    out = out[(out.index(':[[')+3):(out.index('},"allowance"')-2)]
    out = out.split('],[')
    temp = out
    temp2 = pd.DataFrame(columns=['price','amount'])
    for i in range(0, len(temp)):
        tmp = temp[i].split(',')
        temp2 = temp2.append(pd.Series([tmp[0],tmp[1]],index=['price','amount']),ignore_index=True)
    out = temp2
    return out












