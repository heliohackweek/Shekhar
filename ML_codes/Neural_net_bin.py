import numpy as np
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

bins=np.arange(0,2159)
i=0
bin_data=pickle.load(open("/Users/sapnashekhar/Python_files/Model_data/bin_"+'{:04d}'.format(i)+".sav", 'rb')) 
var=list(bin_data)
time=bin_data[var[0]]+bin_data[var[1]]/60.+bin_data[var[2]]/3600.
n=[]
bin_data['time']=time
i_time=np.where(bin_data['mep05']==0.0)

if (not i_time == False):
    if (len(i_time[0])>10):
        n.append(len(i_time[0]))
        i_p=1
        n_time_data={}
        for j in var[3:-8]:
            n_time_data[j]=bin_data[j][i_time[0]]
            n_time_data['time']=time[i_time[0]]
            L_cen=bin_data['L_cen']
            MLT_cen=bin_data['MLT_cen']
            x_plot=bin_data['mep06'][i_time[0]]
            i_p=i_p+1
        labels=np.array(n_time_data['mep06'])
        #out_e3=np.array(n_time_data['me03'])
        #out_p5=np.array(n_time_data['mep05'])
        data=pd.DataFrame(data=n_time_data)
        features=data[var[3:9]]
        model = Sequential()
        model.add(Dense(12, input_dim=6, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(1, activation='relu'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(features, labels, epochs=150, batch_size=10)
        predictions = model.predict(features)
        _,accuracy = model.evaluate(features, labels)
        print('Accuracy: %.2f' % (accuracy*100))
