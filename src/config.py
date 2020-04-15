"""
This file implements simple configuration classes for use throughout the project.

Matt Nicholson
8 April 2020
"""
import os

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
        
    Notes
    -----
    * netCDF model output variant labels 
        * Last 3 digits = forcing index?
        * NASA E6TmatrixF40EMIP_BNW1999 --> r1i1p5f101
        * NASA E6TmatrixF40EMIP_PNW1999 --> r1i1p5f102
        * Columbia E6TmatrixF40EMIP_PW1999 --> r1i1p5f103
        * Columbia E6TmatrixF40EMIP_BW1999 --> r1i1p5f104
    """
    proj_root = '/pic/projects/GCAM/mnichol/emip'
    model_output = os.path.join(proj_root, 'model-output')
    prefix = ('{0}/gpfsm/dnb53/projects/p117/pub/CMIP6/AerChemMIP/NASA-GISS'
                    'GISS-E2-1-G/piClim-SO2/r1i1p5f{1}/AERmon')
    suffix = 'gn/v20191120'
    
    #TODO:
    #   * Add NASA-GISS path prefix & suffix
    #   * Add PNNL path prefix & suffix (once CMOR-ized)