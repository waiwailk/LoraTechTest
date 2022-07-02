#!/usr/bin/python
import psycopg2
import collections
from config import config


def connect():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        text_file = open('total_return_index.sql','r')
        data = text_file.read()
        text_file.close()
        cur.execute(data)

        stock_list = {}
        for ticker,month,trading_day,total_return_index in cur.fetchall():
            if ticker in stock_list.keys():
                pair = (trading_day, total_return_index)
                stock_list[ticker].append(pair)
            else:
                tradeDaylist = []
                pair = (trading_day, total_return_index)
                tradeDaylist.append(pair)
                stock_list[ticker] = tradeDaylist

        symbollastTradePriceDict = {}    
        for key in stock_list:
            last_month = 0
            dayPriceDict = {}
            for i in range(len(stock_list[key])):
                if stock_list[key][i][0].month != last_month and (
                    i != 0 or i != len(stock_list[key])): 
                    #print(key, i,stock_list[key][i-1][0], stock_list[key][i-1][1])        
                    last_month = stock_list[key][i][0].month

                    dayPriceDict[ stock_list[key][i-1][0] ] = stock_list[key][i-1][1]
            #print('----------')        
            symbollastTradePriceDict[key] = collections.OrderedDict(sorted(dayPriceDict.items()))


        # prepare the .HSI index as the base tri_return reference        
        hsiMktOutPerformerDictItem = {}
        hsiItem = symbollastTradePriceDict['.HSI']
        lasttradePrice = 0
        for x in hsiItem:
            if lasttradePrice != 0: 
                pair = (hsiItem[x],hsiItem[x]/lasttradePrice-1) 
                hsiMktOutPerformerDictItem[x.month] = pair
            lasttradePrice = hsiItem[x]
        


        postgresSqlFile = open("postgres_mktoutlier.sql","w")
        mongoDBFile = open("mongo_mktoutlier.json","w")
        mongoDBFile.write("[");

        sSize = len(symbollastTradePriceDict)
        item = 1
        for key in symbollastTradePriceDict:
            eachItem = symbollastTradePriceDict[key]
            eachMktOutPerformerDictItem = {}
            lasttradePrice = 0
            for x in eachItem:
                if lasttradePrice != 0:
                    tri_return =  eachItem[x]/lasttradePrice-1
                    if tri_return > hsiMktOutPerformerDictItem[x.month][1]:
                        pair = (eachItem[x],tri_return,"true")
                    else:
                        pair = (eachItem[x],tri_return,"false")
                else:
                    tri_return = 0
                    if tri_return > hsiMktOutPerformerDictItem[x.month][1]:
                        pair = (eachItem[x],tri_return,"true")
                    else:
                        pair = (eachItem[x],tri_return,"false")

                lasttradePrice = eachItem[x]
                
                if x.year == 2020:
                    eachMktOutPerformerDictItem[x] = pair
            
            for x in eachMktOutPerformerDictItem:
                if item != sSize:
                    pline = "INSERT INTO monthly_market_outperformer VALUES ('" + key +"',"+ str(x.month) +","+ str(eachMktOutPerformerDictItem[x][1])+","+  eachMktOutPerformerDictItem[x][2]+ ');\n'
                    mline = '{"ticker": "'+key+'", "month": '+str(x.month)+', "tri_return": '+str(eachMktOutPerformerDictItem[x][1])+', "outperform": '+eachMktOutPerformerDictItem[x][2]+'},' + '\n'
                else:
                    pline = "INSERT INTO monthly_market_outperformer VALUES ('" + key +"',"+ str(x.month) +","+ str(eachMktOutPerformerDictItem[x][1])+","+  eachMktOutPerformerDictItem[x][2]+ ');'
                    mline = '{"ticker": "'+key+'", "month": '+str(x.month)+', "tri_return": '+str(eachMktOutPerformerDictItem[x][1])+', "outperform": '+eachMktOutPerformerDictItem[x][2]+'}]'

                postgresSqlFile.write(pline)
                mongoDBFile.write(mline)
            item = item + 1

        postgresSqlFile.close()
        mongoDBFile.close()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Postgres and Mongo file generated.')


if __name__ == '__main__':
    connect()
