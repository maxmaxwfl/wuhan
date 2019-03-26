# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 17:14:08 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import cx_Oracle
import time
import os
from collections import Counter
from sqlalchemy import types,create_engine

connection = cx_Oracle.connect('TONGJI/501430@127.0.0.1:1521/orcl',encoding='utf-8')
#tj_con = create_engine('oracle+cx_oracle://TONGJI:501430@127.0.0.1:1521/?service_name=orcl')
c=connection.cursor()

ck_sfz = pd.read_sql("SELECT DISTINCT GMSFHM FROM TONGJI.CK_HOTEL",con=connection)

#test date part
"""
test_sfz = ck_sfz.iloc[3]["GMSFHM"]
test = pd.read_sql("SELECT * FROM TONGJI.CK_HOTEL WHERE GMSFHM='%s'"%test_sfz,con=connection)
times = test["TFSJ"]-test["RZSJ"]
# drop 缺失的退房时间相减后会得到NaT 
times = times.dropna()
"""
for i,sfz in enumerate(ck_sfz["GMSFHM"]):
    hotel = pd.read_sql("SELECT * FROM TONGJI.CK_HOTEL WHERE GMSFHM='%s'"%sfz,con=connection)
    xm_list = hotel["XM"]
    xm=""
    for names in xm_list:
        if (names):
            xm = names
            break
    xm = xm.decode('utf-8')
    
    times = hotel[['RZSJ','TFSJ']]
    times = times.dropna()
    sub = times["TFSJ"]-times["RZSJ"]
    days = []
    for items in sub:
        days.append(str(items.days))
    day_count = Counter(days).most_common(10)
    day_list=""
    day_times=""
    for item in day_count:
        day_list += item[0].decode('utf-8')
        day_list += ';'
        day_times += str(item[1]).decode('utf-8')
        day_times += ';'
    hotels = hotel["QYMC"]
    hotels = hotels.dropna()
    hotel_count = Counter(hotels).most_common(10)
    hotel_list=""
    hotel_times=""
    for item in hotel_count:
        hotel_list += item[0].decode('utf-8')
        hotel_list += ';'
        hotel_times += str(item[1]).decode('utf-8')
        hotel_times += ';'
    types = hotel["YWLB"]
    types = types.dropna()
    types_count = Counter(types).most_common(10)
    type_list = ""
    type_times = ""
    for item in types_count:
        type_list += item[0].decode('utf-8')
        type_list += ';'
        type_times += str(item[1]).decode('utf-8')
        type_times += ';'
    query = "INSERT INTO CK_HOTEL_STATIS(GMSFHM,XM,TOP_DAY_LIST,TOP_DAYS,TOP_HOTEL_LIST,\
    TOP_HOTEL_TIMES,TOP_TYPE,TOP_TYPE_TIMES) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(sfz,xm,\
    day_list,day_times,hotel_list,hotel_times,type_list,type_times)
    try:
        result= c.execute(query)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        print'error occurs,is %s'%e
    finally:
        print '%i th done'%i

xd_sfz = pd.read_sql("SELECT DISTINCT GMSFHM FROM TONGJI.XD_HOTEL",con=connection)
for i,sfz in enumerate(xd_sfz["GMSFHM"]):
    hotel = pd.read_sql("SELECT * FROM TONGJI.XD_HOTEL WHERE GMSFHM='%s'"%sfz,con=connection)
    xm_list = hotel["XM"]
    xm=""
    for names in xm_list:
        if (names):
            xm = names
            break
    xm = xm.decode('utf-8')
    
    times = hotel[['RZSJ','TFSJ']]
    times = times.dropna()
    sub = times["TFSJ"]-times["RZSJ"]
    days = []
    for items in sub:
        days.append(str(items.days))
    day_count = Counter(days).most_common(10)
    day_list=""
    day_times=""
    for item in day_count:
        day_list += item[0].decode('utf-8')
        day_list += ';'
        day_times += str(item[1]).decode('utf-8')
        day_times += ';'
    hotels = hotel["QYMC"]
    hotels = hotels.dropna()
    hotel_count = Counter(hotels).most_common(10)
    hotel_list=""
    hotel_times=""
    for item in hotel_count:
        hotel_list += item[0].decode('utf-8')
        hotel_list += ';'
        hotel_times += str(item[1]).decode('utf-8')
        hotel_times += ';'
    types = hotel["YWLB"]
    types = types.dropna()
    types_count = Counter(types).most_common(10)
    type_list = ""
    type_times = ""
    for item in types_count:
        type_list += item[0].decode('utf-8')
        type_list += ';'
        type_times += str(item[1]).decode('utf-8')
        type_times += ';'
    query = "INSERT INTO XD_HOTEL_STATIS(GMSFHM,XM,TOP_DAY_LIST,TOP_DAYS,TOP_HOTEL_LIST,\
    TOP_HOTEL_TIMES,TOP_TYPE,TOP_TYPE_TIMES) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(sfz,xm,\
    day_list,day_times,hotel_list,hotel_times,type_list,type_times)
    try:
        result= c.execute(query)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        print'error occurs,is %s'%e
    finally:
        print '%i th done'%i