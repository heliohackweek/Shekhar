import numpy as np
import pickle
#######load data#########
bins=np.arange(0,2159)
i=0
bin_data=pickle.load(open("/Users/sapnashekhar/Python_files/Model_data/bin_"+'{:04d}'.format(i)+"_2013.sav", 'rb')) 
var=list(bin_data)
#########var=['Hour', 'minute','second','Kp','Dst', 'dens','velo','Pdyn', 'ByIMF', 'BzIMF', 'mep06', 'mep05', 'mep01','me03',######
####### 'Lval','mlt', 'lat', 'lon', 'L_cen', 'MLT_cen', 'year', 'month', 'dom']##################################################
################################################################################################################################
#####bin_data[var[n]] gets the column of data for the var chosen#############
