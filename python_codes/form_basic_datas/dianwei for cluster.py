# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 11:20:10 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import cx_Oracle
import time
import os
from collections import Counter
from sqlalchemy import types,create_engine

#上级目录
lastdir = os.path.abspath(os.path.dirname(os.getcwd()))
ck_path = os.path.join(lastdir,'ck_1953.pkl')
xd_path = os.path.join(lastdir,'xdry_1818.pkl')

ck = pd.read_pickle(ck_path)
xd = pd.read_pickle(xd_path)

connection = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd',encoding='utf-8')
connection1 = cx_Oracle.connect('tongji/501430@127.0.0.1:1521/orcl',encoding='utf-8')
tj_con = create_engine('oracle+cx_oracle://TONGJI:501430@127.0.0.1:1521/?service_name=orcl')
"""
for i,sfz in enumerate(ck["CK_GMSFHM"]):
    query = "SELECT SFZH,BEGINTIME,EVENT,USERNUM,HOMEAREA,RELATENUM,RELATEHOMEAC,\
    IMSI,IMEI,CURAREA,NEID,LAI,CI,LONGITUDE,LATITUDE,OLDLAI,OLDCI,OLDLONGITUDE,OLDLATITUDE \
    FROM GATOJZ.TB_CFG_XDCZ_DW WHERE SFZH='%s'"%sfz
    dw = pd.read_sql(query,con=connection)
    dw.columns = ['SFZH','BEGINTIME','EVENT','USERNUM','HOMEAREA','RELATENUM','RELATEHOMEAC','IMSI',\
                  'IMEI','CURAREA','NEID','LAI','CI','LONGITUDE','LATITUDE','OLDLAI','OLDCI',\
                  'OLDLONGITUDE','OLDLATITUDE']
    col_list= ['SFZH','EVENT','USERNUM','HOMEAREA','RELATENUM','RELATEHOMEAC','IMSI',\
                  'IMEI','CURAREA','NEID','CI','OLDCI']
    dw_col = {c:types.VARCHAR(dw[c].str.len().max())for c in col_list}
    dw.to_sql("CK_DW",tj_con,if_exists='append',index=False,dtype=dw_col)
    print '%i ck th complete'%i
"""
for i,sfz in enumerate(xd["XDRY_GMSFHM"]):
    if i<=1000:
        query = "SELECT SFZH,LONGITUDE,LATITUDE,CP,LAI\
        FROM GATOJZ.TB_CFG_XDCZ_DW WHERE SFZH='%s'"%sfz
        dw = pd.read_sql(query,con=connection)
        dw.columns = ['SFZH','LONGTITUDE','LATITUDE','CP','LAI']
        col_list= ['SFZH']
        dw_col = {c:types.VARCHAR(dw[c].str.len().max())for c in col_list}
        dw.to_sql("xd_dw_c",tj_con,if_exists='append',index=False,dtype=dw_col)
        print '%i th xd complete'%i