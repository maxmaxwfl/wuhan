# -*- coding: utf-8 -*-
"""
Created on Fri Mar 09 08:36:07 2018

@author: whjz2
"""
import pandas as pd
import numpy as np
import cx_Oracle
import time
import os
import numpy as np
center= np.load("d:/python_codes/datas/cluster_center.npy")
from sklearn.cluster import MeanShift,estimate_bandwidth
from sklearn import metrics

"""
posi_set=[]
tj_con = cx_Oracle.connect('TONGJI/501430@127.0.0.1:1521/orcl',encoding='utf-8')
query="select SFZH,LONGITUDE,LATITUDE from TONGJI.XD_DW where SFZH='420106198101094084'"
dw = pd.read_sql(query,con=tj_con)
dw = dw.replace(0,np.nan)
dw = dw.dropna()
for j in range(len(dw)):
    posi = []
    lon = dw.iloc[j][1]
    lat = dw.iloc[j][2]
    posi.append(lon)
    posi.append(lat)
    posi_set.append(posi)
"""
center_1= np.load("d:/python_codes/datas/center_1_1.npy")
center_2= np.load("d:/python_codes/datas/center_2_1.npy")
center_3= np.load("d:/python_codes/datas/center_3_1.npy")
center_4= np.load("d:/python_codes/datas/center_4_1.npy")
center_5= np.load("d:/python_codes/datas/center_5_1.npy")
center_6= np.load("d:/python_codes/datas/center_6_1.npy")
whole_center = np.vstack([center_1,center_2,center_3,center_4,center_5,center_6])
print "data combined"

bandwidth = estimate_bandwidth(whole_center,quantile=0.2,n_samples = len(whole_center))
ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
ms.fit(whole_center)
        
labels= ms.labels_
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(labels)
n_cluster = len(labels_unique)

cluster_centers = np.array(cluster_centers)

"""
import matplotlib.pyplot as plt
from itertools import cycle

center =np.array(center)
center_6 = np.array(center_6)
plt.figure(1)
plt.clf()
plt.xlim(109,116)
plt.ylim(29,33)
colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmykbgrcmyk')
for k,col in zip(range(n_cluster),colors):
    my_members = labels==k
    cluster_center =cluster_centers[k]
    plt.plot(center_6[my_members,0],center_6[my_members,1],col+'.')
    plt.plot(cluster_center[0],cluster_center[1],'o',markerfacecolor=col,
             markeredgecolor='k',markersize=4)
plt.show()
"""