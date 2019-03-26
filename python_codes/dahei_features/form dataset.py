# -*- coding: utf-8 -*-
"""
Created on Fri May 11 09:20:08 2018

@author: whjz2
"""
import cx_Oracle
import numpy as np
import pandas as pd
import jieba
import jieba.posseg as pseg
from sqlalchemy import types,create_engine
#jieba.load_userdict("D:/python_codes/dict.txt")
con_jz = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd',encoding='utf-8')
#condition = "%聚众赌博%"
#condition = "%强迫交易%"
#condition ="%组织%卖淫%"
#condition="%寻衅滋事%"
condition="%敲诈%"
condition_uni = condition.decode("utf-8")
query = "select AJ_MC,AJ_TYBH,AJ_JYAQ from GATOJZ.AJJBXX_JWZH where AJ_MC like '%s'"%condition_uni
rec = pd.read_sql(query,con_jz)
ajbh = list(rec["AJ_TYBH"])

#in 最多1000条 因此若>1000条记录，需根据需求切分
"""
record_length = len(rec)
split_number = record_length / 900 +1
bh_list = ["("]*split_number
query1 = "select AJ_BH,XYR_XM,XYR_GMSFHM from GATOJZ.XYRXX_JWZH where"
for i,bh in enumerate(ajbh):
    index= i /900
    yu = i%900
    
    if i==len(ajbh)-1 or yu ==899:
        bh_list[index] += "'%s'"%bh
        #bh_list[index] += ","
    else:
        bh_list[index] += "'%s'"%bh
        bh_list[index] += ","
for i in range(split_number):
    bh_list[i]+=')'
    if i == 0:
        query1 += " AJ_BH IN %s"%bh_list[i]
    else:
        query1 +=" OR AJ_BH IN %s"%bh_list[i]
"""
"""
bh_list = "("
for i,bh in enumerate(ajbh):
    if i< len(ajbh)-1:
        bh_list += "'%s'"%bh
        bh_list += ","
    else:
        bh_list += "'%s'"%bh
bh_list +=")"
query1 = "select AJ_BH,XYR_XM,XYR_GMSFHM from GATOJZ.XYRXX_JWZH where AJ_BH IN %s"%bh_list
"""
"""
dubo_ry = pd.read_sql(query1,con_jz)
dubo_ry["XYR_XM"]=dubo_ry["XYR_XM"].str.decode("utf-8")
#设置列名，并将非数值列转为str型
dubo_ry.columns = ['AJ_BH','XM','GMSFHM']
varchar_list = ['AJ_BH','XM','GMSFHM']
dubo_dict = {c:types.VARCHAR(dubo_ry[c].str.len().max())for c in varchar_list}
tj_con = create_engine('oracle+cx_oracle://TONGJI:501430@127.0.0.1:1521/?service_name=orcl',encoding="utf-8")
dubo_ry.to_sql("SH_QPJY_LIST",tj_con,if_exists='append',index=False,dtype=dubo_dict)
"""
tj_con1 = cx_Oracle.connect('TONGJI/501430@127.0.0.1:1521/orcl',encoding='utf-8')
c=tj_con1.cursor()
for i in range(len(rec)):
    mc = rec.iloc[i]["AJ_MC"]
    mc_u = mc.decode("utf-8")
    aq = rec.iloc[i]["AJ_JYAQ"]
    aq_u = aq.decode("utf-8")
    aq_u = aq_u.replace("'","")
    bh = rec.iloc[i]["AJ_TYBH"]
    update_q = "update TONGJI.SH_QZLS_LIST set AJ_JYAQ='%s' where AJ_BH='%s'"%(aq_u,bh)
    result= c.execute(update_q)
    tj_con1.commit()

"""
name_list=[]
for item in ajms:
    pos = pseg.cut(item)
    for word,flag in pos:
        if flag=='nr':
            name_list.append(word)
name_list = list(set(name_list))
name_list = np.array(name_list)
name_list_utf = [item.encode("utf-8") for item in name_list]
np.savetxt("dubo_name_list1.txt",name_list_utf,fmt='%s')
#jieba.add_word("白玉山",100)
#jieba.add_word("张公寨",100)
pos = pseg.cut(ajms[118])
for word,flag in pos:
    print ('%s %s'%(word,flag))
"""