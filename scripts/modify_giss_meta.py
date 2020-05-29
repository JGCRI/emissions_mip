"""
Python 3.6
modify_giss_meta.py

A simple script to modify the netcdf metadata for GISS CESM output for the intital 
phase of the Emissions-MIP project.

This script assumes the directory tree holding the GISS output files follows
the CMIP6 BADC directory structure.

Usage
-----
$ python modify_giss_meta.py /path/to/activity/dir
  * "Activity dir" is the directory containing the CMIP6 activity sub-directory.
    In this case, it's the parent directory of AerChemMIP/,
    which is /home/nich980/emip/input/GISS-EMIP.

Example directory structure
----------------------------
.../AerChemMIP/NASA-GISS
    |- GISS-base
    |   |- season-so2
    |   |   |- r1i1p5f101
    |   |       |- AERmon
    |   |           |- var1
    |   |           |   |- gn
    |   |           |       |- v20191120
    |   |           |           |- var1_AERmon_GISS-base_season-so2_r1i1p5f101_gn_200001-201412.nc
    |   |           |- var2
    |   |               |- gn
    |   |                   |- v20191120
    |   |                       |- var2_AERmon_GISS-base_season-so2_r1i1p5f101_gn_200001-201412.nc
    |   |   
    |   |- reference
    |       |- r1i1p5f102
    |           |- AERmon
    |               |- var1
    |               |   |- gn
    |               |       |- v20191120
    |               |           |- var1_AERmon_GISS-base_reference_r1i1p5f102_gn_200001-201412.nc
    |               |- var2
    |                   |- gn
    |                       |- v20191120
    |                           |- var2_AERmon_GISS-base_reference_r1i1p5f102_gn_200001-201412.nc
    |
    |- GISS-nudge
        |- reference
        |    |- r1i1p5f103
        |       |- AERmon
        |           |- var1
        |           |   |- gn
        |           |       |- v20191120
        |           |           |- var1_AERmon_GISS-nudge_referencer1i1p5f103_gn_200001-201412.nc
        |           |- var2
        |               |- gn
        |                   |- v20191120
        |                       |- var2_AERmon_GISS-nudge_reference_r1i1p5f103_gn_200001-201412.nc
        |    
        |- season-so2
            |- r1i1p5f104
                |- AERmon
                    |- var1
                    |   |- gn
                    |       |- v20191120
                    |           |- var1_AERmon_GISS-nudge_season-so2_r1i1p5f104_gn_200001-201412.nc
                    |- var2
                        |- gn
                            |- v20191120
                                |- var2_AERmon_GISS-nudge_season-so2_r1i1p5f104_gn_200001-201412.nc

Output configuration
--------------------
*********************************************************************************************************************
*   Run   |  Archive   | Base/Perturb. | Wind Nudging | SO2 Seasonality | Modified GISS Model | Modified Experiment *
* ========|============|===============|==============|=================|=====================|=====================*
* BNW1999 | r1i1p5f101 |     base      |     no       |      yes        |     GISS-E2-1-G     |     season-SO2      *
* --------|------------|---------------|--------------|-----------------|---------------------|---------------------*
* PNW1999 | r1i1p5f102 |  perturbation |     no       |      no         |     GISS-E2-1-G     |     reference       *
* --------|------------|---------------|--------------|-----------------|---------------------|---------------------*
* PW1999  | r1i1p5f103 |  perturbation |     yes      |      no         |  GISS-E2-1-G-nudge  |     reference       *
* --------|------------|---------------|--------------|-----------------|---------------------|---------------------*
* BW1999  | r1i1p5f104 |     base      |     yes      |      yes        |  GISS-E2-1-G-nudge  |     season-SO2      *
*********************************************************************************************************************

Matt Nicholson
27 April 2020
"""
from __future__ import print_function
from netCDF4 import Dataset
from os.path import join, split
from os import listdir, rename
import sys

class ModelConfig:
    """
    Simple class to represent an EMIP model configuration.
    
    Instance Attributes
    -------------------
    * archive : str
        Model archive string.
    * model_name : str
        Model EMIP name.
    * experiment : str
        Model EMIP experiment.
    """
    
    def __init__(self, archive, model_name, experiment):
        self.archive    = archive
        self.model_name = model_name
        self.experiment = experiment
        
    def __repr__(self):
        return "<EMIP ModelConfig {} {} {}>".format(self.archive, self.model_name, self.experiment)
        

def update_fname(curr_fname, model_config, rename_file=True):
    """
    Replace a filename's model/dataset and experiment sub-strings.
    Maintains correct CMIP6 filename format.
    
    Parameters
    ----------
    curr_fname : str
        Absolute path of a model output file.
    model_config : ModelConfig object
        ModelConfig object corresponding to the output file being renamed. 
    rename_file : bool
        Whether or not to rename the file. Default is True, meaning the filename
        modification will be applied to the file. If False, the updated filename
        string is returned without modifying the actual filename.
        
    Returns
    -------
    str : Absolute path of the file, with updated filename.
    """
    abs_path, old_fname = split(curr_fname)
    new_fname = old_fname.replace('piClim-SO2', model_config.experiment)
    new_fname = new_fname.replace('GISS-E2-1-G', model_config.model_name)
    new_fname = join(abs_path, new_fname)
    if rename_file:
        print('{} -> {}'.format(curr_fname, new_fname))
        rename(curr_fname, new_fname)
    return new_fname
    
    
def update_nc_attrs(nc_fname, model_config):
    """
    Add EMIP-specific global attributes to a GISS CESM output file.
    
    Parameters
    ----------
    nc_fname : str
        Absolute path of a GISS output file.
    model_config : ModelConfig object
        ModelConfig object corresponding to the output file being processed. 
        
    Returns
    -------
    str : Absolute path of the modified GISS output file.
    """
    print('Reading {}...'.format(nc_fname))
    # Open netcdf in 'append' mode.
    # WARNING: 'w' mode will OVERWRITE THE ENTIRE FILE.
    nc = Dataset(nc_fname, 'r+')
    # --- Add 'emip_experiment' attribute ---
    print('Adding "emip_experiment" attribute. Value: {}'.format(model_config.experiment))
    nc.emip_experiment = model_config.experiment
    # --- Add 'emip_model' attribute ---
    print('Adding "emip_model" attribute. Value: {}'.format(model_config.model_name))
    nc.emip_model = model_config.model_name
    print('Closing {}...\n'.format(nc_fname))
    nc.close()
    return nc_fname
    

def get_var_paths(archive_path, mip):
    """
    Get the absolute paths of output variable files.
    
    Parameters
    ----------
    archive_path : str
        Path of a GISS CESM model output archive directory.
    mip : str
        MIP that the variables belong to.
        
    Returns
    -------
    list of str : list of variable output file absolute paths.
    """
    suffix = join('gn', 'v20191120')
    var_dirs = [join(archive_path, mip, x, suffix) for x in listdir(join(archive_path, mip))]
    var_files = [join(var, listdir(var)[0]) for var in var_dirs]
    return var_files
    

if __name__ == '__main__':
    ROOT_DIR = sys.argv[1]
    
    # Set this variable to the name of the MIP that the variables being processed
    # belong to (e.g., AERmon, Amon, etc)
    mip = 'Amon'
    
    # Archive, emip model name, emip experiment name.
    model_configs = [['r1i1p5f101', 'GISS-base', 'season-so2'],
                     ['r1i1p5f102', 'GISS-base', 'reference'],
                     ['r1i1p5f103', 'GISS-nudge', 'reference'],
                     ['r1i1p5f104', 'GISS-nudge', 'season-so2']]
                     
    config_ojbs = [ModelConfig(x[0], x[1], x[2]) for x in model_configs]
    
    num_files = 0
    for model_config in config_ojbs:
        print('Processing model config: {}'.format(model_config.archive))
        base_path = join(ROOT_DIR, model_config.model_name, model_config.experiment, model_config.archive)
        # Get a list of the absolute paths of directories within /base_path/archive_path/AERmon.
        # These subdirectories are named after the variables whose output files they contain.
        var_files = get_var_paths(base_path, mip)
        updated_files = [update_fname(var, model_config, rename_file=True) for var in var_files]
        updated_files = [update_nc_attrs(var, model_config) for var in updated_files]
        print('*'*60)
        num_files += len(updated_files)
    print('Finished! {} files processed.'.format(num_files))
        
        
        
    