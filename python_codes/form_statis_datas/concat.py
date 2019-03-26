# -*- coding: utf-8 -*-
"""
Created on Fri May 18 10:00:05 2018

@author: whjz2
"""

import numpy as np
xd_feature = np.load("D:/python_codes/form_statis_datas/datas/xd_feature12_400.npy")
ck_feature = np.load("D:/python_codes/form_statis_datas/datas/ck_feature12_400.npy")

xd_feature1 = np.load("D:/python_codes/form_statis_datas/datas/xd_featureandi_400.npy")
ck_feature1 = np.load("D:/python_codes/form_statis_datas/datas/ck_featureandi_400.npy")
xd_all =np.hstack([xd_feature,xd_feature1])
ck_all =np.hstack([ck_feature,ck_feature1])

np.save("xd_feature13_400",xd_all)
np.save("ck_feature13_400",ck_all)