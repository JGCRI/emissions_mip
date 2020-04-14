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
    prefix_colum : str
        'Prefix' of the directory holding the model output variable sub-directories
        for output from collaborators at Columbia University. 
    suffix_colum : str
        'Suffix' of the directory holding the gridded variable output file for
        output from collaborators at Columbia University.
    prefix_nasa : str
        Not yet implemented!
    suffix_nasa : str
        Not yet implemented!
    prefix_pnnl : str
        Not yet implemented!
    suffix_pnnl : str
        Not yet implemented!
    """
    proj_root = '/pic/projects/GCAM/mnichol/emip'
    model_output = os.path.join(proj_root, 'model-output')
    prefix_colum = ('columbia/gpfsm/dnb53/projects/p117/pub/CMIP6/AerChemMIP/NASA-GISS'
                    'GISS-E2-1-G/piClim-SO2/r1i1p5f103/AERmon')
    suffix_colum = 'gn/v20191120'
    
    #TODO:
    #   * Add NASA-GISS path prefix & suffix
    #   * Add PNNL path prefix & suffix (once CMOR-ized)