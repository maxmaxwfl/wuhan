# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:46:15 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import os
from collections import Counter
from sklearn.cluster import MeanShift,estimate_bandwidth

files = os.listdir('C:/Users/whjz2/Desktop/dahei/dianwei')
csv_list=[]
for fi in files:
    if fi[-3]=='c':
        csv_list.append(fi)
path = "C:/Users/whjz2/Desktop/dahei/dianwei"

loc=[]
for csv in csv_list:
    filepath = os.path.join(path,csv)        
    dianwei = pd.read_csv(filepath,encoding='utf-8')

    #去除记录中为0的经纬度
    dianwei = dianwei.replace(0,np.nan)
    dianwei = dianwei.replace('0\t',np.nan)
    
    dianwei = dianwei.dropna()
    for i in range(len(dianwei)):
        current=[]
        if type(dianwei.iloc[i][u"经度"])==unicode:
            if dianwei.iloc[i][u"经度"]!='\t':
                current.append(float(dianwei.iloc[i][u"经度"][:-1]))
                current.append(float(dianwei.iloc[i][u"纬度"][:-1]))
                loc.append(current)
        else:
            current.append(float(dianwei.iloc[i][u"经度"]))
            current.append(float(dianwei.iloc[i][u"纬度"]))
            loc.append(current)

bandwidth = estimate_bandwidth(loc,quantile=0.3,n_samples = len(loc))
ms= MeanShift(bandwidth = bandwidth,bin_seeding=True)
ms.fit(loc)
        
labels= ms.labels_
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(labels)
n_cluster = len(labels_unique)
