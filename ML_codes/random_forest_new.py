""" 

Implementing a random forest for the POES data

 """



# imports for the random forest
import numpy as np
import scipy.stats as stats
import pandas as pd
import glob
import csv
import matplotlib.pyplot as plt


import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn import metrics


from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor





### new forest

# loading in the data and sepearating out the x and y
# and the train and test set 

def create_dataset(filename, cols, shuffle):
    dataset = pd.read_csv(filename) 

    # removing columns 
    dataset = dataset.drop(columns=cols)

    
    if(shuffle):
        train_dataset = dataset.sample(frac=0.8,random_state=0)
        test_dataset = dataset.drop(train_dataset.index)
    else:
        number_entries = round(dataset.size*.8)
        train_dataset=dataset[:number_entries]
        test_dataset=dataset[number_entries:]

    y_train = train_dataset.pop("mep06") # using .pop function to store only the dependent variable
    y_test = test_dataset.pop("mep06")

    x_train = train_dataset
    x_test = test_dataset

    return(x_train, y_train, x_test, y_test)


# inputs are the x and y for training and x and y for testing and 
# the n_est for the random forest 
# debug is for showing debug results 
def start_training(x_train, y_train, x_test, y_test, n_est, debug=False):
    #training the data 
    regressor = RandomForestRegressor(n_estimators = n_est, random_state = 0) 

    regressor.fit(x_train, y_train)  
    
    #predicting the output
    if debug:
        Y_pred = regressor.predict(x_test)  
        mae=metrics.mean_absolute_error(y_test, Y_pred)
        mse=metrics.mean_squared_error(y_test, Y_pred)
        print(mae)
        print(mse)
        plt.scatter(y_test[y_test<2],Y_pred[y_test<2])
        plt.show()
    return(regressor)


if __name__ == "__main__":
    cols = ['dateTime', 'mep05', 'mep01', 'me03', 'Lval', 'mlt', 'lat', 'lon', 'BzIMF', 'dens', 'velo']
    x_train, y_train, x_test, y_test = create_dataset('../metop_rad_belt_passes_median.csv',cols, True)
    start_training(x_train, y_train, x_test, y_test,200, debug= True)