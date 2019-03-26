# -*- coding: utf-8 -*-
"""
Created on Tue Mar 06 16:43:06 2018

@author: whjz2
"""

import pandas as pd
import numpy as np
import cx_Oracle
import time
import os
import re

from collections import Counter
from sqlalchemy import types,create_engine

from sklearn.cluster import MeanShift,estimate_bandwidth
from sklearn import metrics

connection = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd',encoding='utf-8')

query="SELECT AJ_DZMC,AJ_JYAQ from GATOJZ.AJJBXX_JWZH where AJ_AJLBDM='204063'"
ajs = pd.read_sql(query,con=connection)


"""
#统计案件发生位置
loc=[]
for i in range(len(ajs)):
    loc.append(ajs.iloc[i][0])
    
count=Counter(loc).most_common()
"""

key_words=[]
import jieba
import jieba.analyse
string = ajs.iloc[5464][1]
print string
for x,w in jieba.analyse.textrank(string,withWeight=True,allowPOS=('n','nr','ns','nz','v','vd','vn','l')):
    print('%s :%s'%(x,w))

"""
#案件内容提取关键词
key_words=[]
import jieba
import jieba.analyse
for i in range(len(ajs)):
    
    key =dict()
    string = ajs.iloc[i][1]
    #关键用的是jieba分词中的textrank
    for x,w in jieba.analyse.textrank(string,withWeight=True,allowPOS=('n','nr','ns','nz','v','vd','vn','l')):
        key[x]=w
    key_words.append(key)
    print'%i th done'%i
key_words = np.array(key_words)
np.save("d:/python_codes/datas/anjian_keyword",key_words)
"""

"""
#案件内容运行lda主题模型
r='[1-9]\d*'
stop_word=[u'[',u']',u"吸毒",u"报警",u"接警",u"嫌疑人",u"民警",u",",u"、",u")",u"(",u"年月日",u"年月日时",u"时许",u":",u"。"]
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import jieba
jyaq = []

for i in range(len(ajs)):
    if i<=10000:
        current_doc = dict()
        string = ajs.iloc[i][1]
        #去除停用词
        string = re.sub(r,'',string)
        #分词
        words = jieba.cut(string)
        #对文档构成词的词典
        for word in words:
            if word not in stop_word:
                current_doc[word] = current_doc.get(word,0.0)+1.0
        jyaq.append(current_doc)

tf_vectorizer = DictVectorizer(sparse=False)
tf = tf_vectorizer.fit_transform(jyaq)
#sklearnLDA
lda = LatentDirichletAllocation(n_components=5,max_iter=10,learning_method='online',
                                learning_offset=50.,random_state=0)
lda.fit(tf)

n_top_words= 30
def print_top_words(model,feature_names,n_top_words):
    for topic_idx,topic in enumerate(model.components_):
        message = "Topic #%d: "%topic_idx
        feature_word = topic.argsort()[::-1][:n_top_words]
        message += " ".join([feature_names[i]for i in feature_word])
        print("topics in LDA models are:")
        print(message)
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda,tf_feature_names,n_top_words)
print lda.perplexity(tf)
"""
