"""
Class to represent a netCDF variable

Matt Nicholson
7 April 2020
"""
import numpy as np
import copy

class NetcdfVariable:

    def __init__(self, var_obj):
        """
        Instance constructor. 
        
        Parameters
        ----------
        var_obj : netCDF4 Variable object
            Variable object to pull data from
            
        Attributes
        ----------
        name : str
            Name of the variable.
        parent_file : str
            Name of the file the variable came from.
        parent_source_id : str
            Source ID of the parent NetCDF file.
        parent_institution_id : str
            Institution ID of the parent NetCDF file.
        dtype : str
            Variable dtype.
        value : NumPy array
            Variable values/data.
        shape : tuple of int
            Shape of the variable's data/values.
        attrs : List of str
            List of attributes returned by the netCDF4 Variable object's getncattr()
            function. 
        """
        self.name   = var_obj.name
        self.dtype  = var_obj.dtype.name
        self.values = var_obj[:]
        self.shape  = self.values.shape
        self.attrs  = var_obj.ncattrs()
        self.date_first  = None
        self.date_last   = None
        self.parent_file = None
        self.parent_source_id = None
        self.parent_institution_id = None
        for attr in self.attrs:
            setattr(self, attr, var_obj.getncattr(attr))
        
    
    def __repr__(self):
        return "<NetcdfVariable - {}>".format(self.name)