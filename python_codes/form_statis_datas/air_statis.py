# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 15:29:59 2018

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
c=connection.cursor()
#tj_con = create_engine('oracle+cx_oracle://TONGJI:501430@127.0.0.1:1521/?service_name=orcl')
ck_sfz = pd.read_sql("SELECT DISTINCT GMSFHM FROM TONGJI.CK_AIR",con=connection)
for i,sfz in enumerate(ck_sfz["GMSFHM"]):
    air = pd.read_sql("SELECT GMSFHM,XM,HKGSDH,DJJCBH,DDJCBH FROM TONGJI.CK_AIR \
                          WHERE GMSFHM='%s'"%sfz,con=connection)
    #combine 出发站和达到站 with '-'
    xm_list = air["XM"]
    xm=""
    for names in xm_list:
        if (names):
            xm = names
            break
    xm = xm.decode('utf-8')
    
    combine = air["DJJCBH"]+'-'+air["DDJCBH"]
    air_count = Counter(combine).most_common(10)
    air_list=""
    air_times=""
    for item in air_count:
        air_list += item[0].decode('utf-8')
        air_list += ';'
        air_times += str(item[1]).decode('utf-8')
        air_times += ';'
    company = Counter(air['HKGSDH']).most_common(10)
    company_list = ""
    company_times = ""
    for item in company:
        company_list += item[0].decode('utf-8')
        company_list += ';'
        company_times += str(item[1]).decode('utf-8')
        company_times += ';'
    query = "INSERT INTO CK_AIR_STATIS(GMSFHM,XM,TOP_ROUTE_LIST,TOP_ROUTE_TIMES,\
    TOP_AIR_COMPANY,TOP_COMPANY_TIMES) VALUES ('%s','%s','%s','%s','%s','%s')"%(sfz,xm,\
    air_list,air_times,company_list,company_times)
    try:
        result= c.execute(query)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        print'error occurs,is %s'%e
    finally:
        print '%i th done'%i
        
xd_sfz = pd.read_sql("SELECT DISTINCT GMSFHM FROM TONGJI.XD_AIR",con=connection)
for i,sfz in enumerate(xd_sfz["GMSFHM"]):
    air = pd.read_sql("SELECT GMSFHM,XM,HKGSDH,DJJCBH,DDJCBH FROM TONGJI.XD_AIR \
                          WHERE GMSFHM='%s'"%sfz,con=connection)
    #combine 出发站和达到站 with '-'
    xm_list = air["XM"]
    xm=""
    for names in xm_list:
        if (names):
            xm = names
            break
    xm = xm.decode('utf-8')
    
    combine = air["DJJCBH"]+'-'+air["DDJCBH"]
    air_count = Counter(combine).most_common(10)
    air_list=""
    air_times=""
    for item in air_count:
        air_list += item[0].decode('utf-8')
        air_list += ';'
        air_times += str(item[1]).decode('utf-8')
        air_times += ';'
    company = Counter(air['HKGSDH']).most_common(10)
    company_list = ""
    company_times = ""
    for item in company:
        company_list += item[0].decode('utf-8')
        company_list += ';'
        company_times += str(item[1]).decode('utf-8')
        company_times += ';'
    query = "INSERT INTO XD_AIR_STATIS(GMSFHM,XM,TOP_ROUTE_LIST,TOP_ROUTE_TIMES,\
    TOP_AIR_COMPANY,TOP_COMPANY_TIMES) VALUES ('%s','%s','%s','%s','%s','%s')"%(sfz,xm,\
    air_list,air_times,company_list,company_times)
    try:
        result= c.execute(query)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        print'error occurs,is %s'%e
    finally:
        print '%i th done'%i
