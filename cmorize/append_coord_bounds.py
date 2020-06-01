"""
Python 3.6
append_coord_bounds.py

Calculate & append lat, lon, & time bounds variables to CESM timeseries output files.

Usage
------
python append_coord_bounds.py file.nc

Matt Nicholson
3 April 2020
"""
from __future__ import print_function
import sys
import numpy as np
import logging
from netCDF4 import Dataset
from os.path import isfile, join
from os import listdir, remove
    
    
def calc_lat_lon_bnds(coord_vals, coord_name):
    """
    Calculate a lat or lon bounds array.
    
    Parameters
    -----------
    coord_vals : NumPy ndarray
        NetCDF coordinate values.
    coord_name : str
        Name of the coordinate being processed, i.e., "lat" or "lon".
        
    Return
    -------
    NumPy n x 2 array
        Coordinate bound values.
    """
    name_long = {'lat' : 'latitude', 'lon' : 'longitude'}
    logger.info('Creating {} bounds...'.format(name_long[coord_name]))
    
    num_coords = coord_vals.size
    logger.debug('{} size: {}'.format(coord_name, num_coords))

    coord_bnds = np.zeros((num_coords, 2))     # n x 2 matrix of lat_bnds
    logger.debug('Created zeroed {}_bnds array of size {}'.format(coord_name, coord_bnds.shape))

    d_val = abs(coord_vals[1] - coord_vals[0])
    logger.debug('d_{}: {}'.format(coord_name, d_val))

    curr_bnd = coord_vals[0] - (d_val / 2)
    for idx in range(num_coords):
        coord_bnds[idx][0] = curr_bnd
        curr_bnd += d_val
        coord_bnds[idx][1] = curr_bnd
    return coord_bnds
    
    
def append_lat_lon_bnd(filename):
    """
    Read, create, and write lat_bnds & lon_bnds variables to a netcdf file.
    
    Parameters
    -----------
    filename : str  
        Path of the CESM netCDF file to process.
        
    Returns
    -------
    filename : str
        Path of the processed CESM output file.
    """
    logger.info('Reading {}'.format(filename))
    nc = Dataset(filename, 'r+')
    # --- Create lat_bnds
    lat_bnds = calc_lat_lon_bnds(nc.variables['lat'][:], 'lat')
    logger.info('Finished creating latitude bounds, adding them to netcdf file...')
    try:
        nc.createVariable('lat_bnds', 'float64', ('lat', 'nbnd'))
    except RuntimeError as err_rt:
        logger.error('The following error was caught while trying to create variable: lat_bnds')
        logger.error(err_rt)
        logger.info('Overwriting existing lat_bnds values')
    except Exception as exp:
        logger.error(exp)
        raise
    nc.variables['lat_bnds'][:] = lat_bnds[:, :]
    # --- Create lon_bnds
    lon_bnds = calc_lat_lon_bnds(nc.variables['lon'][:], 'lon')
    logger.info('Finished creating longitude bounds, adding them to netcdf file...')
    try:
        nc.createVariable('lon_bnds', 'float64', ('lon', 'nbnd'))
    except RuntimeError as err_rt:
        logger.error('The following error was caught while trying to create variable: lon_bnds')
        logger.error(err_rt)
        logger.info('Overwriting existing lon_bnds values')
    except Exception as exp:
        logger.exception(exp)
        raise
    nc.variables['lon_bnds'][:, :] = lon_bnds[:, :]
    nc.close()
    logger.info('Finshed! Closing {}\n'.format(filename))
    return filename
    
    
def calc_time_bnds(start_year, end_year):
    """
    Calculate the time bound array. Designed specifically for CESM output, where
    the time variable values fall on the last day of the month.
    
    Parameters
    ----------
    start_year : int
        First year of variable data.
    end_year : int
        Final year of variable data.
    
    Returns
    -------
    numpy ndarray
        2-D array of time_bnd values.
    """
    days_per_month = { 1: 31, 2: 28, 3: 31,  4: 30,  5: 31,  6: 30,
                       7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
                       
    logger.info('Creating time bounds...')
    cum_days = 0
    time_bnd = []
    for year in range(end_year - start_year + 1):
        for curr_month in list(days_per_month.keys()):
            bnd_0 = (days_per_month[curr_month] / 2) + cum_days
            cum_days += days_per_month[curr_month]
            try:
                bnd_1 = (days_per_month[curr_month + 1] / 2) + cum_days
            except:
                # December case. Jan & Dec have 31 days so this should work.
                bnd_1 = (days_per_month[curr_month] / 2) + cum_days
            time_bnd.append([bnd_0, bnd_1])
    time_bnd = np.asarray(time_bnd)
    logger.info('Finished creating time bounds!')
    return time_bnd
    
    
def append_time_bnd(filename):
    """
    Calculate the time_bnd variable and append to a CESM netcdf file.
    
    Parameters
    ----------
    filename : str
        Path of a CESM output file to append a time bnd to.
        
    Returns
    -------
    filename : str
        Path of the processed CESM output file.
    """
    # ADJUST THESE AS NEEDED
    start_year = 1999
    end_year   = 2014
    
    logger.info('Adding time_bnds to {}'.format(filename))
    time_bnds = calc_time_bnds(start_year, end_year)
    nc = Dataset(filename, 'r+')
    try:
        nc.createVariable('time_bnds', 'float64', ('time', 'nbnd'))
    except RuntimeError as err_rt:
        logger.error('The following error was caught while attempting to create time_bnds variable:')
        logger.error(err_rt)
        logger.info('Overwriting existing time_bnds values')
    except Exception as exp:
        logger.exception(exp)
        raise
    nc.variables['time_bnds'][:] = time_bnds[:, :]
    nc.close()
    logger.info('Finished! Closing {}\n'.format(filename))
    return filename
    

if __name__ == '__main__':
    # --- Initialize logger
    LOG_LEVEL = 'debug'

    log_levels = {'debug': logging.DEBUG,
                  'info' : logging.INFO,
                  'warn' : logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL
                  }
                  
    # Remove previous log if it exists as the logging module prefers appending to 
    # previous log files instead of overwriting. Leave commented out to append to log
    if isfile('append_coord_bounds.log'):
        remove('append_coord_bounds.log')
        
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
    
    # --- Find netcdf files
    root_dir = sys.argv[1]
    logger.info('Looking for NetCDF files in {}'.format(root_dir))
    
    nc_files = [join(root_dir, f) for f in listdir(root_dir) if isfile(join(root_dir, f))
                and f.endswith('.nc')]
    logger.info('NetCDF files found: {}'.format(len(nc_files)))
    
    # --- Calculate and append lat & lon bounds
    processed = [append_lat_lon_bnd(nc_file) for nc_file in nc_files]
    
    # --- Calculate and append time bounds
    processed = [append_time_bnd(nc_file) for nc_file in nc_files]
    
    logger.info('Finished! {} files processed'.format(len(processed)))

