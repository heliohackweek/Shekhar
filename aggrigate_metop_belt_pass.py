"""
This program filters the metop data into radiation belt passes, 
keeps times when mep05==0 and me03 > met06, and adds an optional 
MLT filter. Afterwards, the remaining chunked data is split into
radiation belt passes (every 25 minutes). Lastly, this data is then
saved to the metop_rad_belt_passes_{stat_method}.csv file where the 
stat_method is the statistical method to aggrigate the values in each
radiation belt pass.
"""

import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import read_csv

# orbit_period_min = 25
stat_method='median'

# Search for all the metop csv files.
metop_dir = pathlib.Path('./csv_daily_data/')
metop_paths = sorted(list(metop_dir.glob('data_metop*.csv')))

# Make a list of the metop DataFrames and concatenate 
# them into one. 
df_list = [read_csv.load_meped_csv(str(metop_path)) 
            for metop_path in metop_paths]
df_concat = pd.concat(df_list)

# Filter by the Lval to get only the radiation belt values.
# Additional filters include: mep05 == 0 and 
# me03 > mep06 to remove contamination
df_filtered = df_concat[(df_concat.Lval > 4) & 
                      (df_concat.Lval < 8) & 
                    #   (df_concat.mlt > 16) &
                      (df_concat.mep05 == 0) &
                      (df_concat.me03 > df_concat.mep06)]

# Group by radiation belt passes.
# First define a function that identifies times where there are breaks in the data.
def findTimeBreaks(time, threshold_min=10):
    """
    Find time breaks in the the time array greater than threshold_min 
    """
    dt = (time[1:] - time[:-1]).seconds
    consecutiveFlag = np.where(dt > threshold_min*60)[0]
    startInd = np.insert(consecutiveFlag+1, 0, 0)
    endInd = np.insert(consecutiveFlag, len(consecutiveFlag), len(time)-1) + 1
    return startInd, endInd

startInd, endInd = findTimeBreaks(df_filtered.index)

# Now we know how many radiation belt passes there are, create and populate a DataFrame
# with the aggrigate values.
df_agg = pd.DataFrame(data=np.nan*np.ones((len(startInd), len(df_filtered.columns))), 
                        columns=df_filtered.columns, 
                        index=np.array(df_filtered.index)[startInd])
# Loop over each start-end radiation pass index and aggrigate the columns for each 
# sub-DataFrame
for i, (start_index, end_index) in enumerate(zip(startInd, endInd)):
    df_agg.iloc[i, :] = df_filtered.iloc[start_index:end_index, :].agg(stat_method)

df_agg.to_csv(f'metop_rad_belt_passes_{stat_method}.csv', index_label='dateTime')

### PLOTS ###
fig, ax = plt.subplots(3, 1, sharex=True)

df_agg.loc[:, 'Dst'].plot(ax=ax[0])
df_agg.loc[:, 'mep06'].plot(ax=ax[1])
df_agg.loc[:, 'me03'].plot(ax=ax[2])
plt.show()