"""
Class to represent a netCDF file.

Matt Nicholson
21 Feb 2020
"""
import netCDF4
import os
import numpy as np

import nc_io
import nc_variable

class Netcdf:
    
    def __init__(self, nc_fname, nc_vars=None):
        """
        Constructor for an NCFile instance
        
        Parameters
        -----------
        nc_fname : str
            Name of the netCDF file to read
        nc_vars : str, list of str, optional.
            Subset of variables to read from the netCDF file. If not given,
            all variables will be read. Default is to read all variables.
            
        Attributes
        -----------
        filename : str
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
        self.filename      = self._parse_fname(nc_fname)
        self.variables     = {}
        nc = self._read_nc(nc_fname, nc_vars)
        self._parse_vars(nc, nc_vars)
        nc.close()
        
    def ncattrs(self):
        """
        Return a list of object attributes.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        List of str
        """
        attrs = list(self.__dict__.keys())
        return attrs
        
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
        
    def _parse_vars(self, nc_dataset, nc_vars):
        """
        Create NetcdfVariable instances for variables in the file.
        
        Parameters
        ----------
        nc_dataset : netCDF4 Dataset object
            netCDF4 to extract data from.
        nc_vars : str or list of str
            Subset of variables to extract from the file. If 'None', all variables
            in the file will be read.
        """
        if isinstance(nc_vars, str):
            nc_vars = [nc_vars]
        elif nc_vars == None:
            nc_vars = list(nc_dataset.variables.keys())
        for var in nc_vars:
            var_obj = nc_dataset.variables[var]
            new_var = nc_variable.NetcdfVariable(var_obj)
            self.variables[var] = new_var
    
    def _read_nc(self, nc_file, nc_var=None):
        """
        Read a netCDF file.
        
        Parameters
        -----------
        nc_file : str
            Name of the netCDF file to read.
        nc_vars : str, list of str, optional.
            Names of variables to extract from the netCDF file. If not given,
            all variables will be read. Default is to read all variables.
        
        Return
        ------
        netCDF4 Dataset object
        """
        nc = netCDF4.Dataset(nc_file, 'r')
        attrs = nc.ncattrs()
        self.attrs = attrs
        for attr in attrs:
            setattr(self, attr, nc.getncattr(attr))
        return nc
        
    def __repr__(self):
        return "<Netcdf object - {}>".format(self.filename)