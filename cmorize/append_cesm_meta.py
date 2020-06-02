"""
Python 3.6
append_cesm_meta.py

Add CESM netcdf metadata to variable timeseries files in preparation to CMOR-ize.

Matt Nicholson
23 May 2020
"""
from __future__ import print_function
import sys
import numpy as np
import logging
from netCDF4 import Dataset
from os.path import isfile, join
from os import listdir, remove


def append_lat_meta(nc_handler):
    """
    Append latitude variable metadata to a netcdf file handler.
    
    Parameters
    ----------
    nc_handler : netCDF4._netCDF4.Dataset
        NetCDF4 Dataset object representing the CESM output variable file.
    
    Returns
    -------
    netCDF4._netCDF4.Dataset
        NetCDF4 Dataset object with latitude variable metadata appended.
    """
    logger.info('Appending latitude variable metadata')
    nc_handler.variables['lat'].axis = 'Y'
    logger.debug('    lat:axis = "Y"')
    nc_handler.variables['lat'].standard_name = 'latitude'
    logger.debug('    lat:standard_name = "latitude"')
    # Bounds attribute already present, included for completeness.
    #nc_handler.variables['lat'].bounds = 'lat_bnds'
    #logger.debug('    lat:bounds = "lat_bnds"')
    return nc_handler
    
    
def append_lon_meta(nc_handler):
    """
    Append longitude variable metadata to a netcdf file handler.
    
    Parameters
    ----------
    nc_handler : netCDF4._netCDF4.Dataset
        NetCDF4 Dataset object representing the CESM output variable file.
    
    Returns
    -------
    netCDF4._netCDF4.Dataset
        NetCDF4 Dataset object with longitude variable metadata appended.
    """
    logger.info('Appending longitude variable metadata')
    nc_handler.variables['lon'].axis = 'X'
    logger.debug('    lon:axis = "X"')
    nc_handler.variables['lon'].standard_name = 'longitude'
    logger.debug('    lon:standard_name = "longitude"')
    nc_handler.variables['lon'].bounds = 'lon_bnds'
    logger.debug('    lon:bounds = "lon_bnds"')
    return nc_handler 


def append_var_meta(filename):
    """
    Append missing variable metadata to a CESM output file.
    
    Parameters
    -----------
    filename : str  
        Path of a netCDF file to process.
        
    Returns
    -------
    filename : str
        Path of the processed CESM file.
    """
    logger.info('*** Reading {}'.format(filename))
    nc = Dataset(filename, 'r+')
    # Append lat meta
    nc = append_lat_meta(nc)
    # Append lon meta
    nc = append_lon_meta(nc)
    logger.info('Finished processing {}. Closing file.'.format(filename))
    nc.close()
    return filename
    

if __name__ == '__main__':
    # Initialize logger.
    LOG_LEVEL = 'debug'

    log_levels = {'debug': logging.DEBUG,
                  'info' : logging.INFO,
                  'warn' : logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL
                  }
                  
    # Remove previous log if it exists as the logging module prefers appending to 
    # previous log files instead of overwriting. Leave commented out to append to log.
    if isfile('append_cesm_meta.log'):
        remove('append_cesm_meta.log')
        
    log_format = logging.Formatter("%(asctime)s %(levelname)6s: %(message)s", "%Y-%m-%d %H:%M:%S")
    # File handler.
    file_handler = logging.FileHandler('append_cesm_meta.log')
    file_handler.setFormatter(log_format)
    # Console handler.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    # Configure logger.
    logger = logging.getLogger('main')
    logger.setLevel(log_levels[LOG_LEVEL])
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info("Log created!\n")
    
    # Find netcdf files.
    root_dir = sys.argv[1]
    logger.info('Looking for NetCDF files in {}'.format(root_dir))
    
    nc_files = [join(root_dir, f) for f in listdir(root_dir) if isfile(join(root_dir, f))
                and f.endswith('.nc')]
    logger.info('NetCDF files found: {}'.format(len(nc_files)))
    
    # Pass each file to append_var_meta().
    nc_files = [append_var_meta(nc_file) for nc_file in nc_files]
    logger.info('Finished! {} files processed'.format(len(nc_files)))
    