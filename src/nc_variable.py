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
        """
        self.name  = var_obj.name
        self.value = var_obj[:]
        self.shape = self.value.shape
        self.attrs = var_obj.ncattrs()
        for attr in self.attrs:
            setattr(self, attr, var_obj.getncattr(attr))
    
    def __repr__(self):
        return "<NetcdfVariable - {}>".format(self.name)