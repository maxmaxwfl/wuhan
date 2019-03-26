# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:41:14 2018

@author: whjz2
"""

from collections import Counter
import pandas as pd
dianwei = pd.read_csv("C:/Users/whjz2/Desktop/dahei/dianwei/2018-04-10 09-18-50_1.csv",encoding='utf-8')
#zhujiao = dianwei[dianwei[u'事件类型']==u"主叫\t"]
#beijiao = dianwei[dianwei[u'事件类型']==u'被叫\t']
#zhujiao_count = Counter(zhujiao[u"对端标识码"])
#beijiao_count = Counter(beijiao[u"对端标识码"])

record = dianwei[dianwei[u'事件类型'].str.contains(u'开始')]
zhujiao = []
beijiao = []
for i in range(len(record)):
    #print'%i'%i
    to_no =  record.iloc[i][u"对端标识码"]
    from_no = record.iloc[i][u"本端标识码"]
    calltype = record.iloc[i][u'事件类型']
    if calltype==u'主叫开始\t' and from_no==15972044472:
       
        zhujiao.append(to_no)
    elif calltype==u'主叫开始\t' and to_no ==15972044472:
        beijiao.append(from_no)
    elif calltype==u'被叫开始\t' and to_no ==15972044472:
        
        zhujiao.append(from_no)
    elif calltype==u'被叫开始\t' and from_no ==15972044472:
        beijiao.append(to_no)    

#zhujiao = dianwei[dianwei[u'事件类型']==u"主叫开始\t"]
#beijiao = dianwei[dianwei[u'事件类型']==u"被叫开始\t"]

zhujiao_count = Counter(zhujiao)
beijiao_count = Counter(beijiao)
print 'zhujiao:',zhujiao_count
print 'beijiao:',beijiao_count
