# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 10:09:20 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import cx_Oracle
import time
import os
from sqlalchemy import types,create_engine

lastdir = os.path.abspath(os.path.dirname(os.getcwd()))
xd1_path = os.path.join(lastdir,'xdry_1818.pkl')

connection = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd')
tj_con = create_engine('oracle+cx_oracle://TONGJI:501430@127.0.0.1:1521/?service_name=orcl')


rail=pd.read_sql("SELECT RENYUAN_GMSFHM,RENYUAN_XM,CFZ_MC,MDZ_MC,CC_BH FROM GATOJZ.FTPTLGP_BAK\
                 WHERE RENYUAN_GMSFHM='420111200806244717'",con=connection)
rail.columns =['GMSFHM','XM','RAIL_CFZ','RAIL_MDZ','RAIL_CC']
col_list = ['GMSFHM','XM','RAIL_CFZ','RAIL_MDZ','RAIL_CC']
railn = {c:types.VARCHAR(20)for c in col_list}

rail.to_sql("test2",tj_con,if_exists='append',index=False,dtype=railn)