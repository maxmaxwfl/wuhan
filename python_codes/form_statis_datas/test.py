# -*- coding: utf-8 -*-
"""
Created on Mon May 21 08:46:11 2018

@author: whjz2
"""
import numpy as np
xd = np.load("D:/python_codes/form_statis_datas/datas/xd_featureandi_600.npy")
ck = np.load("D:/python_codes/form_statis_datas/datas/ck_featureandi_600.npy")

xd_sum = np.sum(xd)
ck_sum = np.sum(ck)
print float(xd_sum)/601
print float(ck_sum)/601