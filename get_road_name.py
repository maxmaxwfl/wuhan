# -*- coding: utf-8 -*-
"""
Created on Fri May 11 16:39:58 2018

@author: maxmaxwfl
"""

import urllib2
url ="http://poi.mapbar.com/wuhan/G70/"
response = urllib2.urlopen(url)  
html = response.read()


import re
pattern =re.compile('<a href="http://poi.mapbar.com/wuhan/.*?>(.*?)</a>',re.S)
items = re.findall(pattern,html)

import numpy as np
addstring = " 20 ns"
new_item = [item+addstring for item in items]
new_item = np.array(new_item)
np.savetxt("roads.txt",new_item,fmt='%s')