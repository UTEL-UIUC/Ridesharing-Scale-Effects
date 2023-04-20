import os
import math
import numpy as np
import pandas as pd

def data_read(folder, mode, type_of_data, region = None):
    """
    This function reads a CSV file containing aggregated data for a specific type of trip and returns it
    as a pandas dataframe.
    
    Args:
      folder: The folder parameter is a string that represents the directory path where the data file is
    located.
      mode: The "mode" parameter likely refers to the type of data being read, such as "train" or "test"
    data.
      type_of_data: The type of data being read, which is likely a specific feature or attribute of the
    trips being analyzed. Examples could include "duration", "distance", "fare", "pickup_time", etc.
    
    Returns:
      a pandas DataFrame that is read from a CSV file located in the specified folder, with a file name
    that is constructed based on the input parameters `mode`, `type_of_data`, and the fixed string
    '_trips_df_' and '_agg.csv'.
    """
    if region is None:
        path = os.path.join(folder, mode + '_trips_df_' + type_of_data + '_agg.csv')
    else:
        path = os.path.join(folder, region, mode + '_trips_df_' + type_of_data + '_agg.csv')
    df = pd.read_csv(path) 
    return df

def data_read2(folder, mode, type_of_data, region = None):
    """
    This function reads a CSV file containing aggregated trip data from a specified folder and returns
    it as a pandas dataframe.
    
    Args:
      folder: The folder parameter is a string that represents the directory path where the data file is
    located.
      mode: The mode parameter is a string that specifies the type of data being read. It could be
    'train', 'test', or 'validation'.
      type_of_data: The type of data being read, which is likely a variable such as "income" or "race".
    
    Returns:
      a pandas DataFrame that is read from a CSV file located in the specified folder. The CSV file name
    is constructed using the input parameters `mode`, `type_of_data`, and a fixed string.
    """
    if region is None:
        path = os.path.join(folder, mode + '_trips_df_' + type_of_data + '_agg_tract.csv')
    else:
        path = os.path.join(folder, region, mode + '_trips_df_' + type_of_data + '_agg_tract.csv')
    df = pd.read_csv(path) 
    return df

def data_agg(df, base):
    """
    This function aggregates data from a dataframe and calculates various metrics related to ride
    sharing, such as total fares, trip distances, and percentages of shared rides, and categorizes the
    data into time intervals.
    
    Args:
      df: a pandas DataFrame containing the data to be aggregated
      base: The base parameter is a list of columns to group the data by for aggregation.
    
    Returns:
      The function `data_agg` returns a pandas DataFrame that aggregates and calculates various metrics
    based on the input DataFrame `df` and grouping variable `base`.
    """
    df['fare_total_shared_realized_total'] = df['fare_total_shared_realized']*df['count_shared_realized']
    df['fare_total_single_realized_total'] = df['fare_total_single_realized']*df['count_single_realized']
    df['trip_miles_shared_realized_total'] = df['trip_miles_shared_realized']*df['count_shared_realized']
    df['trip_miles_single_realized_total'] = df['trip_miles_single_realized']*df['count_single_realized']
    df['trip_seconds_shared_realized_total'] = df['trip_seconds_shared_realized']*df['count_shared_realized']
    df['trip_seconds_single_realized_total'] = df['trip_seconds_single_realized']*df['count_single_realized']
    df_agg = df.groupby(base).agg(count_shared_realized_total = ('count_shared_realized', 'sum'), \
                                                                            count_shared_realized_mean = ('count_shared_realized', 'mean'), \
                                                                            count_shared_requested_total = ('count_shared_requested', 'sum'), \
                                                                            count_shared_requested_mean = ('count_shared_requested', 'mean'), \
                                                                            count_single_realized_total = ('count_single_realized', 'sum'), \
                                                                            count_single_realized_mean = ('count_single_realized', 'mean'),\
                                  fare_total_shared_realized_total = ('fare_total_shared_realized_total', 'sum'),\
                                  fare_total_single_realized_total = ('fare_total_single_realized_total', 'sum'),\
                                  trip_miles_shared_realized_total = ('trip_miles_shared_realized_total', 'sum'),\
                                  trip_miles_single_realized_total = ('trip_miles_single_realized_total', 'sum'),\
                                  trip_seconds_shared_realized_total = ('trip_seconds_shared_realized_total', 'sum'),\
                                  trip_seconds_single_realized_total = ('trip_seconds_single_realized_total', 'sum')\
                                                                ).reset_index()
    df_agg['fare_minute_single_realized_mean'] = df_agg['fare_total_single_realized_total']/df_agg['trip_seconds_single_realized_total']*60
    df_agg['fare_minute_shared_realized_mean'] = df_agg['fare_total_shared_realized_total']/df_agg['trip_seconds_shared_realized_total']*60
    df_agg['fare_mile_single_realized_mean'] = df_agg['fare_total_single_realized_total']/df_agg['trip_miles_single_realized_total']
    df_agg['fare_mile_shared_realized_mean'] = df_agg['fare_total_shared_realized_total']/df_agg['trip_miles_shared_realized_total']
    df_agg['count_total_total'] = df_agg['count_shared_realized_total'] + df_agg['count_single_realized_total']
    df_agg['count_mean_total'] = df_agg['count_shared_realized_mean'] + df_agg['count_single_realized_mean']
    df_agg['requested_percent'] = df_agg['count_shared_requested_total']/df_agg['count_total_total']*100
    df_agg['matched_percent'] = df_agg['count_shared_realized_total']/df_agg['count_shared_requested_total']*100
    df_agg['cost_ratio_minute'] = df_agg['fare_minute_shared_realized_mean']/df_agg['fare_minute_single_realized_mean']
    df_agg['cost_ratio_mile'] = df_agg['fare_mile_shared_realized_mean']/df_agg['fare_mile_single_realized_mean']
    df_agg['interval'] = "AM Peak"
    df_agg.loc[(df_agg['pickup_hour']>6) & (df_agg['pickup_hour']<13), 'interval'] = "Mid-day"
    df_agg.loc[(df_agg['pickup_hour']>=13) & (df_agg['pickup_hour']<=18), 'interval'] = "PM Peak"
    df_agg.loc[(df_agg['pickup_hour']>18) | (df_agg['pickup_hour']<4), 'interval'] = "Night"
    colors = {'Night':'blue', 'AM Peak':'orange', 'Mid-day':'green', 'PM Peak':'red'}
    symbols = {'Night':'o', 'AM Peak':'^', 'Mid-day':'s', 'PM Peak':'D'}
    df_agg['colors'] = df_agg['interval'].map(colors)
    df_agg['markers'] = df_agg['interval'].map(symbols)
    return df_agg

def agg_hdm(folder, region= None):
    """
    The function aggregates data from different sources and creates a dataframe with calculated trip
    durations, and adds a column indicating the month class.
    
    Args:
      region: The region parameter is a string that specifies the geographic region for which the
    function will aggregate data.
    
    Returns:
      The function `agg_hdm(region)` is returning a pandas DataFrame `df_hdm` with aggregated data on
    trip durations for single and shared rides, grouped by pickup hour, day, and month, and with an
    additional column indicating whether the pickup month is before or after September/October.
    """
    df_shared_requested = data_read(folder,'shared','requested',region)
    df_shared_realized = data_read(folder,'shared','realized',region)
    df_single_realized = data_read(folder,'single','realized',region)
    df_merged = df_single_realized.merge(df_shared_realized, on=['pickup_hour', 'pickup_date', 'pickup_day', 'pickup_month'], how = 'inner')
    df_merged = df_merged.merge(df_shared_requested, on=['pickup_hour', 'pickup_date', 'pickup_day', 'pickup_month'], how = 'inner')
    df_merged['trip_minutes_single_realized'] = df_merged['trip_seconds_single_realized']/60
    df_merged['trip_minutes_shared_realized'] = df_merged['trip_seconds_shared_realized']/60
    df_hdm = data_agg(df_merged, ['pickup_hour','pickup_day','pickup_month'])
    df_hdm['month_class'] = "pre-Sep"
    df_hdm.loc[(df_hdm['pickup_month']>=10), 'month_class'] = "post-Oct"
    return df_hdm

def data_agg_weekday_new(df):
    """
    This function aggregates data by weekday, pickup hour, and pickup day, calculates the percentage of
    shared rides requested, and categorizes the pickup hour as day or night.
    
    Args:
      df: a pandas DataFrame containing ride-sharing data with columns 'pickup_hour', 'weekday',
    'pickup_day', 'count_total', 'count_total2', and 'count_shared_requested'.
    
    Returns:
      The function `data_agg_weekday_new` is returning a pandas DataFrame with aggregated data for each
    combination of pickup hour, weekday, and pickup day. The aggregated data includes the mean of
    `count_total`, the sum of `count_total`, and the sum of `count_shared_requested`. Additionally, the
    function calculates a new column `d or n` based on the pickup hour, and a new column
    """
    df_weekday = df.groupby(['pickup_hour', 'weekday', 'pickup_day']).agg(count_total=('count_total', 'mean'), \
                                                                          count_total2 = ('count_total', 'sum'), \
                                                                          count_shared_requested=('count_shared_requested', 'sum')).reset_index()
    df_weekday['d or n'] = 30
    df_weekday.loc[(df_weekday['pickup_hour'] >= 4) & (df_weekday['pickup_hour'] <= 18),'d or n'] = 70
    df_weekday['requested_per'] = df_weekday['count_shared_requested']/df_weekday['count_total2']*100
    return df_weekday

def df_day(folder,region = None):
    """
    This function takes a region as input, reads data from different sources, merges them, calculates
    various percentages, maps weekdays and weekends, and aggregates the data by weekday.
    
    Args:
      region: The region parameter is a string that specifies the geographic region for which the data
    is being analyzed.
    
    Returns:
      The function `df_day(region)` returns a dataframe `df_merged_weekday_new` after performing some
    data processing and aggregation operations on the input dataframes `df_shared_requested`,
    `df_shared_realized`, and `df_single_realized`.
    """
    df_shared_requested = data_read(folder,'shared', 'requested', region)
    df_shared_realized = data_read(folder,'shared', 'realized', region)
    df_single_realized = data_read(folder,'single', 'realized', region)
    df_merged = df_single_realized.merge(df_shared_realized, on=['pickup_hour', 'pickup_date', 'pickup_day', 'pickup_month'], how = 'inner')
    df_merged = df_merged.merge(df_shared_requested, on=['pickup_hour', 'pickup_date', 'pickup_day', 'pickup_month'], how = 'inner')
    df_merged['count_total'] = df_merged['count_single_realized'] + df_merged['count_shared_realized']
    df_merged['requested_per'] = df_merged['count_shared_requested']/df_merged['count_total']*100
    df_merged['realized_per'] = df_merged['count_shared_realized']/df_merged['count_total']*100
    df_merged['realized_per2'] = df_merged['count_shared_realized']/df_merged['count_shared_requested']*100
    days = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    df_merged['weekday'] = df_merged['pickup_day'].map(days)
    df_merged['weekday_weekend'] = "Weekend"
    df_merged.loc[(df_merged['pickup_day'] >= 0) & (df_merged['pickup_day'] <= 4),'weekday_weekend'] = 'Weekday'
    df_merged['d or n'] = 10
    df_merged.loc[(df_merged['pickup_hour'] >= 4) & (df_merged['pickup_hour'] <= 18),'d or n'] = 50
    df_merged_weekday_new = data_agg_weekday_new(df_merged[df_merged['pickup_month']<13])
    return df_merged_weekday_new

def df_day_Jan_Sep(folder, region):
    """
    This function aggregates and processes data related to ride requests and realizations for weekdays
    and weekends in a given region from January to September.
    
    Args:
      region: The region for which the function will retrieve and process data.
    
    Returns:
      a dataframe that has been aggregated and filtered based on certain conditions. The dataframe
    contains information about the number of shared and single rides requested and realized, as well as
    the percentage of shared rides requested and realized. It also includes information about the day of
    the week and whether it is a weekday or weekend, and whether the pickup time is during the day or
    night.
    """
    df_shared_requested = data_read(folder,'shared', 'requested', region)
    df_shared_requested = df_shared_requested[df_shared_requested['pickup_month']<=9]
    df_shared_realized = data_read(folder,'shared', 'realized', region)
    df_shared_realized = df_shared_realized[df_shared_realized['pickup_month']<=9]
    df_single_realized = data_read(folder,'single', 'realized', region)
    df_single_realized = df_single_realized[df_single_realized['pickup_month']<=9]
    df_merged = df_single_realized.merge(df_shared_realized, on=['pickup_hour', 'pickup_date', 'pickup_day', 'pickup_month'], how = 'inner')
    df_merged = df_merged.merge(df_shared_requested, on=['pickup_hour', 'pickup_date', 'pickup_day', 'pickup_month'], how = 'inner')
    df_merged['count_total'] = df_merged['count_single_realized'] + df_merged['count_shared_realized']
    df_merged['requested_per'] = df_merged['count_shared_requested']/df_merged['count_total']*100
    df_merged['realized_per'] = df_merged['count_shared_realized']/df_merged['count_total']*100
    df_merged['realized_per2'] = df_merged['count_shared_realized']/df_merged['count_shared_requested']*100
    days = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    df_merged['weekday'] = df_merged['pickup_day'].map(days)
    df_merged['weekday_weekend'] = "Weekend"
    df_merged.loc[(df_merged['pickup_day'] >= 0) & (df_merged['pickup_day'] <= 4),'weekday_weekend'] = 'Weekday'
    df_merged['d or n'] = 10
    df_merged.loc[(df_merged['pickup_hour'] >= 4) & (df_merged['pickup_hour'] <= 18),'d or n'] = 50
    df_merged_weekday_new = data_agg_weekday_new(df_merged[df_merged['pickup_month']<13])
    return df_merged_weekday_new

def merge_tract_trips_weekdays(folder):
    """
    This function merges two dataframes of weekday taxi trips and calculates the total count of trips
    for each origin-destination pair.
    
    Args:
      folder: The folder parameter is a string that represents the directory path where the data files
    are stored.
    
    Returns:
      a merged dataframe of two input dataframes, with additional columns for total count and
    origin-destination (OD) pairs. The input dataframes are filtered for weekdays and specific time
    periods.
    """
    df1 = data_read2(folder,'shared', 'realized')
    df1 = df1[(df1['pickup_day']<4) | ((df1['pickup_day']==4) & (df1['pickup_hour']<=14))]
    df1['Dropoff Census Tract'] = df1['Dropoff Census Tract'].astype(np.int64)
    df1['Pickup Census Tract'] = df1['Pickup Census Tract'].astype(np.int64)
    df2 = data_read2(folder,'single', 'realized')
    df2['Dropoff Census Tract'] = df2['Dropoff Census Tract'].astype(np.int64)
    df2['Pickup Census Tract'] = df2['Pickup Census Tract'].astype(np.int64)
    df_merged = df2.merge(df1, on=['Pickup Census Tract', 'Dropoff Census Tract', 'pickup_hour', 'pickup_date', 'pickup_day', 'pickup_month'], how = 'inner')
    df_merged['count_total'] = df_merged['count_shared_realized'] + df_merged['count_single_realized']
    df_merged['OD'] = df_merged['Pickup Census Tract'].astype(str) + df_merged['Dropoff Census Tract'].astype(str)
    return df_merged