# -*- coding: utf-8 -*-
"""
Created on Mon May 21 15:17:41 2018

@author: whjz2
"""

import cx_Oracle
import numpy as np
import pandas as pd
from sqlalchemy import types,create_engine

tj_con = cx_Oracle.connect('TONGJI/501430@127.0.0.1:1521/orcl',encoding='utf-8')
query = "select XM,GMSFHM from SELECT_QZLS"
rec_count = pd.read_sql(query,tj_con)
rec_count = rec_count.drop_duplicates()
a = np.array(rec_count)
np.save("QZLS_list",a)