"""
Functions to process & convert dates and times

Matt Nicholson
7 April 2020
"""
import datetime
import numpy as np


def time_val_to_date(time_var, time_val):
    """
    Calculate a date from a time variable value.
    
    Parameters
    ----------
    time_var : NetCDF4 Variable object
        NetCDF time variable.
    time_val : float
        Time variable value.
    
    Returns
    -------
    str : Converted time in the format YYYY-MM-DD
    """
    t_0 = time_var.units.split(' ')[2]
    t_0 = datetime.datetime.strptime(t_0, '%Y-%m-%d')
    t_curr = t_0 + datetime.timedelta(days=time_val)
    t_curr = t_curr.strftime('%Y-%m-%d')
    return t_curr
    
    
def date_to_time_val(time_var, date):
    """
    Calculate a time variable value from a date.
    
    Parameters
    ----------
    time_var : NetCDF4 Variable object
        NetCDF time variable.
    date : str
        Date of the format YYYY-MM-DD.
    
    Returns
    -------
    float : Time variable value closest to the date.
    """
    t_0 = time_var.units.split(' ')[2]
    t_0 = datetime.datetime.strptime(t_0, '%Y-%m-%d')
    t_1 = datetime.datetime.strptime(date, '%Y-%m-%d')
    d_t = abs((t_1 - t_0).days)
    time_val = (np.abs(time_var[:] - d_t)).argmin()
    return time_val
    
    
def time_var_to_dates(time_var):
    """
    Calculate the dates corresponding to netCDF time variable values.
    
    Parameters
    ----------
    time_var : NetCDF4 Variable object
        NetCDF time variable.
    
    Returns
    -------
    List of str
        List of dates. Format: YYYY-MM-DD.
    """
    dates = [0] * len(time_var[:].shape[0])
    for idx, time_val in enumerate(time_var[:]):
        curr_val = time_val_to_date(time_var, time_val)
        dates[idx] = curr_val
    return dates
    
    