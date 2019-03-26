# -*- coding: utf-8 -*-
"""
Created on Mon Mar 05 15:15:56 2018

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

query="SELECT GMSFHM,TOP_ROUTE_LIST,TOP_ROUTE_TIMES FROM TONGJI.CK_RAIL_STATIS"
ck_rail_s = pd.read_sql(query,con=connection)
ck_sfz=ck_rail_s["GMSFHM"]

lastdir = os.path.abspath(os.path.dirname(os.getcwd()))
savepath =os.path.join(lastdir,"datas/cksfz.pkl")
ck_sfz.to_pickle(savepath)

query1="SELECT GMSFHM,TOP_ROUTE_LIST,TOP_ROUTE_TIMES FROM TONGJI.XD_RAIL_STATIS"
xd_rail_s = pd.read_sql(query1,con=connection)
xd_sfz=xd_rail_s["GMSFHM"]
savepath1 =os.path.join(lastdir,"datas/xdsfz.pkl")
xd_sfz.to_pickle(savepath1)
#get the context dict
rail_doc=[]
for i in range(len(ck_rail_s)):
    route = ck_rail_s.iloc[i]["TOP_ROUTE_LIST"]
    times = ck_rail_s.iloc[i]["TOP_ROUTE_TIMES"]
    route_s = route.split(";")
    times_s = times.split(";")
    line = dict()
    for j in range(len(route_s)-1):
        ti = int(times_s[j])
        line[route_s[j]]=ti
    rail_doc.append(line)
for i in range(len(xd_rail_s)):
    route = xd_rail_s.iloc[i]["TOP_ROUTE_LIST"]
    times = xd_rail_s.iloc[i]["TOP_ROUTE_TIMES"]
    route_s = route.split(";")
    times_s = times.split(";")
    line = dict()
    for j in range(len(route_s)-1):
        ti = int(times_s[j])
        line[route_s[j]]=ti
    rail_doc.append(line)
#vectorize
from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()
array = vec.fit_transform(rail_doc).toarray()
array = np.array(array)
np.save('d:/python_codes/datas/railroute_vector',array)