# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 10:20:22 2018

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
for i,sfz in enumerate(ck_sfz["GMSFHM"]):
    hotel = pd.read_sql("SELECT * FROM TONGJI.CK_HOTEL WHERE GMSFHM='%s'"%sfz,con=connection)
    
    times = hotel[['RZSJ','TFSJ']]
    times = times.dropna()
    sub = times["TFSJ"]-times["RZSJ"]
    days = []
    for items in sub:
        days.append(int(items.days))
    all_days =sum(days)
    avg=-1.0
    if(len(days)):
        avg = all_days /float(len(days))
    query = "UPDATE TONGJI.CK_HOTEL_STATIS SET AVG_DAYS =%f WHERE GMSFHM='%s'"%(avg,sfz)    
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
    
    times = hotel[['RZSJ','TFSJ']]
    times = times.dropna()
    sub = times["TFSJ"]-times["RZSJ"]
    days = []
    for items in sub:
        days.append(int(items.days))
    all_days =sum(days)
    avg=-1.0
    if(len(days)):
        avg = all_days /float(len(days))
    query = "UPDATE TONGJI.XD_HOTEL_STATIS SET AVG_DAYS =%f WHERE GMSFHM='%s'"%(avg,sfz)
    try:
        result= c.execute(query)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        print'error occurs,is %s'%e
    finally:
        print '%i th done'%i