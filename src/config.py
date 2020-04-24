"""
This file implements simple configuration classes for use throughout the project.
It also congfigures the global logging object.

Matt Nicholson
8 April 2020
"""
import os
import logging


class ModelConfig:
    """
    Class to represent a single model configuration, as outlined in the table
    below.

                         GISS Model Output Description
    ***********************************************************************
    *  Archive |  Ensemble  |  Base/Perturb. | Wind Nudging | Seasonality *
    * =========|============|================|==============|=============*
    * BNW1999  | r1i1p5f101 | base           | no           | yes         *
    * ---------|------------|----------------|--------------|-------------*
    * PWN1999  | r1i1p5f102 | perturbation   | no           | no          *
    * ---------|------------|----------------|--------------|-------------*
    * PW1999   | r1i1p5f103 | perturbation   | yes          | no          *
    * ---------|------------|----------------|--------------|-------------*
    * BW1999   | r1i1p5f104 | base           | yes          | yes         *
    ***********************************************************************
    """
    r1i1p5f101 = {'run' : 'base', 'wind_nudging' : False, 'seasonality' : True}
    r1i1p5f102 = {'run' : 'perturb', 'wind_nudging' : False, 'seasonality' : False}
    r1i1p5f103 = {'run' : 'perturb', 'wind_nudging' : True, 'seasonality' : False}
    r1i1p5f104 = {'run' : 'base', 'wind_nudging' : True, 'seasonality' : True}
    

class DIRS:
    """
    Class to hold project directory information. All paths are formatted for 
    the directory structure on the pic HPC cluster.
    
    Attributes
    ----------
    proj_root : str
        Absolute path of the project's root directory.
    model_output : str
        Absolute path of the directory holding gridded model output files.
    prefix : str
        'Prefix' of the directory holding the model output variable sub-directories. 
    suffix : str
        'Suffix' of the directory holding the gridded variable output file.
        
    """
    proj_root = '/pic/projects/GCAM/mnichol/emip'
    model_output = os.path.join(proj_root, 'model-output')
    prefix = 'AerChemMIP/NASA-GISS/GISS-E2-1-G/piClim-SO2/{0}/AERmon'
    suffix = 'gn/v20191120'
    
    
def config_log(log_name, log_level):
    """
    Configure a global logging object.
    
    Parameters
    ----------
    log_name : str
        Name of the log and log file. 
    log_level : str
        Logging level. 
        Valid: 'debug', 'info', 'warning', 'error', 'critical'.
        
    Returns
    -------
    logging.Logger object
    """
    def nuke_logs(log_dir, target=None):
        """
        Remove any existing logs from the logs/ subdirectory
        
        Parameters
        -----------
        log_dir : str
            Path to the log directory
        target : str, optional
            Target log file to delete. If not given, all log files are deleted.
            Default is 'None'. 
        """
        if (target):
            if (not target.endswith('.log')):
                target = target + '.log'
            files = [target]
        else:
            files = [f for f in os.listdir(log_dir) if f.endswith(".log")]
        for f in files:
            try:
                os.remove(os.path.join(log_dir, f))
            except:
                pass
    # ---------------            
    log_levels = {'debug': logging.DEBUG,
                  'info' : logging.INFO,
                  'warn' : logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL
                  }
    
    nuke_logs(log_dir, target=log_name)
    
    if (not os.path.isdir(log_dir)):
        os.mkdir(log_dir)
    
    if (not log_name.endswith('.log')):
        f_name = '{}.log'.format(log_name)
    log_path = os.path.join(log_dir, f_name)
    
    log_format = logging.Formatter("%(asctime)s %(levelname)6s: %(message)s", "%Y-%m-%d %H:%M:%S")
    
    handler = logging.FileHandler(log_path)
    handler.setFormatter(log_format)
        
    logger = logging.getLogger(log_name)
    logger.setLevel(log_levels[level])
    logger.addHandler(handler)
    logger.info("Log created!\n")
    
    return logger