# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 10:52:35 2018

@author: whjz2
"""

import numpy as np
from sklearn import preprocessing
#from sklearn.decomposition import PCA
from matplotlib.mlab import PCA
xd_feature = np.load("D:/python_codes/form_statis_datas/xd_feature11_600.npy")
ck_feature = np.load("D:/python_codes/form_statis_datas/ck_feature11_600.npy")

xd = []
ck = []
for i in range(len(xd_feature)):
    one_feature=[]
    for j in range(len(xd_feature[i])):
        if j>=1:
            one_feature.append(int(xd_feature[i][j]))
    if (np.sum(one_feature)>0):
        xd.append(one_feature)
    
for i in range(len(ck_feature)):
    one_feature=[]
    for j in range(len(ck_feature[i])):
        if j>=1:
            one_feature.append(int(ck_feature[i][j]))
    if (np.sum(one_feature)>0):
        ck.append(one_feature)

feature1_xd_sum=0
feature1_ck_sum=0
for i in range(len(xd)):
    if(xd[i][0]==1 or xd[i][1]==1 or xd[i][2]==1):
        feature1_xd_sum+=1
for i in range(len(ck)):
    if(ck[i][0]==1 or ck[i][1]==1 or ck[i][2]==1):
        feature1_ck_sum+=1

print float(feature1_xd_sum)/len(xd)*100,'%'
print float(feature1_ck_sum)/len(ck)*100,'%'
        