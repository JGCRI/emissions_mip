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
    root = str(Path(os.path.abspath(__file__)).parents[2])
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
    
    
def get_var_path(inst, var_name, forcing_idx):
    """
    Contruct the CMORized path of an output variable netCDF file.
    
    Parameters
    ----------
    inst : str
        Institution that produced the model output. Corresponds to the directory
        to start searching in. Ex: 'nasa', 'pnnl', 'colum' or 'columbia'.
    var_name : str
        Name of the output variable corresponding to the file.
    forcing_idx : str or int
        Forcing index of the model. Ex: 103.
        
    Return
    ------
    str
        Absolute path of the variable output file.
        
    Usage
    -----
    get_var_path('columbia', 'dryso4', 103)
    """
    prefix = getattr(config.DIRS, 'prefix_{}'.format(inst)).format(inst, forcing_idx)
    suffix = getattr(config.DIRS, 'suffix_{}'.format(inst))
    path = os.path.join(config.DIRS.proj_root, config.DIRS.model_output, prefix,
                        var_name, suffix)
    file = [f for f in os.listdir(path) if f.endswith('.nc')]
    if len(file) > 1:
        raise OSError('Multiple files found in {}'.format(path))
    path = os.path.join(path, file[0])
    return path
