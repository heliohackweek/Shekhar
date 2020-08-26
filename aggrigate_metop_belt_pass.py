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

import read_csv

orbit_period_min = 25
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

# Groupby orbit
groups = df_filtered.groupby(pd.Grouper(freq=f'{orbit_period_min}min'))

df_agg = groups.agg(['min', 'mean', 'max', 'median'])

### Print the aggrigated values.
multiindex_tuples = [('Kp', 'median'), ('mep06', 'median'), ('mep05', 'median')]
print(df_agg.loc[:, multiindex_tuples])

# Pick one stat method and flatten df_agg multi-index.
df_agg_flattened = df_agg.loc[:, (slice(None), stat_method)]
df_agg_flattened.columns = df_agg_flattened.columns.get_level_values(0)
# Add suffix to remind the user what stat do these values represent.
# df_agg_flattened.columns += f'_{stat_method}'
# Save to a csv file after dropping nans.
df_agg_flattened = df_agg_flattened.dropna(axis=0)
df_agg_flattened.to_csv(f'metop_rad_belt_passes_{stat_method}.csv')

### PLOTS ###
fig, ax = plt.subplots(3, 1, sharex=True)

df_agg.loc[:, 'Dst'].plot(ax=ax[0])
df_agg.loc[:, 'mep06'].plot(ax=ax[1])
df_agg.loc[:, 'me03'].plot(ax=ax[2])
plt.show()