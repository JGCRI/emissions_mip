"""
Class to represent a netCDF variable

Matt Nicholson
7 April 2020
"""
import numpy as np

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
        self.name  = var_obj.name
        self.dtype = var_obj.dtype.name
        self.value = var_obj[:]
        self.shape = self.value.shape
        self.attrs = var_obj.ncattrs()
        self.parent_file = None
        self.date_first  = None
        self.date_last   = None
        for attr in self.attrs:
            setattr(self, attr, var_obj.getncattr(attr))
    
    def __repr__(self):
        return "<NetcdfVariable - {}>".format(self.name)