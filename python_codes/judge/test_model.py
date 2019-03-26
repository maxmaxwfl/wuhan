# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 10:18:07 2018

@author: whjz2
"""
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.neural_network import MLPClassifier
#from matplotlib.mlab import PCA
from sklearn.preprocessing import MinMaxScaler
xd_feature = np.load("D:/python_codes/form_statis_datas/datas/xd_feature13_1000.npy")
ck_feature = np.load("D:/python_codes/form_statis_datas/datas/ck_feature13_1000.npy")

#xd_feature1 = np.load("D:/python_codes/form_statis_datas/datas/xd_featureandi_1000.npy")
#ck_feature1 = np.load("D:/python_codes/form_statis_datas/datas/ck_featureandi_1000.npy")

xd_feature1 = np.load("D:/python_codes/form_statis_datas/datas/xd_feature13_600.npy")
ck_feature1 = np.load("D:/python_codes/form_statis_datas/datas/ck_feature13_600.npy")

xd_feature2 = np.load("D:/python_codes/form_statis_datas/datas/xd_feature13_400.npy")
ck_feature2 = np.load("D:/python_codes/form_statis_datas/datas/ck_feature13_400.npy")

xd_all =np.vstack([xd_feature,xd_feature1,xd_feature2])
ck_all =np.vstack([ck_feature,ck_feature1,ck_feature2])
#xd_all = xd_feature
#ck_all =ck_feature

xd = []
ck = []

for i in range(len(xd_all)):
    one_feature=[]
    for j in range(len(xd_all[i])):
        
        #if j==2 or j==4 or j>=8:
        if  j>=2 :
            one_feature.append(int(xd_all[i][j]))
    if (np.sum(one_feature)>0):
        xd.append(one_feature)

    
for i in range(len(ck_all)):
    one_feature=[]
    for j in range(len(ck_all[i])):
        
        #if j==2 or j==4 or j>=8:
        if  j>=2:  
            one_feature.append(int(ck_all[i][j]))
    if (np.sum(one_feature)>0):
        ck.append(one_feature)
#X = np.vstack([xd,ck])
#Y = np.zeros((len(X),2))
#for i in range(len(Y)):
#    start = len(xd)
#    if i < start:
#        Y[i][0]=1
#    else:
#        Y[i][1]=1
#train_x,test_x,train_y,test_y = train_test_split(X,Y,test_size=0.2)
#np.save("ta_x",train_x)
#np.save("te_x",test_x)
#np.save("ta_y",train_y)
#np.save("te_y",test_y)

#xd_s = preprocessing.normalize(xd,norm='l2')
#ck_s = preprocessing.normalize(ck,norm='l2')

#随机抽样构建样本
from sklearn.svm import SVC
acc_sum=0
min_acc = 1
for t in range(100):
    X = np.vstack([xd,ck])
    #X = preprocessing.normalize(X,norm='l2')
    #scalar = StandardScaler()
    #scalar.fit)
    #X = MinMaxScaler().fit_transform(X)
    Y = np.zeros(len(X))
    for i in range(len(ck)):
        start = len(xd)
        Y[i+start]=1
    train_x,test_x,train_y,test_y = train_test_split(X,Y,test_size=0.2)
    
    
    clf = MLPClassifier(hidden_layer_sizes=(15,),solver='sgd',
                        activation='relu',verbose=1,alpha=1e-4,
                        learning_rate_init=0.01,max_iter=1000,random_state=1)
    
    #clf = MLPClassifier(hidden_layer_sizes=(150,),solver='lbfgs',activation='relu',verbose=1)

    #clf = neighbors.KNeighborsClassifier(n_neighbors=27,weights='distance')
    #clf = SVC()
    clf.fit(train_x,train_y)
    #print clf.score(train_x,train_y)
    #pred_p = clf.predict_proba(test_x)
    pred = clf.predict(test_x)
    p_true = pred==test_y
    acc = np.sum(p_true)
    accu = float(acc)/len(test_y)
    print accu
    acc_sum += accu
    if(accu<min_acc):
        min_acc = accu
print acc_sum
#print train_x[0]   

#手动选择前 80 % 数据作为训练集
"""
train_xd_num = int(len(xd)*0.8)
train_xd = xd[:train_xd_num]
test_xd = xd[train_xd_num:]

train_ck_num = int(len(ck)*0.8)
train_ck = ck[:train_ck_num]
test_ck = ck[train_ck_num:]


train_x = np.vstack([train_xd,train_ck])
test_x = np.vstack([test_xd,test_ck])

train_y = np.zeros(len(train_x))
for i in range(len(train_ck)):
    train_y[i+len(train_xd)]=1

test_y = np.zeros(len(test_x))
for i in range(len(test_ck)):
    test_y[i+len(test_xd)]=1
 
train_x=np.array(train_x)
train_y=np.array(train_y)
test_x=np.array(test_x)
test_y=np.array(test_y)



whole_x = np.vstack([train_x,test_x])
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler().fit_transform(whole_x)
pca = PCA(n_components=6) 
pca.fit_transform(scaler)
print(pca.explained_variance_ratio_)

#mypca = PCA(train_x)
#KNN分类

clf = neighbors.KNeighborsClassifier(n_neighbors=5)
clf.fit(train_x,train_y)
pred = clf.predict(test_x)
acc = np.sum(p_true)
accu = float(acc)/len(test_y)
acc_sum += accu

#简单的SVM分类 
   
   clf = SVC()
   clf.fit(train_x,train_y)
   pred = clf.predict(test_x)
   p_true = pred==test_y
   acc = np.sum(p_true)
   accu = float(acc)/len(test_y)
   acc_sum += accu

#AdaBooost 以及随机森林 集成学习

from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
clf = AdaBoostClassifier(n_estimators=100,random_state=0)
#clf = RandomForestClassifier(n_estimators=3000,max_depth=None,random_state=0)
clf.fit(train_x,train_y)
pred = clf.predict(test_x)
p_true = pred==test_y
acc = np.sum(p_true)
print float(acc)/len(test_y)
"""