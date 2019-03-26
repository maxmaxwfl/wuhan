# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:05:47 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import cx_Oracle
import time
import os
from collections import Counter

connection = cx_Oracle.connect('TONGJI/501430@127.0.0.1:1521/orcl',encoding='utf-8')
c=connection.cursor()


hotel_list = pd.read_sql("SELECT TOP_HOTEL_LIST FROM TONGJI.XD_HOTEL_STATIS",con=connection)
hotel_list = hotel_list.dropna()
xd_hotel = []
for i in range(len(hotel_list)):
    hotels = hotel_list.iloc[i]["TOP_HOTEL_LIST"]
    #分割;
    split_h = hotels.split(";")
    for items in split_h:
        if(items):
            xd_hotel.append(items)

xd_hotel = np.array(xd_hotel)
np.save('hotel_list',xd_hotel)
np.savetxt('hotel_list.txt',xd_hotel,fmt='%s')