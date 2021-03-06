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
import get_solar_wind_data


class AggMetopRadPasses:
    def __init__(self, csv_dir='csv_daily_data/', stat_method='median'):
        """
        This class handles the algorithm to load all of the metop csv 
        files and aggrigate the csv data for each radiation belt pass.
        """
        self.stat_method=stat_method
        self.csv_dir = csv_dir
        self.merge_metop_csv()
        return

    def merge_metop_csv(self, glob_regex='data_metop*.csv'):
        """
        Load each metop csv file and concat them into one large DataFrame 
        (this will work for a small dataset, but will have to be adjusted 
        for the entire dataset.)
        """
        # Search for all the metop csv files.
        metop_dir = pathlib.Path(self.csv_dir)
        metop_paths = sorted(list(metop_dir.glob(glob_regex)))

        # Make a list of the metop DataFrames and concatenate 
        # them into one. 
        df_list = [read_csv.load_meped_csv(str(metop_path)) 
                    for metop_path in metop_paths]
        self.df_concat = pd.concat(df_list)
        return
    
    def filter_df(self, L_range=[4,8]):
        """
        A default filter for the concinated metop csv files. Only
        the L shell range is adjustable via the API.

        Filter by the Lval to get only the radiation belt values.
        Additional filters include: mep05 == 0 and 
        me03 > mep06 to remove contamination
        """
        self.df_filtered = self.df_concat[
                            (self.df_concat.Lval > 4) & 
                            (self.df_concat.Lval < 8) & 
                            #   (self.df_concat.mlt > 16) &
                            (self.df_concat.mep05 == 0) &
                            (self.df_concat.me03 > self.df_concat.mep06)]
        return

    def _findTimeBreaks(self, time, threshold_min=10):
        """
        Find time breaks in the the time array greater than threshold_min 
        """
        dt = (time[1:] - time[:-1]).seconds
        consecutiveFlag = np.where(dt > threshold_min*60)[0]
        startInd = np.insert(consecutiveFlag+1, 0, 0)
        endInd = np.insert(consecutiveFlag, len(consecutiveFlag), len(time)-1) + 1
        return startInd, endInd

    def agg_passes(self, threshold_min=10):
        """
        Split up self.df_filtered by the radiation belt passes and apply the 
        self.stat_method aggrigation function to the radiation belt chunks.
        """
        # Find the radiation belt start and end incides passes.  
        startInd, endInd = self._findTimeBreaks(self.df_filtered.index)

        # Now we know how many radiation belt passes there are, create and populate a DataFrame
        # with the aggrigate values.
        self.df_agg = pd.DataFrame(
                                data=np.nan*np.ones(
                                    (len(startInd), len(self.df_filtered.columns))
                                    ), 
                                columns=self.df_filtered.columns, 
                                index=np.array(self.df_filtered.index)[startInd]
                                )
        # Loop over each start-end radiation pass index and aggrigate the columns for each 
        # sub-DataFrame
        for i, (start_index, end_index) in enumerate(zip(startInd, endInd)):
            sub_df = self.df_filtered.iloc[start_index:end_index, :]
            self.df_agg.iloc[i, :] = sub_df.agg(self.stat_method)

        return

    def save_agg_data(self, save_file_name=None):
        """
        Save the aggrigated file to a csv file. If save_file_name is None,
        a generic filename, 'metop_rad_belt_passes_{self.stat_method}.csv',
        will be used.
        """
        if save_file_name is None:
            save_file_name = f'metop_rad_belt_passes_{self.stat_method}.csv'
        self.df_agg.to_csv(save_file_name, index_label='dateTime')
        return


class AppendSW(AggMetopRadPasses):
    def __init__(self, csv_dir='csv_daily_data/', stat_method='median'):
        """
        Child class of AggMetopRadPasses that adds functionality to add
        the solar wind (SW) data with one time lag and at some point it 
        will include a lag time series.
        """
        super().__init__(csv_dir=csv_dir, stat_method=stat_method)
        return

    def append_single_sw_lag(self, lag_hr):
        """
        Replaces the SW columns in df_agg with the 
        time-lagged parameter lag_hr prior.
        """
        if not hasattr(self, 'df_agg'):
            raise AttributeError('df_agg does not exist. Try running'
                        ' the filter_df and agg_passes methods first.')

        for t_i in self.df_agg.index:
            # Get the solar wind parameters
            sw_df = get_solar_wind_data.get_solar_wind_data(
                t_i-pd.Timedelta(hours=lag_hr), lag_hr=0)
            # Awfull indexing, but seems to work!
            copy_keys = ['dens', 'velo', 'Pdyn', 'ByIMF','BzIMF']
            self.df_agg.loc[t_i, copy_keys] = sw_df.loc[:, copy_keys].to_numpy()
        return

    def append_multiple_sw_lag(self, max_lag_hr, single_level_index=True):
        """
        Appends the SW columns in df_agg with the time-lagged time history 
        of parameters up to max_lag_hr prior. The lagged keys have the 
        "_lagN" suffix where N is the lag in the number of hours.
        """
        if not hasattr(self, 'df_agg'):
            raise AttributeError('df_agg does not exist. Try running'
                        ' the filter_df and agg_passes methods first.')

        # Create the keys with the _lagN suffix and make a 
        sw_keys = ['dens', 'velo', 'Pdyn', 'ByIMF','BzIMF']
        if single_level_index:
            lagged_keys = np.ones((len(sw_keys), (max_lag_hr+1)), dtype=object)
            for i, sw_key in enumerate(sw_keys):
                # for j, lag_hr in enumerate(np.arange(max_lag_hr, -1, -1)):
                for j, lag_hr in enumerate(np.arange(max_lag_hr+1)):
                    lagged_keys[i, j] = f'{sw_key}_lag{lag_hr}'
            # Flatten the 2d keys array for the csv
            lagged_keys = lagged_keys.flatten()
        else:
            # EXPERMINETAL!
            lagged_keys = pd.MultiIndex.from_product([sw_keys, np.arange(max_lag_hr+1)],
                           names=['sw', 'lag'])
        self.df_sw = pd.DataFrame(index=self.df_agg.index, columns=lagged_keys)

        for t_i in self.df_agg.index:
            # Get the solar wind parameters
            df_sw_one_set = get_solar_wind_data.get_solar_wind_data(t_i, lag_hr=max_lag_hr)
            
            for sw_key in sw_keys:
                one_set_of_lagged_keys = [key for key in self.df_sw if sw_key in key]
                self.df_sw.loc[t_i, one_set_of_lagged_keys] = df_sw_one_set.loc[:, sw_key].to_numpy()[::-1]
        self.df_agg = self.df_agg.merge(self.df_sw, left_index=True, right_index=True)
        return



if __name__ == '__main__':
    ### The API for the basic aggrigate class.
    # agg = AggMetopRadPasses(stat_method='median')
    # agg.filter_df()
    # agg.agg_passes()
    # agg.save_agg_data()

    ### The same API as above and it changes the solar wind parameters 
    ### to the ones lag_hr prior.
    lag_hr=6
    agg = AppendSW(stat_method='median')
    agg.filter_df()
    agg.agg_passes()
    agg.append_multiple_sw_lag(6)
    # agg.append_single_sw_lag(lag_hr)
    save_file_name=f'metop_rad_belt_{agg.stat_method}_vals_lagged_sw.csv'
    agg.save_agg_data(save_file_name=save_file_name)

    # ### PLOTS ###
    # fig, ax = plt.subplots(3, 1, sharex=True)

    # agg.df_agg.loc[:, 'Dst'].plot(ax=ax[0])
    # agg.df_agg.loc[:, 'mep06'].plot(ax=ax[1])
    # agg.df_agg.loc[:, 'me03'].plot(ax=ax[2])
    # plt.show()