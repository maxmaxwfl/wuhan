# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 11:04:00 2018

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

ck_sfz = pd.read_sql("SELECT DISTINCT GMSFHM FROM TONGJI.CK_NET",con=connection)
for i,sfz in enumerate(ck_sfz["GMSFHM"]):
    net = pd.read_sql("SELECT GMSFHM,XM,WBDH FROM TONGJI.CK_NET \
                          WHERE GMSFHM='%s'"%sfz,con=connection)
    #combine 出发站和达到站 with '-'
    xm_list = net["XM"]
    xm=""
    for names in xm_list:
        if (names):
            xm = names
            break
    xm = xm.decode('utf-8')
    
    
    net_count = Counter(net["WBDH"]).most_common(10)
    net_list=""
    net_times=""
    for item in net_count:
        net_list += item[0].decode('utf-8')
        net_list += ';'
        net_times += str(item[1]).decode('utf-8')
        net_times += ';'
    
    
    query = "INSERT INTO CK_NET_STATIS(GMSFHM,XM,NET_INDEX,NET_TIMES)VALUES ('%s','%s','%s','%s')"%(sfz,xm,\
    net_list,net_times)
    try:
        result= c.execute(query)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        print'error occurs,is %s'%e
    finally:
        print '%i th done'%i

xd_sfz = pd.read_sql("SELECT DISTINCT GMSFHM FROM TONGJI.XD_NET",con=connection)
for i,sfz in enumerate(xd_sfz["GMSFHM"]):
    net = pd.read_sql("SELECT GMSFHM,XM,WBDH FROM TONGJI.XD_NET \
                          WHERE GMSFHM='%s'"%sfz,con=connection)
    #combine 出发站和达到站 with '-'
    xm_list = net["XM"]
    xm=""
    for names in xm_list:
        if (names):
            xm = names
            break
    xm = xm.decode('utf-8')
    
    
    net_count = Counter(net["WBDH"]).most_common(10)
    net_list=""
    net_times=""
    for item in net_count:
        net_list += item[0].decode('utf-8')
        net_list += ';'
        net_times += str(item[1]).decode('utf-8')
        net_times += ';'
    
    
    query = "INSERT INTO XD_NET_STATIS(GMSFHM,XM,NET_INDEX,NET_TIMES)VALUES ('%s','%s','%s','%s')"%(sfz,xm,\
    net_list,net_times)
    try:
        result= c.execute(query)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        print'error occurs,is %s'%e
    finally:
        print '%i th done'%i