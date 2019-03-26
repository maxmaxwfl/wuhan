# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 09:34:49 2018

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
#read all sfz lists from 
#ck
"""
ck_sfz = pd.read_sql("SELECT DISTINCT GMSFHM FROM TONGJI.CK_RAIL",con=connection)
for i,sfz in enumerate(ck_sfz["GMSFHM"]):
    railway = pd.read_sql("SELECT GMSFHM,XM,RAIL_CFZ,RAIL_MDZ,RAIL_CC FROM TONGJI.CK_RAIL \
                          WHERE GMSFHM='%s'"%sfz,con=connection)
    #combine 出发站和达到站 with '-'
    xm = railway.iloc[0]["XM"]
    xm = xm.decode('utf-8')
    combine = railway["RAIL_CFZ"]+'-'+railway["RAIL_MDZ"]
    rail_count = Counter(combine).most_common(10)
    rail_list=""
    rail_times=""
    for item in rail_count:
        rail_list += item[0].decode('utf-8')
        rail_list += ';'
        rail_times += str(item[1]).decode('utf-8')
        rail_times += ';'
    
    train = [item[0] for item in railway["RAIL_CC"]]
    train_count = Counter(train).most_common(10)
    train_list =""
    train_times =""
    for item in train_count:
        train_list += item[0].decode('utf-8')
        train_list +=';'
        train_times += str(item[1]).decode('utf-8')
        train_times +=';'
    query = "INSERT INTO CK_RAIL_STATIS(GMSFHM,XM,TOP_ROUTE_LIST,TOP_ROUTE_TIMES,\
    TOP_TRAIN_TYPE,TOP_TYPE_TIMES) VALUES ('%s','%s','%s','%s','%s','%s')"%(sfz,xm,\
    rail_list,rail_times,train_list,train_times)
    try:
        result= c.execute(query)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        print'error occurs,is %s'%e
    finally:
        print '%i th done'%i
"""
#xd
xd_sfz = pd.read_sql("SELECT DISTINCT GMSFHM FROM TONGJI.XD_RAIL",con=connection)
for i,sfz in enumerate(xd_sfz["GMSFHM"]):
    railway = pd.read_sql("SELECT GMSFHM,XM,RAIL_CFZ,RAIL_MDZ,RAIL_CC FROM TONGJI.XD_RAIL \
                          WHERE GMSFHM='%s'"%sfz,con=connection)
    #combine 出发站和达到站 with '-'
    xm_list = railway["XM"]
    xm=""
    for names in xm_list:
        if (names):
            xm = names
            break
    xm = xm.decode('utf-8')
    combine = railway["RAIL_CFZ"]+'-'+railway["RAIL_MDZ"]
    rail_count = Counter(combine).most_common(10)
    rail_list=""
    rail_times=""
    for item in rail_count:
        rail_list += item[0].decode('utf-8')
        rail_list += ';'
        rail_times += str(item[1]).decode('utf-8')
        rail_times += ';'
    
    train = [item[0] for item in railway["RAIL_CC"]]
    train_count = Counter(train).most_common(10)
    train_list =""
    train_times =""
    for item in train_count:
        train_list += item[0].decode('utf-8')
        train_list +=';'
        train_times += str(item[1]).decode('utf-8')
        train_times +=';'
    query = "INSERT INTO XD_RAIL_STATIS(GMSFHM,XM,TOP_ROUTE_LIST,TOP_ROUTE_TIMES,\
    TOP_TRAIN_TYPE,TOP_TYPE_TIMES) VALUES ('%s','%s','%s','%s','%s','%s')"%(sfz,xm,\
    rail_list,rail_times,train_list,train_times)
    try:
        result= c.execute(query)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        print'error occurs,is %s'%e
    finally:
        print '%i th done'%i