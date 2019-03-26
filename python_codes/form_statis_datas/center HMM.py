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

#读取D:/python_codes/xdry_1818.pkl 
lastdir = os.path.abspath(os.path.dirname(os.getcwd()))
xd_path = os.path.join(lastdir,'xdry_1818.pkl')
xd = pd.read_pickle(xd_path)

#connection = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd',encoding='utf-8')
import matplotlib.pyplot as plt
from itertools import cycle

center_1 = []
center_2 = []
center_3 = []
center_4 = []
center_5 = []
center_6 = []

tj_con = cx_Oracle.connect('TONGJI/501430@127.0.0.1:1521/orcl',encoding='utf-8')
#sfz =xd.iloc[2]["XDRY_GMSFHM"]
#query="select SFZH,LONGITUDE,LATITUDE from TONGJI.XD_DW where SFZH='%s'"%sfz
#dw = pd.read_sql(query,con=tj_con)
#reader = pd.read_sql(query,con=tj_con,chunksize=10000000)
#for i,chunk in enumerate(reader):
#    if i<=1000000:
#        df=chunk

#仅测试一个人
query="select SFZH,LONGTITUDE,LATITUDE,CP,LAI from TONGJI.XD_DW_C where SFZH='420114198012075455'"
dw = pd.read_sql(query,con=tj_con)
#将dataframe中的0替换为np.nan
dw = dw.replace(0,np.nan)
#去除dataframe中的nan
dw = dw.dropna()
#按时间排序
dw = dw.sort_values(by='CP')
pos=[]
for i in range(len(dw)):
    current=[]
    current.append(dw.iloc[i][1])
    current.append(dw.iloc[i][2])
    pos.append(current)
#meanshift 聚类过程
bandwidth = estimate_bandwidth(pos,quantile=0.2,n_samples = len(pos))
ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
ms.fit(pos)

#每一个点属于哪一类    
labels= ms.labels_
#聚类中心
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(labels)
n_cluster = len(labels_unique)

#提取该人员区快信息，并编码如区块信息是11、12，则重新编码为0,1
lai = set(dw["LAI"])
state = dict()
#利用字典对区块编码
for i,item in enumerate(lai):
    state[item]=i
lai_list = list(dw["LAI"])
lai_index = []
for item in lai_list:
    lai_index.append(state[item])

#基于位置信息构建隐马尔科夫模型的三要素pi,A,B,重点！！！
n_states = len(lai)
n_observe = n_cluster

A = np.zeros((n_states,n_states))
for i in range(len(lai_index)-1):
    font_state = lai_index[i]
    after_state = lai_index[i+1]
    A[font_state][after_state]+=1
for i in range(n_states):
    A[i] = A[i]/A[i].sum()

B = np.zeros((n_states,n_cluster))
for i in range(len(lai_index)-1):
    state = lai_index[i]
    observe = labels[i]
    B[state][observe]+=1
for i in range(n_states):
    B[i] = B[i]/B[i].sum()
pi = np.ones(n_states)/n_states

#HMM前向算法
def forward(obs_seq):
    N = A.shape[0]
    T = len(obs_seq)
    F = np.zeros((N,T))
    F[:,0] = pi * B[:,obs_seq[0]]
    for t in range(1,T):
        for n in range(N):
            F[n,t] = np.dot(F[:,t-1],(A[:,n]))* B[n,obs_seq[t]]
    return F
#对于每个可能的候选地点计算概率

top1=0
top3=0
for j in range(200):
    label_50 = labels[j:j+50]
    true_label = labels[j+50]
    predict=[]
    for i in range(n_observe):
        label_test = np.append(label_50,i)    
    #test = np.array([0,0,0,0,0,0,1,0,1,1,2,1,1,2,2,2,2,2,1,1,0,0,0,0])
        #label_test = np.append(label_test,i)
        F = forward(label_test)
        one_predict = np.sum(F[:,-1])        
        predict.append(one_predict)
    max_index =np.argsort(predict)[::-1]
    top1_index = max_index[0]
    top3_index = max_index[0:3]
    if true_label==top1_index:
        top1+=1
    if true_label in top3_index:
        top3+=1
