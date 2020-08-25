"""
Created on Wed Feb 14 08:38:53 2020

@author: sapnashekhar
"""
import pandas as pd
import numpy as np
import os
import spacepy.time as spt
import spacepy.omni as om
import spacepy.toolbox as tb
import pickle

def read_all_text_files(f_name, L_low=3.5, L_high=8.0):
    data=pd.read_fwf("/Users/sapnashekhar/IDLWorkspace81/POES_16s_text_data/"+f_name)
    data_1=data.loc[(data["lval"]>=L_low) & (data["lval"]<=L_high) & (data["mep0p6"]>0)& (data["mep0p6"]<500.0)]
    return(data_1)
    
def get_sw_values(time_str):
    ticks = spt.Ticktock(time_str, 'ISO')
    d_s = om.get_omni(ticks)
    return(d_s)   
        
        
def main():
    tb.update()
    sat=["metop02"]
    year=list(range(2013,2015))
    month=list(range(1,13))
    dom=list(range(1,32))
    
    for i in range(len(sat)):
        for j in range(len(year)):
            for k in range(len(month)):
                for q in range(len(dom)):
                    f_name=sat[i]+"/poes_"+sat[i][0]+sat[i][-2:]+"_"+'{:04d}'.format(year[j])+'{:02d}'.format(month[k])+'{:02d}'.format(dom[q])+".txt" 
                    print(f_name)
                    time_str=[]
                    stat_data_25=[]
                    stat_data_50=[]
                    stat_data_75=[]
                    can_dir="/Users/sapnashekhar/IDLWorkspace81/POES_16s_text_data/"+f_name
                    if (os.path.exists(can_dir)==True):
                        if (os.path.getsize(can_dir) > 1000):
                            data=read_all_text_files(f_name)
                            print(data["mep0p6"].describe())
                            stat=data["mep0p6"].describe()
                            stat_data_25.append(stat[4])
                            stat_data_50.append(stat[5])
                            stat_data_75.append(stat[6])
                            fin_data={}
                            t_hr=[]
                            t_min=[]
                            t_sec=[]
                            t_mep6=[]
                            t_mep5=[]
                            t_mep1=[]
                            t_me3=[]
                            t_lval=[]
                            t_mlt=[]
                            t_lat=[]
                            t_lon=[]
                            for h_r in range(24):
                                h_p=np.where(np.array(data["hr"])==h_r)[0]
                                if len(h_p)>0:
                                    for h in h_p:
                                        t_min.append(np.array(data["mi"])[h])
                                        t_sec.append(np.array(data["second"])[h])
                                        t_mep6.append(np.array(data["mep0p6"])[h])
                                        t_mep5.append(np.array(data["mep0p5"])[h])
                                        t_mep1.append(np.array(data["mep0p1"])[h])
                                        t_me3.append(np.array(data["mep0e3"])[h])
                                        t_lval.append(np.array(data["lval"])[h])
                                        t_mlt.append(np.array(data["mlt"])[h])
                                        t_lat.append(np.array(data["sslat"])[h])
                                        t_lon.append(np.array(data["sslon"])[h])
                                        t_hr.append(h_r)
                                        time_s='{:04d}'.format(year[j])+'-'+'{:02d}'.format(month[k])+'-'+'{:02d}'.format(dom[q])+'T'+'{:02d}'.format(np.array(data["hr"])[h])+':'+'{:02d}'.format(np.array(data["mi"])[h])+':'+'{:012.9f}'.format(np.array(data["second"])[h])+'Z'
                                        time_str.append(time_s)
                            d_sw=get_sw_values(time_str)
                            fin_data['Hour']=np.array(t_hr)
                            fin_data['minute']=np.array(t_min)
                            fin_data['second']=np.array(t_sec)
                            fin_data['Kp']=np.array(d_sw['Kp'])
                            fin_data['Dst']=np.array(d_sw['Dst'])
                            fin_data['dens']=np.array(d_sw['dens'])
                            fin_data['velo']=np.array(d_sw['velo'])
                            fin_data['Pdyn']=np.array(d_sw['Pdyn'])
                            fin_data['ByIMF']=np.array(d_sw['ByIMF'])
                            fin_data['BzIMF']=np.array(d_sw['BzIMF'])
                            fin_data['mep06']= np.array(t_mep6)
                            fin_data['mep05']= np.array(t_mep5)
                            fin_data['mep01']= np.array(t_mep1)
                            fin_data['me03']= np.array(t_me3)
                            fin_data['Lval']=np.array(t_lval)
                            fin_data['mlt']=np.array(t_mlt)
                            fin_data['lat']=np.array(t_lat)
                            fin_data['lon']=np.array(t_lon)
                            
                            filename = '/Users/sapnashekhar/Python_files/Model_data/finalized_data_'+sat[i]+'{:04d}'.format(year[j])+'{:02d}'.format(month[k])+'{:02d}'.format(dom[q])+'.sav'
                            pickle.dump(fin_data, open(filename, 'wb'))   
    
    
                    
