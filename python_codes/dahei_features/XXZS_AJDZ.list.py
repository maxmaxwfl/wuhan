# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:53:54 2018

@author: whjz2
"""

import cx_Oracle
import numpy as np
import pandas as pd
from sqlalchemy import types,create_engine
tj_con1 = cx_Oracle.connect('TONGJI/501430@127.0.0.1:1521/orcl',encoding='utf-8')
tj_con2 = cx_Oracle.connect('JZ_TEST/jz_test@12.14.144.114:1521/whbd',encoding='utf-8')

query1 = "select DISTINCT AJ_BH from SELECT_XXZS"
rec_count1 = pd.read_sql(query1,tj_con1)
dz = []
for i in range(len(rec_count1)):
    temp = rec_count1.iloc[i][0]
    query2 = "select AJ_DZMC from GATOJZ.AJJBXX_JWZH where AJ_TYBH = '%s'" % temp
    rec_count2 = pd.read_sql(query2,tj_con2)
    dz.append(rec_count2.iloc[0][0])

a = np.array(dz)
np.save("QZLS_XXZS",a)