# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 10:09:20 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import cx_Oracle
import time
import os
from sqlalchemy import types,create_engine
#set file path
lastdir = os.path.abspath(os.path.dirname(os.getcwd()))
xd_path = os.path.join(lastdir,'xdry_1818.pkl')
ck_path = os.path.join(lastdir,'ck_1953.pkl')
#read data from file
xd=pd.read_pickle(xd_path)
ck=pd.read_pickle(ck_path)
 
connection = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd')
tj_con = create_engine('oracle+cx_oracle://TONGJI:501430@127.0.0.1:1521/?service_name=orcl')
#tj_con1 = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd',encoding='utf-8')
xd_sfz = xd['XDRY_GMSFHM']
xd_sfz_list=["("]*10
for i,sfz in enumerate(xd_sfz):
    index = i / 900
    yu = (i+1) % 900
    if yu!=0:
        if i!=len(xd_sfz)-1:
            sfz1="'%s'"%sfz
            xd_sfz_list[index] +=sfz1
            xd_sfz_list[index] +=","
        else:
            sfz1="'%s'"%sfz
            xd_sfz_list[index] +=sfz1
    else:
        sfz1="'%s'"%sfz
        xd_sfz_list[index] +=sfz1
   
xd_sfz_list[0]+=")"
xd_sfz_list[1]+=")"
xd_sfz_list[2]+=")"     

ck_sfz = ck['CK_GMSFHM']
ck_sfz_list=["("]*10
for i,sfz in enumerate(ck_sfz):
    index = i / 900
    yu = (i+1) % 900
    if yu!=0:
        if i!=len(ck_sfz)-1:
            sfz1="'%s'"%sfz
            ck_sfz_list[index] +=sfz1
            ck_sfz_list[index] +=","
        else:
            sfz1="'%s'"%sfz
            ck_sfz_list[index] +=sfz1
    else:
        sfz1="'%s'"%sfz
        ck_sfz_list[index] +=sfz1
   
ck_sfz_list[0]+=")"
ck_sfz_list[1]+=")"
ck_sfz_list[2]+=")"
#ck bak
"""
sql_query = "SELECT RENYUAN_GMSFHM,RENYUAN_XM,CHUFA_RQ,CFZ_MC,MDZ_MC,CC_BH FROM GATOJZ.FTPTLGP_BAK  WHERE RENYUAN_GMSFHM IN %s OR RENYUAN_GMSFHM IN %s OR RENYUAN_GMSFHM IN %s"%(ck_sfz_list[0],ck_sfz_list[1],ck_sfz_list[2])
ck_df = pd.read_sql(sql_query,con=connection)
ck_df = ck_df.sort_values(by=["RENYUAN_GMSFHM"])
ck_df.columns = ['GMSFHM','XM','RAIL_CFRQ','RAIL_CFZ','RAIL_MDZ','RAIL_CC']
col_list = ['GMSFHM','XM','RAIL_CFZ','RAIL_MDZ','RAIL_CC']
railn = {c:types.VARCHAR(ck_df[c].str.len().max())for c in col_list}
ck_df.to_sql("CK_RAIL",tj_con,if_exists='append',index=False,dtype=railn)
"""
#ck add
"""
sql_query = "SELECT RENYUAN_GMSFHM,RENYUAN_XM,CHUFA_RQ,CFZ_MC,MDZ_MC,CC_BH FROM GATOJZ.FTPTLGP_ADD  WHERE RENYUAN_GMSFHM IN %s OR RENYUAN_GMSFHM IN %s OR RENYUAN_GMSFHM IN %s"%(ck_sfz_list[0],ck_sfz_list[1],ck_sfz_list[2])
ck_df = pd.read_sql(sql_query,con=connection)
ck_df = ck_df.sort_values(by=["RENYUAN_GMSFHM"])
ck_df.columns = ['GMSFHM','XM','RAIL_CFRQ','RAIL_CFZ','RAIL_MDZ','RAIL_CC']
col_list = ['GMSFHM','XM','RAIL_CFZ','RAIL_MDZ','RAIL_CC']
railn = {c:types.VARCHAR(ck_df[c].str.len().max())for c in col_list}
ck_df.to_sql("CK_RAIL",tj_con,if_exists='append',index=False,dtype=railn)
"""
#xd add
"""
sql_query = "SELECT RENYUAN_GMSFHM,RENYUAN_XM,CHUFA_RQ,CFZ_MC,MDZ_MC,CC_BH FROM GATOJZ.FTPTLGP_ADD  WHERE RENYUAN_GMSFHM IN %s OR RENYUAN_GMSFHM IN %s OR RENYUAN_GMSFHM IN %s"%(xd_sfz_list[0],xd_sfz_list[1],xd_sfz_list[2])
xd_df = pd.read_sql(sql_query,con=connection)
xd_df = xd_df.sort_values(by=["RENYUAN_GMSFHM"])
xd_df.columns = ['GMSFHM','XM','RAIL_CFRQ','RAIL_CFZ','RAIL_MDZ','RAIL_CC']
col_list = ['GMSFHM','XM','RAIL_CFZ','RAIL_MDZ','RAIL_CC']
railn = {c:types.VARCHAR(xd_df[c].str.len().max())for c in col_list}
xd_df.to_sql("XD_RAIL",tj_con,if_exists='append',index=False,dtype=railn)
"""
#xd bak
sql_query = "SELECT RENYUAN_GMSFHM,RENYUAN_XM,CHUFA_RQ,CFZ_MC,MDZ_MC,CC_BH FROM GATOJZ.FTPTLGP_BAK  WHERE RENYUAN_GMSFHM IN %s OR RENYUAN_GMSFHM IN %s OR RENYUAN_GMSFHM IN %s"%(xd_sfz_list[0],xd_sfz_list[1],xd_sfz_list[2])
xd_df = pd.read_sql(sql_query,con=connection)
xd_df = xd_df.sort_values(by=["RENYUAN_GMSFHM"])
xd_df.columns = ['GMSFHM','XM','RAIL_CFRQ','RAIL_CFZ','RAIL_MDZ','RAIL_CC']
col_list = ['GMSFHM','XM','RAIL_CFZ','RAIL_MDZ','RAIL_CC']
railn = {c:types.VARCHAR(xd_df[c].str.len().max())for c in col_list}
xd_df.to_sql("XD_RAIL",tj_con,if_exists='append',index=False,dtype=railn)
