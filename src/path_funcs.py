"""
Functions to parse paths and such.

Matt Nicholson
8 April 2020
"""
import os
from pathlib import Path

import config


def get_root():
    """
    Get the path of the project's root directory.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    str
        Path of the project's root directory.
    """
    root = str(Path(os.path.abspath(__file__)).parents[1])
    return root
    
    
def get_cwd():
    """
    Get the current working directory. Wrapper for os.getcwd().
    
    Parameters
    ----------
    None
    
    Returns
    -------
    str
        Absolute path of the current working directory.
    """
    return os.getcwd()
    
    
def split_namestring(namestring):
    """
    Split a model output namestring into its institution & forcing component
    components.
    
    Parameters
    ----------
    namestring : str
        Model output namestring. Format: <institution>-<forcing_index>
    
    Returns
    -------
    List of str
        [<institution>, <forcing_index>]
    """
    return namestring.split('-')
    
    
def get_var_path(namestring, var_name):
    """
    Contruct the CMORized path of an output variable netCDF file.
    
    Parameters
    ----------
    namestring : str
        Model output namestring. Format: <institution>-<forcing_index>
    var_name : str
        Name of the output variable corresponding to the file.
        
    Return
    ------
    str
        Absolute path of the variable output file.
        
    Usage
    -----
    get_var_path('columbia-103', 'dryso4')
    """
    inst, forcing_idx = split_namestring(namestring)
    prefix = config.DIRS.prefix.format(inst, forcing_idx)
    suffix = config.DIRS.suffix
    path = os.path.join(config.DIRS.proj_root, config.DIRS.model_output, prefix,
                        var_name, suffix)
    file = [f for f in os.listdir(path) if f.endswith('.nc')]
    if len(file) > 1:
        raise OSError('Multiple files found in {}'.format(path))
    path = os.path.join(path, file[0])
    return path
