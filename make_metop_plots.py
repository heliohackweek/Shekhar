import matplotlib.pyplot as plt
import pandas as pd

import read_csv_dict

file_name = './csv_daily_data/data_metop0220061206.csv'
df = read_csv_dict.load_meped_csv(file_name)

# df = df[df.mlt > 20 ]
# df.hist()
pd.plotting.scatter_matrix(df, alpha=0.2)
# df.plot()
# plt.tight_layout()
plt.show()