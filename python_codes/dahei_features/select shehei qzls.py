# -*- coding: utf-8 -*-
"""
Created on Wed May 16 14:35:31 2018

@author: whjz2
"""

import cx_Oracle
import numpy as np
import pandas as pd
from sqlalchemy import types,create_engine

tj_con1 = cx_Oracle.connect('TONGJI/501430@127.0.0.1:1521/orcl',encoding='utf-8')
#3人3起部分
query = "select AJ_BH,count(*) from TONGJI.SH_QZLS_LIST group by TONGJI.SH_QZLS_LIST.AJ_BH"
rec_count = pd.read_sql(query,tj_con1)
three = rec_count[rec_count["COUNT(*)"]>=3]
aj_list = list(three["AJ_BH"])

record =pd.DataFrame()
for aj in aj_list:
    query1 = "select * from TONGJI.SH_QZLS_LIST where AJ_BH='%s'"%aj
    one_case = pd.read_sql(query1,tj_con1)
    print_flag = 0 
    xm_list = list(one_case["XM"])
    for name in xm_list:
        query_n = "select * from TONGJI.SH_QZLS_LIST where XM='%s'"%name
        name_case = pd.read_sql(query_n,tj_con1)
        if(len(name_case)>=3):
            one_case= pd.concat([one_case,name_case])
            print_flag=1
    if(print_flag==1):
        record=pd.concat([record,one_case])

#关键词部分：拟定关键词 "%借款%" "%非法拘禁%" "%费%" "%装修材料%" "%沙%石%" "%砂%" "%水泥%" "%工地%"
# "%承包%" "%啤酒%" "%施工%"
        
query_k = "select * from TONGJI.SH_QZLS_LIST where AJ_JYAQ LIKE '%借款%' or AJ_JYAQ LIKE '%非法拘禁%'\
OR AJ_JYAQ LIKE '%费%' OR AJ_JYAQ LIKE '%装修材料%' OR AJ_JYAQ LIKE '%沙%石%' OR AJ_JYAQ LIKE '%砂%'\
OR AJ_JYAQ LIKE '%水泥%' OR AJ_JYAQ LIKE '%工地%' OR AJ_JYAQ LIKE '%承包%' OR AJ_JYAQ LIKE '%啤酒%'\
OR AJ_JYAQ LIKE '%施工%'"
key = pd.read_sql(query_k,tj_con1)

all_rec= pd.concat([record,key])
all_rec=all_rec.drop_duplicates()

all_rec["XM"]=all_rec["XM"].str.decode("utf-8")
all_rec["AJ_MC"]=all_rec["AJ_MC"].str.decode("utf-8")
all_rec["AJ_JYAQ"]=all_rec["AJ_JYAQ"].str.decode("utf-8")

tj_con = create_engine('oracle+cx_oracle://TONGJI:501430@127.0.0.1:1521/?service_name=orcl',encoding="utf-8")
all_rec.to_sql("SELECT_QZLS",tj_con,if_exists='append',index=False)
