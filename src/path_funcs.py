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
    
    
def ensemble_lut(ensemble):
    """
    Given the run's ensemble, retrieve information about purturbation,
    wind nudging, and seasonality. 
    
    Parameters
    ----------
    ensemble : str
        Ensemble that produced the model output. Ex: 'r1i1p5f101'
    
    Returns
    -------
    dict : {str, bool, bool}
        Dictionary containing metadata about the model configuration.
        Keys: 
            * run : str, whether the model output is from a base run or 
                    purturbation run.
            * wind_nudging : bool, whether the model included wind nudging.
            * seasonality : bool, SO2 seasonality.
    """
    return getattr(config.ModelConfig, ensemble)
    
    
def get_var_path(ensemble, var_name):
    """
    Contruct the CMORized path of an output variable netCDF file.
    
    Parameters
    ----------
    ensemble : str
        Model ensemble that produced the output. Ex: 'r1i1p5f101'.
    var_name : str
        Name of the output variable corresponding to the file.
        
    Return
    ------
    str
        Absolute path of the variable output file.
        
    Usage
    -----
    get_var_path('r1i1p5f101', 'dryso4')
    """
    prefix = config.DIRS.prefix.format(ensemble)
    suffix = config.DIRS.suffix
    path = os.path.join(config.DIRS.proj_root, config.DIRS.model_output, prefix,
                        var_name, suffix)
    file = [f for f in os.listdir(path) if f.endswith('.nc')]
    if len(file) > 1:
        raise OSError('Multiple files found in {}'.format(path))
    path = os.path.join(path, file[0])
    return path
