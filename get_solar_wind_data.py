from datetime import datetime, timedelta
import dateutil.parser

import h5py
import pandas as pd
import numpy as np
import spacepy.omni

# Suppress the h5py warning (the warning that is triggered by the 
# spacepy.omni.get_omni()).
h5py.get_config().default_file_mode = 'r'


def download_solar_wind(t, lag_hr, dbase='QDhourly', to_df=True):
    """
    Given a start time in strng or datetime.datetime format,
    use the spacepy library to download the solar wind data
    for the time range [t-lag_hr, t], where lag_hr is the 
    integer or float hour lag.

    The dbase kwarg is passed directly into spacepy.omni.get_omni
    to get hourly solar wind values.

    to_df converts the solar wind data to a pandas DataFrame after
    throwing away some of the derived products.

    NOTE: the output uses the lag_hr INCLUSIVE so the number of 
    output time stamps is 1 greater than lag_hr.
    """
    if isinstance(t, str):
        t = dateutil.parser.parse(t)
    omni_times = pd.date_range(t-timedelta(hours=lag_hr), t, freq='h')
    try:
        data = spacepy.omni.get_omni(omni_times.to_pydatetime(), dbase=dbase)
    except ValueError as err:
        if str(err) == 'Requested dates are outside data range':
            print(f"For time {t} spacepy thinks it's out of range. If you "
                   "don't have the data, run these two commands:\n"
                   "import spacepy.toolbox as tb\n"
                   "tb.update(omni=True)")

    if to_df: # Return a DataFrame
        cast_data_dict = {}
        # Lots of finess going on here. We need to treat the ticks key
        # carefully because it is a spacepy.time.Ticktock object.
        # Also do make it compatable with a DataFrame, I removed the
        # Tsyganenko derived inpputs G and W.
        for key, val in data.items():
            # if key == 'ticks':
            #     cast_data_dict[key] = np.array(val.UTC)
            if key in ['G', 'W', 'Qbits','ticks']:
                continue
            else:
                cast_data_dict[key] = np.array(val)
        df = pd.DataFrame(data=cast_data_dict) 
        df.index=df.UTC
        df = df.drop(['UTC'], axis=1)
        return df
    else:
        # Return a dictionary of spacepy dmarrays
        return data 

if __name__ == "__main__":
    t = '2002-02-02T12:00:00'
    lag_hr = 4
    data = download_solar_wind(t, lag_hr)
    print(data.head())