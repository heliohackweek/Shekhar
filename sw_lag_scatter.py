import matplotlib.pyplot as plt
import pandas as pd

import example_load_sw_lagged_data

# Load in the data
stat_method = 'max'
file_name=f'metop_rad_belt_{stat_method}_vals_lagged_sw.csv'
df = pd.read_csv(file_name, index_col=0, parse_dates=True)
# df=df[df.mlt > 16]
df=df[df.mep06 > 3]
print(df.shape[0])

sw_keys = ['dens', 'velo', 'Pdyn', 'ByIMF','BzIMF']

df2 = example_load_sw_lagged_data.pick_lagged_sw_data(df, 'dens', verbose=False)
fig, ax = plt.subplots(len(sw_keys), df2.shape[1], figsize=(15, 10))

for i, sw_key in enumerate(sw_keys):
    # Get the lagged solar wind parameters
    df2 = example_load_sw_lagged_data.pick_lagged_sw_data(df, sw_key, verbose=False)
    for j, lag_key in enumerate(df2.columns):
        ax[i,j].scatter(df.mep06, df2.loc[:, lag_key], label=f'lag={lag_key} hr', alpha=0.3)
        ax[i,j].legend()
        ax[i,j].set_ylabel(sw_key)
        ax[i,j].set_xlabel('mep06')

fig2, ax2 = plt.subplots()
ax2.hist(df.mlt)

fig3, ax3 = plt.subplots()
ax3.scatter(df.mep06, df.mlt)

plt.tight_layout()
plt.show()