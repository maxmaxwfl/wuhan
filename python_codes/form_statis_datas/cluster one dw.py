# -*- coding: utf-8 -*-
"""
Created on Mon Mar 05 09:19:52 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import cx_Oracle
import time
import os
from collections import Counter
from sqlalchemy import types,create_engine

from sklearn.cluster import MeanShift,estimate_bandwidth
from sklearn import metrics

import traceback

#读取涉毒人员身份证列表
lastdir = os.path.abspath(os.path.dirname(os.getcwd()))
xd_path = os.path.join(lastdir,'xdry_1818.pkl')
xd = pd.read_pickle(xd_path)

#connection = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd',encoding='utf-8')

#画出聚类点所用包
import matplotlib.pyplot as plt
from itertools import cycle

center_1 = []
center_2 = []
center_3 = []
center_4 = []
center_5 = []
center_6 = []

tj_con = cx_Oracle.connect('TONGJI/501430@127.0.0.1:1521/orcl',encoding='utf-8')


for i,sfz in enumerate(xd["XDRY_GMSFHM"]):
    query="select SFZH,LONGTITUDE,LATITUDE,CP from TONGJI.XD_DW_C where SFZH='%s'"%sfz
    dw = pd.read_sql(query,con=tj_con)
    #把电围数据中的"0"替换为NaN
    dw = dw.replace(0,np.nan)
    #删除为NaN的数据
    dw = dw.dropna()
    dw["CP"] = dw["CP"].astype(str)
    
    pos_1 = []
    pos_2 = []
    pos_3 = []
    pos_4 = []
    pos_5 = []
    pos_6 = []
    if len(dw)>30000:
        records = 30000
    else:
        records = len(dw)
    for j in range(records):
        #将一天分为6个时间切片 深夜0-4,清晨5-7,上午8-11,中午12-13,下午13-18，傍晚19-24 
        lon = dw.iloc[j][1]
        lat = dw.iloc[j][2]
        s_time = int(dw.iloc[j]["CP"][-2:])
        if(s_time>=0 and s_time<=4):
            current=[]
            current.append(lon)
            current.append(lat)
            pos_1.append(current)
        elif(s_time>=5 and s_time<=7):
            current=[]
            current.append(lon)
            current.append(lat)
            pos_2.append(current)
        elif(s_time>=8 and s_time<=11):
            current=[]
            current.append(lon)
            current.append(lat)
            pos_3.append(current)
        elif(s_time>=12 and s_time<=13):
            current=[]
            current.append(lon)
            current.append(lat)
            pos_4.append(current)
        elif(s_time>=14 and s_time<=18):
            current=[]
            current.append(lon)
            current.append(lat)
            pos_5.append(current)
        elif(s_time>=19 and s_time<=23):
            current=[]
            current.append(lon)
            current.append(lat)
            pos_6.append(current)
    try:
        bandwidth = estimate_bandwidth(pos_1,quantile=0.2,n_samples = len(pos_1))
        ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
        ms.fit(pos_1)
            
        labels= ms.labels_
        cluster_centers = ms.cluster_centers_
        labels_unique = np.unique(labels)
        n_cluster = len(labels_unique)
        for k in range(n_cluster):
            center_1.append(pos_1[k])
        
        bandwidth = estimate_bandwidth(pos_2,quantile=0.2,n_samples = len(pos_2))
        ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
        ms.fit(pos_2)
            
        labels= ms.labels_
        cluster_centers = ms.cluster_centers_
        labels_unique = np.unique(labels)
        n_cluster = len(labels_unique)
        for k in range(n_cluster):
            center_2.append(pos_2[k])
        
        bandwidth = estimate_bandwidth(pos_3,quantile=0.2,n_samples = len(pos_3))
        ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
        ms.fit(pos_3)
            
        labels= ms.labels_
        cluster_centers = ms.cluster_centers_
        labels_unique = np.unique(labels)
        n_cluster = len(labels_unique)
        for k in range(n_cluster):
            center_3.append(pos_3[k])
        
        bandwidth = estimate_bandwidth(pos_4,quantile=0.2,n_samples = len(pos_4))
        ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
        ms.fit(pos_4)
            
        labels= ms.labels_
        cluster_centers = ms.cluster_centers_
        labels_unique = np.unique(labels)
        n_cluster = len(labels_unique)
        for k in range(n_cluster):
            center_4.append(pos_4[k])
        
        bandwidth = estimate_bandwidth(pos_5,quantile=0.2,n_samples = len(pos_5))
        ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
        ms.fit(pos_5)
            
        labels= ms.labels_
        cluster_centers = ms.cluster_centers_
        labels_unique = np.unique(labels)
        n_cluster = len(labels_unique)
        for k in range(n_cluster):
            center_5.append(pos_5[k])
        
        bandwidth = estimate_bandwidth(pos_6,quantile=0.2,n_samples = len(pos_6))
        ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
        ms.fit(pos_6)
            
        labels= ms.labels_
        cluster_centers = ms.cluster_centers_
        labels_unique = np.unique(labels)
        n_cluster = len(labels_unique)
        for k in range(n_cluster):
            center_6.append(pos_6[k])
    except:
        pass
    print "%i %i th done"%(i,j)
    
    print '%i th done'%i
#center_1 = np.array(center_1)
#np.save('d:/python_codes/datas/center_1_1.npy',center_1)
#center_2 = np.array(center_2)
#np.save('d:/python_codes/datas/center_2_1.npy',center_2)
#center_3 = np.array(center_3)
#np.save('d:/python_codes/datas/center_3_1.npy',center_3)
#center_4 = np.array(center_4)
#np.save('d:/python_codes/datas/center_4_1.npy',center_4)
#center_5 = np.array(center_5)
#np.save('d:/python_codes/datas/center_5_1.npy',center_5)
#center_6 = np.array(center_6)
#np.save('d:/python_codes/datas/center_6_1.npy',center_6)
"""
#获取经纬度信息
query="select SFZH,LONGTITUDE,LATITUDE,CP,LAI from TONGJI.XD_DW_C where SFZH='420114198012075455'"
dw = pd.read_sql(query,con=tj_con)
#将dataframe中的0替换为np.nan
dw = dw.replace(0,np.nan)
#去除dataframe中的nan
dw = dw.dropna()
dw["CP"] = dw["CP"].astype(str)
pos_1 = []
pos_2 = []
pos_3 = []
pos_4 = []
pos_5 = []
pos_6 = []
if len(dw)>30000:
    records = 30000
else:
    records = len(dw)
for j in range(records):
    #将一天分为6个时间切片 深夜0-4,清晨5-7,上午8-11,中午12-13,下午13-18，傍晚19-24 
    lon = dw.iloc[j][1]
    lat = dw.iloc[j][2]
    s_time = int(dw.iloc[j]["CP"][-2:])
    if(s_time>=0 and s_time<=4):
        current=[]
        current.append(lon)
        current.append(lat)
        pos_1.append(current)
    elif(s_time>=5 and s_time<=7):
        current=[]
        current.append(lon)
        current.append(lat)
        pos_2.append(current)
    elif(s_time>=8 and s_time<=11):
        current=[]
        current.append(lon)
        current.append(lat)
        pos_3.append(current)
    elif(s_time>=12 and s_time<=13):
        current=[]
        current.append(lon)
        current.append(lat)
        pos_4.append(current)
    elif(s_time>=14 and s_time<=18):
        current=[]
        current.append(lon)
        current.append(lat)
        pos_5.append(current)
    elif(s_time>=19 and s_time<=23):
        current=[]
        current.append(lon)
        current.append(lat)
        pos_6.append(current)
import matplotlib.pyplot as plt
from itertools import cycle

bandwidth = estimate_bandwidth(pos_3,quantile=0.2,n_samples = len(pos_3))
ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
ms.fit(pos_3)
    
labels= ms.labels_
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(labels)
n_cluster = len(labels_unique)
for k in range(n_cluster):
    center_3.append(pos_3[k])
"""

#画图用
"""
pos_3 =np.array(pos_3)
plt.figure(1)
plt.clf()
colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmykbgrcmyk')
for k,col in zip(range(n_cluster),colors):
    my_members = labels==k
    cluster_center =cluster_centers[k]
    plt.plot(pos_3[my_members,0],pos_3[my_members,1],col+'.')
    plt.plot(cluster_center[0],cluster_center[1],'o',markerfacecolor=col,
             markeredgecolor='k',markersize=4)
    
plt.show()
"""    
"""
bandwidth = estimate_bandwidth(pos_2,quantile=0.2,n_samples = len(pos_2))
ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
ms.fit(pos_2)
    
labels= ms.labels_
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(labels)
n_cluster = len(labels_unique)


bandwidth = estimate_bandwidth(pos_3,quantile=0.2,n_samples = len(pos_3))
ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
ms.fit(pos_3)
    
labels= ms.labels_
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(labels)
n_cluster = len(labels_unique)


bandwidth = estimate_bandwidth(pos_4,quantile=0.2,n_samples = len(pos_4))
ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
ms.fit(pos_4)
    
labels= ms.labels_
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(labels)
n_cluster = len(labels_unique)


bandwidth = estimate_bandwidth(pos_5,quantile=0.2,n_samples = len(pos_5))
ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
ms.fit(pos_5)
    
labels= ms.labels_
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(labels)
n_cluster = len(labels_unique)


bandwidth = estimate_bandwidth(pos_6,quantile=0.2,n_samples = len(pos_6))
ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
ms.fit(pos_6)
    
labels= ms.labels_
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(labels)
n_cluster = len(labels_unique)
"""
    



"""

"""

"""            
colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmykbgrcmyk')
for k,col in zip(range(n_cluster),colors):
    my_members = labels==k
    cluster_center =cluster_centers[k]
    plt.plot(pos_6[my_members,0],pos_6[my_members,1],col+'.')
    plt.plot(cluster_center[0],cluster_center[1],'o',markerfacecolor=col,
             markeredgecolor='k',markersize=4)
plt.show()

center=[]
for i,sfz in enumerate(xd["XDRY_GMSFHM"]):
    if i>1000 and i<=1999:
        posi_set=[]
        query="select SFZH,LONGTITUDE,LATITUDE,CP from TONGJI.XD_DW where SFZH='%s'"%sfz
        dw = pd.read_sql(query,con=tj_con)
        dw = dw.replace(0,np.nan)
        dw = dw.dropna()
        if(len(dw)):
            if(len(dw)>50000):
                for j in range(50000):
                    posi = []
                    lon = dw.iloc[j][1]
                    lat = dw.iloc[j][2]
                    posi.append(lon)
                    posi.append(lat)
                    posi_set.append(posi)
            else:
                for j in range(len(dw)):
                    posi = []
                    lon = dw.iloc[j][1]
                    lat = dw.iloc[j][2]
                    posi.append(lon)
                    posi.append(lat)
                    posi_set.append(posi)
            try:
                bandwidth = estimate_bandwidth(posi_set,quantile=0.2,n_samples = len(posi_set))
                ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
                ms.fit(posi_set)
        
                labels= ms.labels_
                cluster_centers = ms.cluster_centers_
                labels_unique = np.unique(labels)
                n_cluster = len(labels_unique)
                for k in range(n_cluster):
                    center.append(cluster_centers[k])
            except:
                traceback.print_exc()
    print '%i th done'%i
center = np.array(center)
np.save('d:/python_codes/datas/cluster_center1.npy',center)
    #s_time = time.time()


bandwidth = estimate_bandwidth(posi_set,quantile=0.2,n_samples = len(posi_set))
ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
ms.fit(posi_set)

labels= ms.labels_
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(labels)
n_cluster = len(labels_unique)

import matplotlib.pyplot as plt
from itertools import cycle

posi_set =np.array(posi_set)
plt.figure(1)
plt.clf()
colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmykbgrcmyk')
for k,col in zip(range(n_cluster),colors):
    my_members = labels==k
    cluster_center =cluster_centers[k]
    plt.plot(posi_set[my_members,0],posi_set[my_members,1],col+'.')
    plt.plot(cluster_center[0],cluster_center[1],'o',markerfacecolor=col,
             markeredgecolor='k',markersize=4)
plt.show()
##############################
#comute clustering with MeanShift

    if(posi_set):
        bandwidth = estimate_bandwidth(posi_set,quantile=0.2,n_samples = len(posi_set))
        ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
        ms.fit(posi_set)

        labels= ms.labels_
        cluster_centers = ms.cluster_centers_
        labels_unique = np.unique(labels)
        n_cluster = len(labels_unique)
        for k in range(n_cluster):
            centers.append(list(cluster_centers[k]))
    print'%i th done'%i
    centers = np.array(centers) 
    np.save('cluster_center',centers)
    #e_time = time.time()
    #t_time = e_time - s_time


####################3##########

import matplotlib.pyplot as plt
from itertools import cycle

posi_set =np.array(posi_set)
plt.figure(1)
plt.clf()
colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmykbgrcmyk')
for k,col in zip(range(n_cluster),colors):
    my_members = labels==k
    cluster_center =cluster_centers[k]
    plt.plot(posi_set[my_members,0],posi_set[my_members,1],col+'.')
    plt.plot(cluster_center[0],cluster_center[1],'o',markerfacecolor=col,
             markeredgecolor='k',markersize=4)
plt.show()
"""