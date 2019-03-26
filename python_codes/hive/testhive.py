# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:36:00 2018

@author: whjz2
"""

#import pyhs2 
#host_list = ['12.14.144.172','12.14.144.171','12.14.144.170']
#con= pyhs2.connect(host="12.14.144.170",port=24002,authMechanism='NOSASL')

from impala.dbapi import connect

conn = connect(host="12.14.144.170",port=21066)
#conn = connect(host=host_list[1],port=24002)
#conn = connect(host=host_list[2],port=24002)
cursor = conn.cursor()
cursor.execute('show tables')
results = cursor.fetchall()
#test = pyhs2.connect(host="12.14.144.172",port=24002,user='hive',authMechanism='NOSASL')
#cusor = pyhs2.connect(host="12.14.144.172",port=24002,username='hive')