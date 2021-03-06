"""
Make a scatter_matrix summary metop plot for all 
data_metop... plots in the csv_daily_data/ directpry.
"""

import pathlib

import matplotlib.pyplot as plt
import pandas as pd

import read_csv

# Search for all the metop csv files.
metop_dir = pathlib.Path('./csv_daily_data/')
metop_paths = sorted(list(metop_dir.glob('data_metop*.csv')))

# Make a list of the metop DataFrames and concatenate 
# them into one. 
df_list = [read_csv.load_meped_csv(str(metop_path)) 
            for metop_path in metop_paths]
df_concat = pd.concat(df_list)

### Make plots! ###
# df = df[df.mlt > 20 ] # Filter by MLT.
# df.hist()
pd.plotting.scatter_matrix(df_concat, alpha=0.2)
# df.plot()
plt.show()