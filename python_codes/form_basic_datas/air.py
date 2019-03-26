# -*- coding: utf-8 -*-
"""
Created on Sat Feb 03 16:25:56 2018

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

#连接数据库
connection = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd')

#如果要将pandas dataframe写入数据库的话，需要用以下连接方式
tj_con = create_engine('oracle+cx_oracle://TONGJI:501430@127.0.0.1:1521/?service_name=orcl')
#tj_con1 = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd',encoding='utf-8')


#构建涉毒人员身份证列表，为了使用sql IN命令加快查询速度 
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

#构建常住人口身份证列表
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


#查询所有在列表中的数据    
sql_query = "SELECT PAS_ID_NBR,PAS_CHN_NM,AIR_CARR_CD,AIR_SEG_DPT_DT_LCL,AIR_SEG_ARRV_TM_LCL,AIR_SEG_DPT_AIRPT_CD,AIR_SEG_ARRV_AIRPT_CD,AIR_SEG_DPT_TM_LCL\
FROM GATOJZ.TBL_DZXXB_DISPATCH  WHERE PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s"%(ck_sfz_list[0],ck_sfz_list[1],ck_sfz_list[2])
ck_df = pd.read_sql(sql_query,con=connection)

#按身份证号码排序
ck_df = ck_df.sort_values(by=["PAS_ID_NBR"])
#设置列名，并将非数值列转为str型
ck_df.columns = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
col_list = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
railn = {c:types.VARCHAR(ck_df[c].str.len().max())for c in col_list}
#写入新数据库
ck_df.to_sql("ck_air",tj_con,if_exists='append',index=False,dtype=railn)

"""
sql_query = "SELECT PAS_ID_NBR,PAS_CHN_NM,AIR_CARR_CD,AIR_SEG_DPT_DT_LCL,AIR_SEG_ARRV_TM_LCL,AIR_SEG_DPT_AIRPT_CD,AIR_SEG_ARRV_AIRPT_CD,AIR_SEG_DPT_TM_LCL\
 FROM GATOJZ.TBL_DZXXB_DISPATCH_ADD  WHERE PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s"%(ck_sfz_list[0],ck_sfz_list[1],ck_sfz_list[2])
ck_df = pd.read_sql(sql_query,con=connection)
ck_df = ck_df.sort_values(by=["PAS_ID_NBR"])
ck_df.columns = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
col_list = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
railn = {c:types.VARCHAR(ck_df[c].str.len().max())for c in col_list}
ck_df.to_sql("ck_air",tj_con,if_exists='append',index=False,dtype=railn)
"""
"""
sql_query = "SELECT PAS_ID_NBR,PAS_CHN_NM,AIR_CARR_CD,AIR_SEG_DPT_DT_LCL,AIR_SEG_ARRV_TM_LCL,AIR_SEG_DPT_AIRPT_CD,AIR_SEG_ARRV_AIRPT_CD,AIR_SEG_DPT_TM_LCL\
 FROM GATOJZ.TBL_DZXXB_DISPATCH_BAK  WHERE PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s"%(ck_sfz_list[0],ck_sfz_list[1],ck_sfz_list[2])
ck_df = pd.read_sql(sql_query,con=connection)
ck_df = ck_df.sort_values(by=["PAS_ID_NBR"])
ck_df.columns = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
col_list = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
railn = {c:types.VARCHAR(ck_df[c].str.len().max())for c in col_list}
ck_df.to_sql("ck_air",tj_con,if_exists='append',index=False,dtype=railn)
"""
"""
sql_query = "SELECT PAS_ID_NBR,PAS_CHN_NM,AIR_CARR_CD,AIR_SEG_DPT_DT_LCL,AIR_SEG_ARRV_TM_LCL,AIR_SEG_DPT_AIRPT_CD,AIR_SEG_ARRV_AIRPT_CD,AIR_SEG_DPT_TM_LCL\
 FROM GATOJZ.TBL_DZXXB_DISPATCH  WHERE PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s"%(xd_sfz_list[0],xd_sfz_list[1],xd_sfz_list[2])
xd_df = pd.read_sql(sql_query,con=connection)
xd_df = xd_df.sort_values(by=["PAS_ID_NBR"])
xd_df.columns = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
col_list = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
railn = {c:types.VARCHAR(xd_df[c].str.len().max())for c in col_list}
xd_df.to_sql("xd_air",tj_con,if_exists='append',index=False,dtype=railn)
"""
"""
sql_query = "SELECT PAS_ID_NBR,PAS_CHN_NM,AIR_CARR_CD,AIR_SEG_DPT_DT_LCL,AIR_SEG_ARRV_TM_LCL,AIR_SEG_DPT_AIRPT_CD,AIR_SEG_ARRV_AIRPT_CD,AIR_SEG_DPT_TM_LCL\
 FROM GATOJZ.TBL_DZXXB_DISPATCH_ADD  WHERE PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s"%(xd_sfz_list[0],xd_sfz_list[1],xd_sfz_list[2])
xd_df = pd.read_sql(sql_query,con=connection)
xd_df = xd_df.sort_values(by=["PAS_ID_NBR"])
xd_df.columns = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
col_list = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
railn = {c:types.VARCHAR(xd_df[c].str.len().max())for c in col_list}
xd_df.to_sql("xd_air",tj_con,if_exists='append',index=False,dtype=railn)
"""
sql_query = "SELECT PAS_ID_NBR,PAS_CHN_NM,AIR_CARR_CD,AIR_SEG_DPT_DT_LCL,AIR_SEG_ARRV_TM_LCL,AIR_SEG_DPT_AIRPT_CD,AIR_SEG_ARRV_AIRPT_CD,AIR_SEG_DPT_TM_LCL\
 FROM GATOJZ.TBL_DZXXB_DISPATCH_BAK  WHERE PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s OR PAS_ID_NBR IN %s"%(xd_sfz_list[0],xd_sfz_list[1],xd_sfz_list[2])
xd_df = pd.read_sql(sql_query,con=connection)
xd_df = xd_df.sort_values(by=["PAS_ID_NBR"])
xd_df.columns = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
col_list = ['GMSFHM','XM','HKGSDH','CFRQ','DDSJ','DJJCBH','DDJCBH','CFSJ']
railn = {c:types.VARCHAR(xd_df[c].str.len().max())for c in col_list}
xd_df.to_sql("xd_air",tj_con,if_exists='append',index=False,dtype=railn)
