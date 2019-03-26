# -*- coding: utf-8 -*-
"""
Created on Thu May 31 18:06:28 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import cx_Oracle
import pickle
#person = np.load("d:/python_codes/dahei_features/qzls_list.npy")
#person = person[0:,1]
fr =open("D:/python_codes/ck_1953.pkl",'rb')
ck = pickle.load(fr)
person = list(ck["CK_GMSFHM"])
con_jz = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd',encoding='utf-8')
points = np.load("d:/python_codes/dahei_features/qzls_points.npy")
#test = pd.read_csv("d:/python_codes/dahei_features/pos.txt",delimiter='\t',header=None)
#test = test.replace(0,np.NaN)
#test = test.dropna()


result = np.zeros(500)

for i,sfz in enumerate(person):
    #one = test[test[0]=='%s'%sfz]
    if i<=499:
        query_position="SELECT LONGITUDE,LATITUDE,CP FROM GATOJZ.TB_CFG_XDCZ_DW WHERE SFZH='%s'"%sfz
        pos = pd.read_sql(query_position,con_jz)
        pos = pos.replace(0,np.nan)
        pos = pos.dropna()
        if(len(pos)):
            for j in range(len(pos)):
                lon = pos.iloc[j]["LONGITUDE"]
                lat = pos.iloc[j]["LATITUDE"]
                for center in points:
                    c_lon = center[0]
                    c_lat = center[1]
                    if (c_lon-0.0005<=lon and lon<=c_lon+0.0005 and c_lat-0.0005<=lat and lat<=c_lat+0.0005):
                        result[i] =1
                        break
    print'%i th done'%i