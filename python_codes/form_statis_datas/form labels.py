# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 09:10:41 2018

@author: whjz2
"""
import pandas as pd
import numpy as np
import cx_Oracle
import time
import os
from collections import Counter
import pickle 
from sqlalchemy import types,create_engine
#判断火车的三个标签
def set_labels_rail(sfz,ck_xd):
    if(ck_xd==0):
        query_rail = "SELECT RAIL_CFZ,RAIL_MDZ FROM TONGJI.XD_RAIL WHERE GMSFHM='%s'"%sfz
    else:
        query_rail = "SELECT RAIL_CFZ,RAIL_MDZ FROM TONGJI.CK_RAIL WHERE GMSFHM='%s'"%sfz
    label_rail_yunnan=0
    label_rail_imp =0 
    label_rail_les =0
    label_rail = 0
    
    rail = pd.read_sql(query_rail,connection)
    
    cfz = list(rail["RAIL_CFZ"])
    mdz = list(rail["RAIL_MDZ"])
    if len(rail):
        label_rail=1
    
    if(len(cfz)):
        for item in cfz:
            item_u = item.decode("utf-8")
            if item_u in rail_yunnan:
                label_rail_yunnan = 1
                
            if item_u in rail_important:
                label_rail_imp = 1
                
            if item_u in rail_less:
                label_rail_les = 1
                
    
    if(len(mdz)):
        for item in mdz:
            item_u = item.decode("utf-8")
            if item_u in rail_yunnan:
                label_rail_yunnan = 1
                
            if item_u in rail_important:
                label_rail_imp = 1
                
            if item_u in rail_less:
                label_rail_les = 1
    
    #query_insert = "INSERT INTO XD_LABEL(GMSFHM,RAIL_YUNNAN,RAIL_IMPORTANT,RAIL_LESS)values \
    #('%s',%i,%i,%i)"%(sfz,label_rail_yunnan,label_rail_imp,label_rail_les)
    
    #try:
    #    result= c.execute(query_insert)
    #    connection.commit()
    #    print"rail success"
    #finally:            
    return label_rail_yunnan,label_rail_imp,label_rail_les,label_rail
#判断民航的三个标签
def set_labels_air(sfz,ck_xd):
    if(ck_xd==0):
        query_air = "SELECT DJJCBH,DDJCBH FROM TONGJI.XD_AIR WHERE GMSFHM='%s'"%sfz
    else:
        query_air = "SELECT DJJCBH,DDJCBH FROM TONGJI.CK_AIR WHERE GMSFHM='%s'"%sfz
    label_air_yunnan=0
    label_air_imp =0 
    label_air_les =0
    label_air =0 
    air = pd.read_sql(query_air,connection)
    dj = list(air["DJJCBH"])
    dd = list(air["DDJCBH"])
    
    if(len(air)):
        label_air=1
    if(len(dj)):
        for add in dj:
            if add in airport_yunnan:
                label_air_yunnan =1
                
            elif add in airport_important:
                label_air_imp =1
                break
            elif add in  airport_less:
                label_air_les =1
    if(len(dd)):
        for add in dd:
            if add in airport_yunnan:
                label_air_yunnan =1
                
            elif add in airport_important:
                label_air_imp=1
                break
            elif add in  airport_less:
                label_air_les=1
    """
    query_insert = "UPDATE TONGJI.XD_LABEL SET AIR_YUNNAN = %i,AIR_IMPORTANT = %i,\
    AIR_LESS=%i WHERE GMSFHM='%s'"%(label_air_yunnan,label_air_imp,label_air_les,sfz)
    print query_insert
    try:
        result= c.execute(query_insert)
        connection.commit()
        print"air success"
    finally:            
        return
    """
    return label_air_yunnan,label_air_imp,label_air_les,label_air

def set_labels_hotel(sfz,ck_dw):
    if(ck_dw==0):
        query_hotel ="SELECT QYMC FROM TONGJI.XD_HOTEL WHERE GMSFHM='%s'"%sfz
    else:
        query_hotel ="SELECT QYMC FROM TONGJI.CK_HOTEL WHERE GMSFHM='%s'"%sfz
    label_hotel = 0
    hotel = pd.read_sql(query_hotel,connection)
    qymc = list(hotel["QYMC"])
    if(len(qymc)):
        for add in qymc:
            if add in hotel_list:
                label_hotel =1
                break
    """
    query_insert = "UPDATE TONGJI.XD_LABEL SET HOTEL= %i WHERE GMSFHM='%s'"%(label_hotel,sfz)
    
    try:
        result= c.execute(query_insert)
        connection.commit()
        print"hotel success"
    finally:
    """            
    return label_hotel

def set_labels_position(sfz):
    query_position="SELECT LONGITUDE,LATITUDE,CP FROM GATOJZ.TB_CFG_XDCZ_DW WHERE SFZH='%s'"%sfz
    label_position = 0 
    label_more_night = 0
    pos = pd.read_sql(query_position,con_jz)
    #print"done"
    pos = pos.replace(0,np.nan)
    pos = pos.dropna()
    pos["CP"] = pos["CP"].astype(str)
    if(len(pos)):
        night_time =0
        day_time =0
        for i in range(len(pos)):
            lon = pos.iloc[i]["LONGITUDE"]
            lat = pos.iloc[i]["LATITUDE"]
            s_time = int(pos.iloc[i]["CP"][-2:])
            #print s_time
            if((s_time>=18 and s_time<=23)or (s_time>=0 and s_time<=7)):
                night_time += 1
            else:
                day_time += 1
            
            for center in center_list:
                c_lon = center[0]
                c_lat = center[1]
                if (c_lon-0.0005<=lon and lon<=c_lon+0.0005 and c_lat-0.0005<=lat and lat<=c_lat+0.0005):
                    label_position =1
                    break
        print'night_time %i'%night_time
        print'day_time %i'%day_time
        if(night_time>day_time):
            label_more_night = 1            
    return label_position,label_more_night
def set_labels_communi(sfz,ck_xd):
    if(ck_xd==0):
        query="select SFZH,USERNUM from TONGJI.XD_DW where SFZH='%s'"%sfz
    else:
        query="select SFZH,USERNUM from TONGJI.CK_DW where SFZH='%s'"%sfz
    label_multi_numbers = 0
    ph = pd.read_sql(query,connection)
    if(len(ph)):
        number_set=set(list(ph["USERNUM"]))
        if len(number_set)>=3:
            label_multi_numbers=1
    return label_multi_numbers
    """
    query_insert = "UPDATE TONGJI.XD_LABEL SET CLUSTER_CENTER= %i WHERE GMSFHM='%s'"%(label_position,sfz)
    try:
        result= c.execute(query_insert)
        connection.commit()
        print"position success"
    finally:            
        return 
    """
def set_labels_crj(sfz):
    query="select CRJZJR_GMSFHM,CRJZJR_XM from GATOJZ.JMCRJZJQFXX_STGX where CRJZJR_GMSFHM='%s'"%sfz
    label_crj = 0 
    crj = pd.read_sql(query,con_jz)
    if(len(crj)>0):
        label_crj = 1
    return label_crj

def set_labels_andi(sfz):
    #du_string = "%毒%"
    #du_string = du_string.decode("utf-8")
    query = "select XYR_WFFZJLMSMS,XYR_GMSFHM from GATOJZ.XYRXX_JWZH where XYR_GMSFHM='%s'"%(sfz)
    label_andi = 0        
    andi = pd.read_sql(query,con_jz)
    if(len(andi)>1):
        label_andi =1
    return label_andi

connection = cx_Oracle.connect('TONGJI/501430@127.0.0.1:1521/orcl',encoding='utf-8')
con_jz = cx_Oracle.connect('jz_test/jz_test@12.14.144.114:1521/whbd',encoding='utf-8')

c=connection.cursor()
rail_yunnan = np.load("D:/python_codes/judge/rail_yunnan.npy")
rail_yunnan = set(rail_yunnan)
rail_important = np.load("D:/python_codes/judge/rail_important.npy")
rail_important = set(rail_important)
rail_less = np.load("D:/python_codes/judge/rail_less.npy")
rail_less = set(rail_less)
airport_yunnan = np.load("D:/python_codes/judge/airport_yunnan.npy")
airport_yunnan = set(airport_yunnan)
airport_important = np.load("D:/python_codes/judge/airport_important.npy")
airport_important = set(airport_important)
airport_less = np.load("D:/python_codes/judge/airport_less.npy")
airport_less = set(airport_less)
hotel_list = np.load("D:/python_codes/judge/hotel_list.npy")
hotel_list = set(hotel_list)
center_list = np.load("D:/python_codes/judge/cluster_centers.npy")

fr =open("D:/python_codes/xdry_1818.pkl",'rb')
xd = pickle.load(fr)
#fr =open("D:/python_codes/ck_1953.pkl",'rb')
#ck = pickle.load(fr)
sfz_list = list(xd["RY_GMSFHM"])


xd_feature=[]
#rail_lyunnan,rail_limp,rail_lless,label_rail = set_labels_rail(sfz_list[4])
#position,more_night = set_labels_position(sfz_list[2])

for i,sfz in enumerate(sfz_list):
    #if i<=600:
    #if i>=600 and i<1600:
    if i>=1600:
        #rail_lyunnan,rail_limp,rail_lless,label_rail = set_labels_rail(sfz,0)
        #air_lyunnan,air_limp,air_lless,label_air = set_labels_air(sfz,0)
        #hotel_label = set_labels_hotel(sfz,0)
        #position,more_night = set_labels_position(sfz)
        #multi_user = set_labels_communi(sfz,0)
        #crj = set_labels_crj(sfz)
        andi = set_labels_andi(sfz)
        one_line = []
        #one_line.append(sfz)
        #one_line.append(rail_lyunnan)
        #one_line.append(rail_limp)
        #one_line.append(rail_lless)
        #one_line.append(label_rail)
        #one_line.append(air_lyunnan)
        #one_line.append(air_limp)
        #one_line.append(air_lless)
        #one_line.append(label_air)
        #one_line.append(hotel_label)
        #one_line.append(position)
        #one_line.append(more_night)
        #one_line.append(crj)
        one_line.append(andi)
        xd_feature.append(one_line)
        print '%i th done'%i
np.save("D:/python_codes/form_statis_datas/datas/xd_featureandi_400",xd_feature)
np.savetxt("D:/python_codes/form_statis_datas/datas/xd_featureandi_400.txt",xd_feature,fmt='%s')
