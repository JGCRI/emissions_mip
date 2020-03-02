"""
Class to represent a single variable from a netCDF file

Matt Nicholson
21 Feb 2020
"""
import numpy as np

class NCVar:
    
    def __init__(self, nc_file, var_name, parent_nc):
        """
        Constructor for an NCVar instance
        
        Parameters
        -----------
        nc_file : netCDF4.Dataset
            A netCDF4 dateset object
        var_name : str
            Name of the variable represented by the instance
        parent_nc : str 
            Name of the parent netCDF file from which the variable is being retrieved
            
        Instance Attributes
        --------------------
        name : str
            Name of the variable. Ex: 'so4_c2'
        shape : tuple of int
            Shape of the variable
        units : str
            Variable units
        long_name : str
            Variable long name. Ex: 'so4_c2 in cloud water'
        data : NumPy nd array
            Variable data
        """
        self.parent       = parent_nc
        self.name         = var_name
        self.shape        = nc_file.variables[var_name].shape
        self.units        = nc_file.variables[var_name].units
        self.long_name    = nc_file.variables[var_name].long_name
        self.data         = np.asarray(nc_file.variables[var_name][:])
        
    def get_name(self):
        return self.name
    
    def get_shape(self):
        return self.shape
        
    def get_units(self):
        return self.units
    
    def get_name_long(self):
        return self.long_name
    
    def get_data(self):
        return self.data
    
    def get_parent(self):
        return parent
        
    def __repr__(self):
        return "<NCVar object - {}-{}>".format(self.parent, self.name)