"""
Wrappers for NetCDF4 Variable class functions.

Matt Nicholson
7 April 2020
"""


def get_attributes(nc_var):
    """
    Retrieve the attributes for a netCDF variable. 
    Wrapper for netCDF4.Variable.ncattrs().
    
    Parameters
    ----------
    nc_var : NetCDF4 Variable object
        Variable to retrieve attributes from.
    
    Returns
    -------
    List of str
        The variable's attributes.
    """
    attrs = nc_var.ncattrs()
    return attrs
    

def get_attr(nc_var, attr):
    """
    Retrieve a netCDF variable attribute.
    Use if you need to set a netCDF attribute with the same name as one of
    the reserved python attributes.
    Wrapper for netCDF4.Variable.getncattr().
    
    Parameters
    ----------
    nc_var : NetCDF4 Variable object
        Variable to retrieve attributes from.
    attr : str
        Name of the attribute to retrieve.
        
    Returns
    -------
    str : NetCDF attribute
    
    Raises
    ------
    AttributeError
        If the attribute is not found within the variable.
    """
    try:
        return nc_var.getncattr(attr)
    except AttributeError:
        raise AttributeError('Attribute not found: {}'.format(attr))
    
    
def get_group(nc_var):
    """
    Return the group that the variable is a member of.
    Wrapper for netCDF4.Variable.group()
    
    Parameters
    ----------
    nc_var : NetCDF4 Variable object
        Variable to retrieve attributes from.
    
    Returns
    -------
    List of str
        The variable's attributes.
    """
    attrs = nc_var.ncattrs()
    return attrs