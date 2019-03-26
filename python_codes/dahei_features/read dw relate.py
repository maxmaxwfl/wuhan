# -*- coding: utf-8 -*-
"""
Created on Fri Jun 01 10:18:01 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
#import cx_Oracle
#import pickle
person = np.load("d:/python_codes/dahei_features/qzls_list.npy")
person = person[0:,1]

numbers = pd.read_csv("d:/python_codes/dahei_features/numbers1.txt",header=None)
number_list =list(numbers[0])

relate = pd.read_csv("d:/python_codes/dahei_features/relate.txt",delimiter='\t',header=None)
relate = relate.dropna()

result = np.zeros(len(person))

for i,sfz in enumerate(person):
    one = relate[relate[0]=='%s'%sfz]
    for j in range(len(one)):
        p_num = one.iloc[j][1]
        if(len(p_num)==11 and p_num.isdigit()==True):
            int_p = long(p_num)
            if int_p in number_list:
                result[i] = 1
                break
    print("%i th done"%i)