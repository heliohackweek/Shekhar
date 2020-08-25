"""

"""

import pathlib

import matplotlib.pyplot as plt
import pandas as pd

import read_csv

orbit_period_min = 101

# Search for all the metop csv files.
metop_dir = pathlib.Path('./csv_daily_data/')
metop_paths = sorted(list(metop_dir.glob('data_metop*.csv')))

# Make a list of the metop DataFrames and concatenate 
# them into one. 
df_list = [read_csv.load_meped_csv(str(metop_path)) 
            for metop_path in metop_paths]
df_concat = pd.concat(df_list)

# Filter by the Lval to get only the radiation belt values
df_concat = df_concat[(df_concat.Lval > 4) & 
                      (df_concat.Lval < 8) & 
                      (df_concat.mlt > 18)]

# Groupby orbit
groups = df_concat.groupby(pd.Grouper(freq=f'{orbit_period_min}min'))

# for key, group in groups:
#     print(key, '\n', group.loc[:, ['Lval', 'mlt', 'mep06']])

agg_df = groups.agg(['min', 'mean', 'max'])
print(agg_df.loc[:, [('Kp', 'mean')]])

fig, ax = plt.subplots(2, 1)

agg_df.loc[:, 'Dst'].plot(ax=ax[0])
agg_df.loc[:, 'mep06'].plot(ax=ax[1])
plt.show()