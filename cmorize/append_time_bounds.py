"""
Append time bounds variable to all NetCDF files in a given directory.

Usage
------
python append_time_bounds.py path/to/files

Input files
-----------
time_bnds.csv
    Comma-separated time_bnds values.

Matt Nicholson
3 April 2020
"""
from __future__ import print_function
import sys
import numpy as np
import logging
from netCDF4 import Dataset
from os.path import isfile, join
from os import listdir


def add_time_bnds(filename, time_bnds):
    """
    Read, create, and write lat_bnds & lon_bnds variables to a netcdf file
    
    Parameters
    -----------
    filename : str  
        Name of the netCDF file to process.

    time_bnds : NumPy 2D array
        Array containing time_bnds values to add.

    Returns
    -------
    None
    """
    logger.info('Adding time_bnds to {}'.format(filename))
    nc = Dataset(filename, 'r+')
    try:
        nc.createVariable('time_bnds', 'float64', ('time', 'bnds'))
    except RuntimeError as err:
        logger.error('The following error was caught while attempting to create time_bnds variable:')
        logger.error(err)
        logger.info('Overwriting existing time_bnds values')
    nc.variables['time_bnds'][:] = time_bnds[:, :]
    nc.close()
    logger.info('Finished! Closing {}\n'.format(filename))


if __name__ == '__main__':
    # --- Init logger
    LOG_LEVEL = 'debug'

    log_levels = {'debug': logging.DEBUG,
                  'info' : logging.INFO,
                  'warn' : logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL
                  }
                  
    # Remove previous log if it exists as the logging module prefers appending to 
    # previous log files instead of overwriting. Leave commented out to append to log
    # if os.path.isfile('append_coord_bounds.log'):
        # os.remove('append_coord_bounds.log')
        
    log_format = logging.Formatter("%(asctime)s %(levelname)6s: %(message)s", "%Y-%m-%d %H:%M:%S")
    # File handler
    file_handler = logging.FileHandler('append_coord_bounds.log')
    file_handler.setFormatter(log_format)
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    # Configure logger
    logger = logging.getLogger('main')
    logger.setLevel(log_levels[LOG_LEVEL])
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info("Log created!\n")

    # --- Read the time_bnds values from .csv
    time_bnds = np.loadtxt("time_bnds.csv", delimiter=',')
    
    # --- Find & process netcdf files
    root_dir = sys.argv[1]
    logger.info('Looking for NetCDF files in {}'.format(root_dir))
    
    nc_files = [join(root_dir, f) for f in listdir(root_dir) if isfile(join(root_dir, f))
                and f.endswith('.nc')]
    logger.info('NetCDF files found: {}'.format(len(nc_files)))
    [add_time_bnds(nc_file, time_bnds) for nc_file in nc_files]
    logger.info('Finished processing all files!')