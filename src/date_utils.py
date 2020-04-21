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
        Time variable value to convert to date.
    
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
    idx = (np.abs(time_var[:] - d_t)).argmin()
    return time_var[:][idx]
    
    
def time_var_to_dates(time_var):
    """
    Calculate the dates corresponding to netCDF time variable values.
    
    Parameters
    ----------
    time_var : NetCDF4 Variable object
        NetCDF time variable.
    
    Returns
    -------
    Numpy array of str
        Array of dates. Format: YYYY-MM-DD.
    """
    dates = [0] * time_var.shape[0]
    for idx, time_val in enumerate(time_var.values):
        curr_val = time_val_to_date(time_var, time_val)
        dates[idx] = curr_val
    return np.asarray(dates)
    
    
def time_var_to_year_month(time_var):
    """
    Calculate the dates corresponding to netCDF time variable values and return
    them in the format YYYY-MM.
    
    Parameters
    ----------
    time_var : NetCDF4 Variable object
        NetCDF time variable.
    
    Returns
    -------
    List of str
        List of dates. Format: YYYY-MM.
    """
    dates = time_var_to_dates(time_var)
    dates = [d[:7] for d in dates]
    return dates
    
    
def time_var_to_years(time_var):
    """
    Calculate the years represented in the netCDF time variable.
    
     Parameters
    ----------
    time_var : NetCDF4 Variable object
        NetCDF time variable.
    
    Returns
    -------
    List of str
        List of years. Format: YYYY.
    """
    years = [dt.split('-')[0] for dt in time_var_to_year_month(time_var)]
    years = list(set(years))
    return sorted(years)
    
    
def chunk_var_annual(netcdf, var):
    """
    Transform a variable's 3-D data array from months into years.
    
    Parameters
    ----------
    netcdf : Netcdf object
        Netcdf object holding the variable to chunk.
    var : NetcdfVariable object
        Variable to chunk.
        
    Returns
    -------
    List of NumPy ndarrays
        List where each element is a year-chunk of monthly data.
    """
    num_months = netcdf.variables['time'].shape[0]
    num_years = int(num_months / 12)
    if num_months != var.shape[0]:
        raise ValueError('Variable time dimension does not match time variable dimension: {}'.format(var.name))
    chunks = [0] * num_years
    for yr_idx in range(num_years):
        m_0 = yr_idx * 12
        m_1 = m_0 + 12   # m_0 + 11 on paper, but +1 due to numpy slicing.
        chunks[yr_idx] = var.value[m_0:m_1]
    return chunks
    