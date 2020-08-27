"""
Example of how to load the lagged solar wind data
"""
import re

import numpy as np
import pandas as pd

def pick_lagged_sw_data(df, sw_param, verbose=True, rename_cols=True):
    """
    Given a DataFrame and a solar wind parameter from this list:
    ['dens', 'velo', 'Pdyn', 'ByIMF','BzIMF'], extract the relevant
    sw columns from the DataFrame and return the condensed dataframe.
    
    if verbose is True, will print what the picked keys are and what the 
    keys will be renamed to (if rename_cols is True as well.)
    
    If rename_cols is True, the column format of "sw_param"_lagN for the
    solar wind parameter sw_param N hours prior, the column will be renamed
    to just N, the lag time in hours.
    """
    sw_cols = [col for col in df.columns if sw_param in col]
    sw_cols.remove(sw_param) # Remove the column from the original csv file.
    if verbose: print('Picked these columns:', sw_cols)

    df_sw = df.loc[:, sw_cols]
    if rename_cols:
        # Use list comprehensions to remname the sw columns, using
        # regular expressions to pick out the integer values in the
        # old column name.
        new_columns = np.array([re.search('\d+', column).group(0) 
                                for column in sw_cols]).astype(float)
        df_sw.columns = new_columns
        if verbose: 
            print('Renamed the lag columns to:', new_columns)
    return df_sw

if __name__ == "__main__":
    stat_method = 'median'
    file_name=f'metop_rad_belt_{stat_method}_vals_lagged_sw.csv'

    # Index col and parse dates just converts the datetime string 
    # column into datetime objects
    df = pd.read_csv(file_name, index_col=0, parse_dates=True)
    df2 = pick_lagged_sw_data(df, 'velo')
    print(df2)