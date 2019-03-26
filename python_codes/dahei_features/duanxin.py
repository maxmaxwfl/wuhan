# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 17:12:57 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import os
from collections import Counter
import jieba
import jieba.analyse

testsms = "C:/Users/whjz2/Desktop/dahei/2018-04-10 09-27-37_1.csv"

dx = pd.read_csv(testsms,encoding='utf-8')
text = list(dx[u"内容简要"])

for x,w in jieba.analyse.textrank(text[39],withWeight=True,allowPOS=('ns','n','vn','v','m')):
    print('%s :%s'%(x,w))