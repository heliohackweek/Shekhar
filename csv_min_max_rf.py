#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 17:07:59 2020

@author: sapnashekhar
"""

#Code implements and tests random Forest regressor for the POES cleaned data#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import export_graphviz
import pydot
    
def main():
    f_min=pd.read_csv("./metop_rad_belt_passes_min.csv")
    f_median=pd.read_csv("./metop_rad_belt_passes_median.csv")
    f_max=pd.read_csv("./metop_rad_belt_passes_max.csv")
    var=list(f_max)
    ###construct the feature dataframe#########################
    labels=np.array(f_max['mep06'])
    
    feat_list=[[f_min[var[1]]],[f_min[var[2]]],[f_min[var[3]]],[f_max[var[4]]],[f_median[var[5]]],[f_max[var[6]]],[f_median[var[8]]],[f_median[var[9]]],[f_median[var[14]]],[f_max[var[7]]*f_max[var[15]]]]#,[labels]]
    feat_head=['min_IMFBy','min_IMFBz','min_Dst','max_Kp','med_L','max_Pdyn','med_lat','med_lon','med_MLT','max_moment']#,'mep06']
    feat_arr=np.array(feat_list)
    features=np.transpose(feat_arr.reshape([10,len(f_min[var[1]])]))
    feat_df=pd.DataFrame(features, columns=feat_head)
    #################################################################
    ##########Scatter plot####################################
    pd.plotting.scatter_matrix(feat_df, alpha=0.2, figsize=(10,10))
    plt.savefig("./plots/data_metop_scatter_mtx_min_max_val.pdf",dpi=300)
    plt.show() 
    ######################################################################3
    #splits 25% of data as test data and 75% as traiing data$$$$$$$$$$$$$$$$$$
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)
    ##################################################################################
    ############creates a RFR model with decision trees as deep as 100########
    rf = RandomForestRegressor(n_estimators = 1000, random_state = 42, max_depth=100)    
    rf.fit(train_features, train_labels)
    predictions = rf.predict(test_features)
    train_pred = rf.predict(train_features)
    ##################################################################################
    #########visualization of the rfr decision tree########################
    tree = rf.estimators_[5]
    export_graphviz(tree, out_file = './plots/tree.dot', feature_names = feat_head, rounded = True, precision = 1)
    (graph, ) = pydot.graph_from_dot_file('./plots/tree.dot')
    graph.write_png('./plots/tree_depth100.png')
    ###############plots meped p6 channel count rates observed in th satellite vs predicted by the RFR model####################
    fig = plt.figure(figsize=(4, 4))
    ax=plt.subplot(2,1,2)  
    ax.plot(test_labels,predictions,linestyle=' ',marker='o', markersize=2,color='b')
    ax.set_title('RFR test fit for 12/2006 n_test='+str(len(test_labels)),size=10)
    ax.set_xlabel('p6 count rates')
    ax.set_ylabel('Predicted p6 count rates')
    y=np.arange(10)
    line=plt.plot(y,y,color='red')
    ax.set_xlim([0,np.max(test_labels)])
    ax.set_ylim([0,np.max(predictions)])
    ax=plt.subplot(2,1,1)  
    ax.plot(train_labels,train_pred,linestyle=' ',marker='o', markersize=2,color='b')
    ax.set_title('RFR train fit for 12/2006 n_train='+str(len(train_labels)),size=10)
    ax.set_xlabel('p6 count rates')
    ax.set_ylabel('Predicted p6 count rates')
    line=plt.plot(y,y,color='red')
    ax.set_xlim([0,np.max(train_labels)])
    ax.set_ylim([0,np.max(train_pred)])
    plt.tight_layout()#plt.legend(loc='upper right')
    plt.savefig("./plots/cross_validation_rf_depth100.png",dpi=300)
    plt.show() 
##################################################################   
    