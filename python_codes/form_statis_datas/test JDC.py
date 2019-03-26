# -*- coding: utf-8 -*-
"""
Created on Fri May 18 08:41:29 2018

@author: whjz2
"""

import cx_Oracle
import os
import numpy as np
import pandas as pd
import jieba
import jieba.posseg as pseg
from sqlalchemy import types,create_engine
#set file path
lastdir = os.path.abspath(os.path.dirname(os.getcwd()))
xd_path = os.path.join(lastdir,'xdry_1818.pkl')
ck_path = os.path.join(lastdir,'ck_1953.pkl')
#read data from file
xd=pd.read_pickle(xd_path)
ck=pd.read_pickle(ck_path)
#连接数据库
con = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd',encoding="utf-8")

#构建涉毒人员身份证列表，为了使用sql IN命令加快查询速度 
ck_name = ck['CK_GMSFHM']
record_length = len(ck)
split_number = record_length / 900 +1
bh_list = ["("]*split_number
query1 = "select ZK_GMSFHM ,ZK_XM from GATOJZ.ZKXX_HZC where"
for i,sfz in enumerate(ck_name):
    index= i /900
    yu = i%900
    
    if i==len(ck_name)-1 or yu ==899:
        bh_list[index] += "'%s'"%sfz
        #bh_list[index] += ","
    else:
        bh_list[index] += "'%s'"%sfz
        bh_list[index] += ","
for i in range(split_number):
    bh_list[i]+=')'
    if i == 0:
        query1 += " ZK_GMSFHM IN %s"%bh_list[i]
    else:
        query1 +=" OR ZK_GMSFHM IN %s"%bh_list[i]
        
test = pd.read_sql(query1,con)
