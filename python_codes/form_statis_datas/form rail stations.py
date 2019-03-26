# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 16:52:19 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import os
from collections import Counter
import jieba
import jieba.analyse
rail_path = "D:/python_codes/railway_stations.csv"
rail = pd.read_csv(rail_path,encoding="utf-8")
#云南火车站
yunnan = rail[rail["city"]==u"云南"]
yunnan_list = list(yunnan["station"])
#湖南、贵州火车站
hunan = rail[rail["city"]==u"湖南"]
hunan_list = list(hunan["station"])

guizhou = rail[rail["city"]==u"贵州"]
guizhou_list = list(guizhou["station"])
#四川、柳州、江西火车站
sichuan = rail[rail["city"]==u"四川"]
sichuan_list = list(sichuan["station"])

liuzhou_list=[]
liuzhou_list.append(u"柳州")
liuzhou_list.append(u"柳州南")
liuzhou_list.append(u"柳州直销")


jiangxi = rail[rail["city"]==u"江西"]
jiangxi_list = list(jiangxi["station"])


rail_important = hunan_list + guizhou_list
rail_less = sichuan_list + liuzhou_list + jiangxi_list

yunnan_list = np.array(yunnan_list)

rail_important = np.array(rail_important)
rail_less = np.array(rail_less)

np.save("rail_yunnan",yunnan_list)
np.save("rail_important",rail_important)
np.save("rail_less",rail_less)
#list中的元素都是unicode,而数据库读出的数据为utf-8,因此数据库中的数据要 .decode("utf-8")


#np.save("rail_yunnan",yunnan_list)
#rail_import=np.vstack([hunan_list,guizhou_list])
#rail_less=np.vstack([sichuan_list,liuzhou_list,jiangxi_list])

#np.save("rail_important",rail_import)
#np.save("rail_less",rail_less)