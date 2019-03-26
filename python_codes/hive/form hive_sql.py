# -*- coding: utf-8 -*-
"""
Created on Wed May 30 19:17:23 2018

@author: whjz2
"""

import numpy as np
import pandas as pd

data = np.load("d:/python_codes/dahei_features/QZLS_list.npy")
data = list(data[0:,1])
record_length = len(data)
split_number = record_length / 900 +1
bh_list = ["("]*split_number
query1 = "select sfzh,msisdn from tb_sub_realname_new where"
for i,bh in enumerate(data):
    index= i /900
    yu = i%900
    
    if i==len(data)-1 or yu ==899:
        bh_list[index] += "'%s'"%bh
        #bh_list[index] += ","
    else:
        bh_list[index] += "'%s'"%bh
        bh_list[index] += ","
for i in range(split_number):
    bh_list[i]+=')'
    if i == 0:
        query1 += " sfzh IN %s"%bh_list[i]
    else:
        query1 +=" OR sfzh IN %s"%bh_list[i]
"""
"""
bh_list = "("
for i,bh in enumerate(data):
    if i< len(data)-1:
        bh_list += "'%s'"%bh
        bh_list += ","
    else:
        bh_list += "'%s'"%bh
bh_list +=")"
query1+=";"