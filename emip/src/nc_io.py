"""
Functions to handle netCDF I/O

Matt Nicholson
21 Feb 2020
"""
import netCDF4

def ncdump(nc_fid, verb=True):
    """
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
        
    Credit: Chris Slocum, 22 Jul 2014
    Adapted to Python 3 by Matt Nicholson
    """
    def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print("\t\ttype: {}".format(repr(nc_fid.variables[key].dtype)))
            for ncattr in nc_fid.variables[key].ncattrs():
                print('\t\t{}: {}'.format(ncattr,
                      repr(nc_fid.variables[key].getncattr(ncattr))))
        except KeyError:
            print("\t\tWARNING: {} does not contain variable attributes".format(key))

    # NetCDF global attributes
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print("NetCDF Global Attributes:")
        for nc_attr in nc_attrs:
            print("\t{}: {}".format(nc_attr, repr(nc_fid.getncattr(nc_attr))))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
    # Dimension shape information.
    if verb:
        print("NetCDF dimension information:")
        for dim in nc_dims:
            print("\tName: {}".format(dim)) 
            print("\t\tsize: {}".format(len(nc_fid.dimensions[dim])))
            print_ncattr(dim)
    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print("NetCDF variable information:")
        for var in nc_vars:
            if var not in nc_dims:
                print("\tName: {}".format(var))
                print("\t\tdimensions: {}".format(nc_fid.variables[var].dimensions))
                print("\t\tsize: {}".format(nc_fid.variables[var].size))
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars


def read_nc(nc_path):
    """
    Read a netCDF file
    
    Parameters
    -----------
    nc_path : str
        Path of the netCDF file to read
    """
    nc = netCDF4.Dataset(nc_path, 'r')
    return nc
    