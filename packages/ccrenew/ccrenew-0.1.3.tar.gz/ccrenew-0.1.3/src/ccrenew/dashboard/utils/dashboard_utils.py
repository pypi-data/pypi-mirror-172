from datetime import (
    datetime,
    timedelta
)
import functools
import logging
from numbers import Number
import os
from pandas import (
    DataFrame,
    read_csv,
    read_excel
)
import re
import sys
from time import time
from typing import Union

from ccrenew.dashboard.data_processing import Bluesky_weather_fucntions_v01 as blu
from ccrenew.dashboard.data_processing.CCR import all_df_keys as df_keys

logger = logging.getLogger(__name__)

class FileNotFoundError(Exception):
    pass

class FileOpenError(Exception):
    pass


def dict_insert(dict_, key, value):
    """Checks if a key already exists in dict, creates new key if not.
    Prevents overwriting of existing dictionary entries.

    Args:
        dict_ (dict): Dictionary to update.
        key (str): Key to check.
        value (str): Value to update if key doesn't exist.

    Returns:
        dict: Updated dictionary.
    """
    if key in dict_:
        pass
    else:
        dict_[key] = value
    return dict_

def picklefy_project_name(project_name):
    """Modifies the project name for pickling.

    Args:
        project_name (str): The "official" project name with spaces, commas, apostrophe's, and all that fun stuff
        year (int): The year to save for the pickle. Defaults to the current year.

    Returns:
        str: The picklefied project name.
    """
    project_name = re.sub("(,\s)|[,\s]", "_", project_name)
    project_name = re.sub("[']", "", project_name)

    return project_name

def get_snow_df(dashboard_folder, data_source):
    """Pulls snow data & returns a dataframe. Temporary fix for now, need to
    update path references

    Returns:
        DataFrame: Snow data
    """
    snow_file = os.path.join(dashboard_folder, 'Python_Functions', 'Snow Losses', '{}Operating-States-snowfall.xlsx'.format(data_source))
    raw_snow_df = read_excel(snow_file)

    return raw_snow_df

def retrieve_s3_df(bucket, key):
# helper function to get data from s3
    path = "s3://{b}/{k}".format(b=bucket, k=key)
    try:
        df = read_csv(path, index_col=0, parse_dates=True)
        df = df.loc[~df.index.duplicated(), :]
    except IOError:
        return DataFrame()
    return df

def run_bluesky(project_name, start=None, end=None, plot=True):
    """Pulls irradiance & weather data from Solcast for the project & date range.

    Args:
        project (Project): The `Project` object to use for the Solcast script.
        start (str, datetime, or date, optional): The start date for Solcast data. Defaults to first day of the current month.
        end (str, datetime, or date, optional): The end date for Solcast data. Defaults to the day before the script is run.

    Returns:
        DataFrame: The Solcast irradiance & weather data.
    """
    
    tz='US/'+str(df_keys.query("index == '{}'".format(project_name))['Timezone'].values[0])

    # Get default dates if not provided.
    if not start:
        today = datetime.today()
        start = datetime(today.year, today.month, 1)
    if not end:
        today = datetime.today()
        end = today - timedelta(days=1)

    df_cats,df_units=blu.solcats_to_dash(project_name,start,end,resample=True,convert=False)
    df_cats = df_cats.tz_localize(None)

    try:
        df_poa=blu.site_s3_to_poa(project_name, start, end).tz_convert(tz).tz_localize(None)
        df_cats['sites_ghi_poa'] = df_poa
        df_cats.loc[:, 'site'] = project_name
        if plot:
            df_cats[['poa','ghi', 'sites_ghi_poa']].plot()
    except IndexError:
        print('No GHI to transpose! Solcast POA only')
        if plot:
            df_cats[['poa','ghi']].plot()    

    df_cats.to_clipboard()
    print('\n')
    print('Solcast data successfully returned for {}'.format(project_name))
    print('\n')
    return df_cats

# Decorator function for timing the execution of functions
def func_timer(func):
    """Decorator for timing the execution of functions.

    Args:
        func (function): Function to time.
    """
    # Initiate logger
    logger = logging.getLogger('timer')

    @functools.wraps(func)
    def timer(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        elapsed = time() - start

        # Build custom message for the logger so it doesn't just show that each
        # call came from the `timer()` function
        # Python 2 compatibility
        # Python 2 compatibility
        if sys.version_info.major == 3:
            file_str = 'File: {}'.format(os.path.basename(func.__code__.co_filename))
            line_str = 'Line: {}'.format(func.__code__.co_firstlineno)
        else:
            file_str = 'File: {}'.format(os.path.basename(func.func_code.co_filename))
            line_str = 'Line: {}'.format(func.func_code.co_firstlineno)

        log_msg = {
            'file': file_str,
            'module': 'Module: {}'.format(func.__module__),
            'function': 'Function: {}'.format(func.__name__),
            'line_no': line_str,
            'func_name': func.__name__,
            'elapsed': elapsed
        }
        # Check if the function call comes from a project, if so we'll add the project name to the log message
        try:
            log_msg['project_name'] = args[0].project_name
            message = '{file}\t{module}\t{function}\t{line_no}\tFunction call `{func_name}` for {project_name} complete. Total time: {elapsed:7.3f}s'.format(**log_msg)
        except AttributeError:
            message = '{file}\t{module}\t{function}\t{line_no}\tFunction call `{func_name}` complete. Total time: {elapsed:7.3f}s'.format(**log_msg)
        logger.info(message)

        return result
    return timer

def update_config(func):
    """Decorator to update the config file if necessary before running a function.

    Args:
        func (function): Function that will need an updated config file.
    """
    @functools.wraps(func)
    def check_config(self, *args, **kwargs):
        if self.last_update_config != os.path.getmtime(self.config_filepath):
            self._parse_config_file()
        return func(self, *args, **kwargs)
    return check_config
