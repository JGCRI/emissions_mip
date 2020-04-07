"""
Functions to process variables.

Matt Nicholson
7 April 2020
"""
import numpy as np

import nc_io


def global_mean_mon(nc_dataset, var_name):
    """
    Get the monthly global means of a variable.
    
    Parameters
    ----------
    nc_dataset : NetCDF4 Dataset object
        Dataset holding to variable to average.
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
    var = nc_io.get_var_val(nc_dataset, var_name)
    avg = np.mean(var, axis=(1,2))
    return avg

