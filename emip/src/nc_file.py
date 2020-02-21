"""
Class to represent a netCEDF file

Matt Nicholson
21 Feb 2020
"""
import netCDF4
import os
import numpy as np

import nc_io
from nc_var import NCVar

class NCFile:
    
    def __init__(self, nc_fname, nc_vars):
        """
        Constructor for an NCFile instance
        
        Parameters
        -----------
        nc_fname : str
            Name & path of the netCDF file to read
        nc_vars : str, list of str
            Names of the netCDF variables to fetch from the file
            
        Attributes
        -----------
        nc_fname : str
            Name of the netCDF file
        nc_path : str
            Path of the netCDF file
        nc_vars : dict of {str : NCVar object}
            Dictionary where a key is the string name of a netCDF variable and 
            the value is the NCVar object corresponding to that variable
        conventions : str
            NetCDF conventions of the file being read
        case : str
            Experiment case pertaining to the netCDF data
        """
        self.nc_fname    = self._parse_fname(nc_fname)
        self.nc_fpath    = nc_fname
        self.nc_vars     = None
        self.conventions = ''
        self.case        = ''
        self._read_nc(nc_fname, nc_vars)
        
    def _parse_fname(self, nc_path):
        """
        Extract the name of the netCDF file from the file's path
        
        Parameters
        -----------
        nc_path : str
            Path of the netCDF file
            
        Return
        -------
        str : name of the netCDF file
        """
        return os.path.basename(nc_path)
    
    def _read_nc(self, nc_path, nc_vars):
        """
        Read a netCDF file and populate instance attributes
        
        Parameters
        -----------
        nc_path : str
            Path of the netCDF file to read
        nc_vars : str, list of str
            Names of variables to extract from the netCDF file
        """
        nc = nc_io.read_nc(nc_path)
        self._parse_meta(nc)
        self._parse_vars(nc, nc_vars)
        
    def _parse_vars(self, nc_file, new_vars):
        """
        Create NCVar object(s) for specified netCDF variable(s) and add them to
        the instance's nc_vars dictionary
        
        Parameters
        -----------
        nc_file : netCDF4.Dataset object
        new_vars : str, list of str
            Names of variables to extract from the netCDF file
        """
        nc_vars = ['lev', 'time', 'date', 'lat', 'lon']
        if not isinstance(new_vars, list):
            nc_vars = default_vars.append(new_vars)
        else:
            nc_vars.extend(new_vars)
        nc_vars = {key: NCVar(nc_file, key, self.nc_fname) for key in nc_vars}
        self.nc_vars = nc_vars
    
    def _parse_meta(self, nc_file):
        try:
            self.conventions = nc_file.Conventions
        except:
            print('Unable to parse Conventions for {}'.format(self.nc_fname))
        try:
            self.case = nc_file.case
        except:
            print('Unable to parse Case for {}'.format(self.nc_fname))
        
    def __repr__(self):
        return "<NCFile object - {}>".format(self.nc_fname)