"""
Calculate & append lat & lon bounds variables to a netCDF file

Usage
------
python append_coord_bounds.py file.nc

Matt Nicholson
3 April 2020
"""
from __future__ import print_function
# import os
import sys
import numpy as np
import logging
from netCDF4 import Dataset
from os.path import isfile, join
from os import listdir
    
    
def create_bounds(coord_vals, coord_name):
    """
    Create a bounds variable for a given coordinate
    
    Parameters
    -----------
    coord_vals : NumPy ndarray
        NetCDF coordinate values
    coord_name : str
        Name of the coordinate being processed, i.e., "lat" or "lon"
        
    Return
    -------
    NumPy n x 2 array
        Coordinate bound values
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
    
    
def process_file(filename):
    """
    Read, create, and write lat_bnds & lon_bnds variables to a netcdf file
    
    Parameters
    -----------
    filename : str  
        Name of the netCDF file to process
    """
    logger.info('Reading {}'.format(filename))
    nc = Dataset(filename, 'r+')

    # --- Create lat_bnds
    lat_bnds = create_bounds(nc.variables['lat'][:], 'lat')
    logger.info('Finished creating latitude bounds, adding them to netcdf file...')
    try:
        nc.createVariable('lat_bnds', 'float64', ('lat', 'nbnd'))
    except RuntimeError as err:
        logger.error('The following error was caught while trying to create variable: lat_bnds')
        logger.error(err)
        logger.info('Overwriting existing lat_bnds values')
    nc.variables['lat_bnds'][:] = lat_bnds[:, :]

    # --- Create lon_bnds
    lon_bnds = create_bounds(nc.variables['lon'][:], 'lon')
    logger.info('Finished creating longitude bounds, adding them to netcdf file...')
    try:
        nc.createVariable('lon_bnds', 'float64', ('lon', 'nbnd'))
    except RuntimeError as err:
        logger.error('The following error was caught while trying to create variable: lon_bnds')
        logger.error(err)
        logger.info('Overwriting existing lon_bnds values')
    nc.variables['lon_bnds'][:, :] = lon_bnds[:, :]
    nc.close()
    logger.info('Finshed! Closing {}\n'.format(filename))


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
    
    # --- Find netcdf files and process them
    root_dir = sys.argv[1]
    logger.info('Looking for NetCDF files in {}'.format(root_dir))
    
    nc_files = [join(root_dir, f) for f in listdir(root_dir) if isfile(join(root_dir, f))
                and f.endswith('.nc')]
    logger.info('NetCDF files found: {}'.format(len(nc_files)))
    map(process_file, nc_files)
    logger.info('Finished processing all files!')

