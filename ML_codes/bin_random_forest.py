"""
Created on Thu Feb 27 11:53:01 2020

@author: sapnashekhar
"""

import numpy as np
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

bins=np.arange(0,2160)
n=[]
R_sq_train=[]
R_sq_test=[]
L_cen=[]
MLT_cen=[]
val_met_n={}
for i in bins:
    bin_data=pickle.load(open("/Users/sapnashekhar/Python_files/Model_data/bin_"+'{:04d}'.format(i)+".sav", 'rb')) 
    var=list(bin_data)
    time=bin_data[var[0]]+bin_data[var[1]]/60.+bin_data[var[2]]/3600.
    bin_data['time']=time
    i_time=np.where((bin_data['mep05']==0.0))
    if (not i_time == False):
        if (len(i_time[0])>10):
            n.append(len(i_time[0]))
            n_time_data={}
            for j in var[3:-8]:
                n_time_data[j]=bin_data[j][i_time[0]]
            L_cen.append(bin_data['L_cen'])
            MLT_cen.append(bin_data['MLT_cen'])
            n_time_data['time']=time[i_time[0]]
            labels=np.array(n_time_data['mep06'])
            data=pd.DataFrame(data=n_time_data)
            features=data[var[3:10]]
            train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)
            rf = RandomForestRegressor(n_estimators = 100, random_state = 42)    
            rf.fit(train_features, train_labels)
            predictions = rf.predict(test_features)
            train_pred = rf.predict(train_features)
            R1=np.cov(predictions, test_labels)/(np.std(predictions)*np.std(test_labels))
            R_sq_test.append(R1[0,1])
            R2=np.cov(train_pred, train_labels)/(np.std(train_pred)*np.std(train_labels))
            R_sq_train.append(R2[0,1])
            print(i)
val_met_n["bin"]=bins        
val_met_n["n_data"]=np.array(n) 
val_met_n["p_coef_tr"]=np.array(R_sq_train)
val_met_n["p_coef_te"]=np.array(R_sq_test)
val_met_n['L_cen']=np.array(L_cen)
val_met_n['MLT_cen']=np.array(MLT_cen) 
pickle.dump(val_met_n,open("/Users/sapnashekhar/Python_files/Model_data/P_coef_random_forest_reg.sav", 'wb'))

