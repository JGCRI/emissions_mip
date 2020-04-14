"""
Functions to analyze variables.

Matt Nicholson
7 April 2020
"""
import numpy as np


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
        chunks[yr_idx] = var.values[m_0:m_1]
    return chunks
    

def global_mean_monthly(netcdf, var_name):
    """
    Get the monthly global means of a variable for all available months.
    
    Parameters
    ----------
    netcdf : Netcdf object
        Netcdf object holding the variable to average.
    var_name : str
        Variable to average.
    
    Returns
    -------
    NumPy array
        Array of monthly averages.
    
    Notes
    -----
    The variables have the shape (X, Y, Z), where:
        * X = time
        * Y = latitude
        * Z = longitude
    """
    var = netcdf.get_var(var_name)
    avg = np.mean(var.values, axis=(1,2))
    # TODO: Return months too?
    return avg
    

def global_mean_annual(netcdf, var_name):
    """
    Get the annual global means of a variable for all available years.
    
    Parameters
    ----------
    netcdf : Netcdf object
        Netcdf object holding the variable to average.
    var_name : str
        Variable to average.
    
    Returns
    -------
    NumPy array
        Array of annual averages.
    
    Notes
    -----
    The variables have the shape (X, Y, Z), where:
        * X = time
        * Y = latitude
        * Z = longitude
    """
    var = netcdf.get_var(var_name)
    chunks = chunk_var_annual(netcdf, var)
    avgs = [np.mean(var_chunk, axis=(1,2)) for var_chunk in chunks]
    avgs = np.asarray(avgs)
    return avgs
    
    

