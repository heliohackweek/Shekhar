import csv
from datetime import datetime
import re

import numpy as np
import pandas as pd

def load_meped_csv(file_name, as_df=True):
    """
    Load the meped data into a dictionary or a pandas 
    DataFrame, togled by the as_df kwarg.
    """
    numeric_date = re.findall(r'\d+', file_name)[0]
    date_obj = datetime.strptime(numeric_date[2:], '%Y%m%d')

    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        mydict = dict(reader)

        for key, val in mydict.items():
            # Remove all of the non-numeric characters
            val = val.replace('\n', '')
            val = val.replace('[', '')
            val = val.replace(']', '')

            mydict[key] = np.array(val.split()).astype(float)

        if as_df:
            df = pd.DataFrame(data=mydict)
            df['dateTime'] = (date_obj + pd.to_timedelta(df['Hour'], unit='h') + 
                                            pd.to_timedelta(df['minute'], unit='m') + 
                                            pd.to_timedelta(df['second'], unit='s'))
            df.index = df['dateTime']
            del(df['dateTime'])
            return df
        else:
            return mydict

if __name__ == "__main__":   
    file_name = 'data_metop0220061203.csv'
    df = load_meped_csv(file_name)
    print(df)