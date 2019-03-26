# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 16:04:58 2018

@author: whjz2
"""

import numpy as np 
#最重要的机场--------云南
airport_yunnan=[]
#云南的机场
airport_yunnan.append("BSD")
airport_yunnan.append("DIG")
airport_yunnan.append("DLU")
airport_yunnan.append("JHG")
airport_yunnan.append("KMG")
airport_yunnan.append("LJG")
airport_yunnan.append("LNJ")
airport_yunnan.append("LUM")
airport_yunnan.append("SYM")
airport_yunnan.append("ZAT")


#重要机场--------湖南、贵州
airport_important=[]
#湖南的机场
airport_important.append("CGD")
airport_important.append("CSX")
airport_important.append("DYG")
airport_important.append("HJJ")
airport_important.append("HNY")
#贵州的机场
airport_important.append("KWE")
airport_important.append("TEN")
airport_important.append("ZYI")

#次重要机场---------江西、四川、柳州
airport_less=[]

#江西机场
airport_less.append("JDZ")
airport_less.append("JGS")
airport_less.append("JIU")
airport_less.append("KHN")
airport_less.append("KOW")
#四川机场
airport_less.append("CTU")
airport_less.append("DAX")
airport_less.append("GHN")
airport_less.append("JZH")
airport_less.append("LZO")
airport_less.append("MIG")
airport_less.append("NAO")
airport_less.append("PZI")
airport_less.append("WXN")
airport_less.append("XIC")
airport_less.append("YBP")
#柳州机场
airport_less.append("LZH")

airport_yunnan =np.array(airport_yunnan)
airport_important = np.array(airport_important)
airport_less = np.array(airport_less)
np.save("airport_yunnan",airport_yunnan)
np.save("airport_important",airport_important)
np.save("airport_less",airport_less)
