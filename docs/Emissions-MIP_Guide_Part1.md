# Emissions-MIP Guide
This guide is a comprehensive list of instructions on how to perform various data processing tasks for the Emissions-MIP project. There are three components to this process: CMORizing model output data (if needed) using the e3sm_to_cmip tool, processing and extracting model data using ESMValTool, and plotting the results from ESMValTool using R.

**Note:** As of the writing of this guide, there already exists a working copy of the CMOR converter (e3sm_to_cmip) and ESMValTool on a shared directory on PIC (/pic/projects/GCAM/Emissions-MIP). So the instructions below for *setting up* these tools won’t be applicable unless you want to setup them up in your own directory. (For ESMValTool however, some of the setup steps will be required in either case. These include installing the configuration file, making the required changes to the different configuration files, and the new shapefile changes.)

Requirements:
- GitHub account
- Access to PIC
- Download [Panoply](https://www.giss.nasa.gov/tools/panoply/) (NetCDF file viewer)

## Setting up and running e3sm_to_cmip
The e3sm_to_cmip tool converts E3SM (and CESM) model output variables to the CMIP standard format. Visit the [GitHub page](https://github.com/E3SM-Project/e3sm_to_cmip) for detailed documentation.

From your home directory on PIC, create a new directory called e3sm_to_cmip and move to it:\
`mkdir e3sm_to_cmip`\
`cd e3sm_to_cmip`

Acquire the following mapping and configuration files and place them in the current directory (if unsure where to get them, let us know!):
- *map_ne30np4_to_cmip6_180x360_aave.20181001.nc*
- *vrt_remap_plev19.nc*
- *cesm_user_config_draft.json*
- *e3sm_user_config_picontrol.json*

Create the following directories (they will hold processed data):\
`mkdir native_add_bounds native_grid regrid_timeseries`

Clone a copy of the CMIP6 Controlled Vocabulary tables:\
`git clone https://github.com/PCMDI/cmip6-cmor-tables.git`

Replace the file */qfs/people/[USER]/e3sm_to_cmip/cmip6-cmor-tables/Tables/CMIP6_CV.json* with the one provided. This file lists the experiment metadata recognized by e3sm_to_cmip. The new file contains experiments specific to Emissions-MIP (e.g. nudge-ref, nudge-BC-no-seas, etc.). **When new experiments become available, add them to the file**.

Make the following changes to the file */qfs/people/[USER]/e3sm_to_cmip/cmip6-cmor-tables/Tables/CMIP6_formula_terms.json*:
- For the variables *a* and *b*, add a “bounds” attribute called “a_bnds” and” b_bnds”, respectively.
- For the *ps* variable, change the “standard_name” to “surface_air_pressure”.

Set up conda environment:\
`module load python/miniconda3.8`\
`source /share/apps/python/miniconda3.8/etc/profile.d/conda.sh`\
`conda create --name cmorize python=3.8`

Activate the newly made conda environment:\
`conda activate cmorize`

Install required packages to conda environment:\
`conda install -c conda-forge nco`\
`conda install -c conda-forge cmor`\
`conda install -c conda-forge tqdm`\
`conda install -c anaconda pyyaml`\
`conda install -c conda-forge xarray dask netCDF4 bottleneck`\
`conda install -c conda-forge scipy`\
`conda install -c conda-forge cdutil`\
`conda install -c conda-forge cdms2`\
`conda install -c conda-forge cwltool nodejs`

Clone the forked e3sm_to_cmip repository from the JGCRI/e3sm_to_cmip GitHub page:\
`git clone https://github.com/JGCRI/e3sm_to_cmip.git`

Change directory and initialize e3sm_to_cmip package:\
`cd e3sm_to_cmip`\
`python setup.py install`

Create a temp directory for holding files processed during the workflow:\
`mkdir temp`

Acquire *config_e3sm.yaml* and *config_cesm.yaml* and place them in the current directory. These files are used to specify various parameters for executing the e3sm_to_cmip workflow via cwltool. Make sure to change all file paths to include your username.

The steps above only need to be done once. The steps below are done every time on PIC.

Loading the environment:\
`module load python/miniconda3.8`\
`source /share/apps/python/miniconda3.8/etc/profile.d/conda.sh`\
`conda activate cmorize`\
`export TMPDIR=/qfs/people/[USER]/e3sm_to_cmip/e3sm_to_cmip/temp`

**Note**: After modifying an existing CMOR handler or adding a new one, always run the setup script:\
`python setup.py install`

Before CMORizing E3SM or CESM model files:
- Update config_e3sm.yaml or config_cesm.yaml with the appropriate data path and variable lists. **Note**: Do not leave either lists empty. If only running 2D variables, just leave the 3D variable Q/hus as a placeholder.
- Update *e3sm_user_config_picontrol.json* with the appropriate experiment name (or *cesm_user_config_draft.json* for the CESM model). These are the experiments we have run so far:

| Phase 1a                 | Phase 1b                        |
|--------------------------|---------------------------------|
|     nudge-ref            |     nudge-shp-10p-red           |
|     nudge-BC-no-seas     |     nudge-shp-20p-red           |
|     nudge-high-SO4       |     nudge-shp-80p-red           |
|     nudge-no-SO4         |     nudge-shp-atl-shift         |
|     nudge-SO2-at-hgt     |     nudge-shp-ind-shift         |
|     nudge-SO2-no-seas    |     nudge-ref-1950              |
|                          |     nudge-shp-10p-red-1950      |
|                          |     nudge-shp-20p-red-1950      |
|                          |     nudge-shp-atl-shift-1950    |
|                          |     nudge-shp-ind-shift-1950    |

Run the E3SM converter using cwltool (automated workflow):\
`cwltool scripts/cwl_workflows/atm-unified/atm-unified.cwl config_e3sm.yaml`

Or run the CESM converter as follows:\
`cwltool scripts/cwl_workflows/atm-cesm/atm-cesm.cwl config_cesm.yaml`

The final CMORized output files will be in the *CMIP6* directory.

It’s good practice to clear the temp directory once in a while to make space. The following command will permanently delete all folders and files in the temp directory, so be careful how you use it!\
`rm -rf /qfs/people/[USER]/e3sm_to_cmip/e3sm_to_cmip/temp/*`

The cwltool commands work for all 2D variables and some 3D variables. There are a few 3D variables (e.g., mmrbc, mmrso4, so2) which result in an error during the CMORizing stage. These variables must be CMORized manually as follows:
- Change directory:\
`cd /qfs/people/[USER]/e3sm_to_cmip`
- For converting 3D E3SM variables, generate the regridded time series files first:
```
ncclimo -7 --dfl_lvl=1 --ypf=[years per file] --var=[var1,var2,var3] -c [case id for data] --yr_srt=[start year] --yr_end=[end year] --input=[input file path] --output=native_grid --regrid=regrid_timeseries --map=map_ne30np4_to_cmip6_180x360_aave.20181001.nc
```
- An example of the above command could look like this:
```
ncclimo -7 --dfl_lvl=1 --ypf=6 --var=Mass_bc, Mass_so4,SO2 -c EmissMIP_E3SMv1_F20TRC5_NUG_SO2-NO-SEAS --yr_srt=1999 --yr_end=2004 --input=/pic/dtn/[USER]/E3SM_runs/EmissMIP_E3SMv1_F20TRC5_NUG_SO2-NO-SEAS/archive/atm/hist --output=native_grid --regrid=regrid_timeseries --map=map_ne30np4_to_cmip6_180x360_aave.20181001.nc
```
- For converting 3D CESM variables, omit the map option. Use the native grid files instead. Generating the regridded timeseries does not work since the CESM input data are at a different resolution than the map file specifies. For example:
```
ncclimo -7 --dfl_lvl=1 --ypf=6 --var=bc_a1,bc_a4,bc_c1,bc_c4,so4_a1,so4_c1,so4_a2,so4_c2,so4_a3,so4_c3,SO2 -c EmissMIP_CESM1_FAMIPC5_NUG_SHP-80P-RED --yr_srt=1999 --yr_end=2004 --input=/pic/dtn/[USER]/CESM_runs/EmissMIP_CESM1_FAMIPC5_NUG_SHP-80P-RED/run/atm --output=native_grid
```
- For CESM variables only, add lat_bnds and lon_bnds to the native grid output files. The modified files will be put in the *native_add_bounds* directory.
```
cd native_grid

for fl in `ls *.nc ; do
ncap2 -s ' defdim("vrt_nbr",2); lon_bnds=make_bounds(lon,$vrt_nbr); lat_bnds=make_bounds(lat,$vrt_nbr);' ${fl} ../native_add_bounds/${fl}
done
```
- Finally, run the CMOR handlers by invoking the converter as a python module:
```
cd /qfs/people/[USER]/e3sm_to_cmip/e3sm_to_cmip

python -m e3sm_to_cmip -v [3Dvar1, 3Dvar2, 3Dvar3] -u /qfs/people/[USER]/e3sm_to_cmip/[e3sm_user_config_picontrol.json or cesm_user_config_draft.json] -i /qfs/people/[USER]/e3sm_to_cmip_test/[regrid_timeseries or native_add_bounds] -o /qfs/people/[USER]/e3sm_to_cmip/e3sm_to_cmip/CMIP6 -t /qfs/people/[USER]/e3sm_to_cmip/cmip6-cmor-tables/Tables -H /qfs/people/[USER]/e3sm_to_cmip/e3sm_to_cmip/e3sm_to_cmip/cmor_handlers
```
- Again, the final CMORized output files will be in the CMIP6 directory.

## Setting up and running ESMValTool
ESMValTool is a climate model diagnostics and evaluation package. We use it to extract timeseries data for each climate model. Visit the [GitHub page](https://github.com/ESMValGroup/ESMValTool) for detailed documentation. It is highly recommended to view the [tutorial](https://esmvalgroup.github.io/ESMValTool_Tutorial/) alongside the following instructions.

### Prerequisites
From your home directory on PIC, clone the forked ESMValTool repository from the JGCRI/ESMValTool GitHub page:\
`git clone https://github.com/JGCRI/ESMValTool.git`

Set up conda environment on PIC and install ESMValTool package:\
`module load julia`\
`module load python/miniconda3.8`\
`source /share/apps/python/miniconda3.8/etc/profile.d/conda.sh`\
`conda create -n esmvaltool -c conda-forge -c esmvalgroup esmvaltool==2.1.1 python=3.8`\
`conda activate esmvaltool`

Check to see that the package tbb is version 2020.2 by running `conda list` (if not install it)\
`conda install tbb=2020.2`

Download the configuration file *config-user.yml*, which contains important global parameters for running ESMValTool (saved to */qfs/people/[USER]/.esmvaltool/config-user.yml*):\
`esmvaltool config get_config_user`

Add the following model file path structure to the file */people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvalcore/config-developer.yml*. This is the developer’s configuration file for ESMValTool. When new models become available, add their corresponding file path structure here too.
```
MIROC:
  cmor_strict: false
  input_dir:
    default: '/'
    BADC: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    DKRZ: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    ETHZ: '{exp}/{mip}/{short_name}/{dataset}/{ensemble}/{grid}/'
  input_file: '{short_name}_{dataset}_{activity}_{exp}*.nc'
  output_file: '{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}'
  cmor_type: 'CMIP6'

NorESM2:
  cmor_strict: false
  input_dir:
    default: '/'
    BADC: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    DKRZ: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    ETHZ: '{exp}/{mip}/{short_name}/{dataset}/{ensemble}/{grid}/'
  input_file: '{short_name}_{dataset}_{exp}*.nc'
  output_file: '{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}'
  cmor_type: 'CMIP6'

GFDL:
  cmor_strict: false
  input_dir:
    default: '/'
    BADC: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    DKRZ: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    ETHZ: '{exp}/{mip}/{short_name}/{dataset}/{ensemble}/{grid}/'
  input_file: '{short_name}_{dataset}_{exp}*.nc'
  output_file: '{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}'
  cmor_type: 'CMIP6'

OsloCTM3:
  cmor_strict: false
  input_dir:
    default: '/'
    BADC: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    DKRZ: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    ETHZ: '{exp}/{mip}/{short_name}/{dataset}/{ensemble}/{grid}/'
  input_file: '{short_name}_{dataset}_{activity}_{exp}*.nc'
  output_file: '{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}'
  cmor_type: 'CMIP6'

UKESM:
  cmor_strict: false
  input_dir:
    default: '/'
    BADC: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    DKRZ: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    ETHZ: '{exp}/{mip}/{short_name}/{dataset}/{ensemble}/{grid}/'
  input_file: '{short_name}_{dataset}_{activity}_{exp}*.nc'
  output_file: '{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}'
  cmor_type: 'CMIP6'
  
GEOS:
  cmor_strict: false
  input_dir:
    default: '/'
    BADC: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    DKRZ: '{activity}/{institute}/{dataset}/{exp}/{ensemble}/{mip}/{short_name}/{grid}/{latestversion}'
    ETHZ: '{exp}/{mip}/{short_name}/{dataset}/{ensemble}/{grid}/'
  input_file: '{short_name}_{dataset}_{activity}_{exp}*.nc'
  output_file: '{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}'
  cmor_type: 'CMIP6'
```

Make changes to the configuration file */qfs/people/[USER]/.esmvaltool/config-user.yml*:
- To save the preprocessor directory for each ESMValTool run, change *remove_preproc_dir* from *true* to *false*
- Set the destination directory for the output (will currently output to home directory)
- Change the rootpath to look like this:
```
   CMIP6: [/pic/projects/GCAM/Emissions-MIP/models/CMIP6, /pic/projects/GCAM/Emissions-MIP/models/GISS]
   MIROC: [/pic/projects/GCAM/Emissions-MIP/models/MIROC]
   NorESM2: [/pic/projects/GCAM/Emissions-MIP/models/NorESM2]
   GFDL: [/pic/projects/GCAM/Emissions-MIP/models/GFDL]
   OsloCTM3: [/pic/projects/GCAM/Emissions-MIP/models/OsloCTM3]
   UKESM: [/pic/projects/GCAM/Emissions-MIP/models/UKESM]
   GEOS: [/pic/projects/GCAM/Emissions-MIP/models/GEOS]
```
- The directory structure should have:
```
   CMIP6: default
   MIROC: default
```
Make changes to the configuration file */qfs/people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvaltool/config-references.yml*:
- Add author to list:
```
  nicholson_matthew:
    name: Nicholson, Matthew
    institute: PNNL, US
    orcid:
```
- Add project to list:
`emissions_mip: Model Intercomparison Project, PNNL`

Add new shapefiles for masking different regions of the globe, such as hemispheric land or ocean, to */qfs/people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvalcore/preprocessor/ne_masks*. These files can be found in the [JGCRI/emissions_mip repo](https://github.com/JGCRI/emissions_mip/tree/master/esmvaltool/masks).

Add the list of new shapefiles to */qfs/people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvalcore/preprocessor/_mask.py*. Under `def mask_landsea`, add the following to the list of shapefiles:
```
'sea_n-land': os.path.join(cwd, 'ne_masks/sea_n-land.shp'),
'sea_s-land': os.path.join(cwd, 'ne_masks/sea_s-land.shp'),
'land_n-sea': os.path.join(cwd, 'ne_masks/land_n-sea.shp'),
'land_s-sea': os.path.join(cwd, 'ne_masks/land_s-sea.shp'),
'non-arctic': os.path.join(cwd, 'ne_masks/non-arctic.shp'),
'non-pacific': os.path.join(cwd, 'ne_masks/non-pacific.shp'),
'non-atlantic': os.path.join(cwd, 'ne_masks/non-atlantic.shp'),
'non-indian': os.path.join(cwd, 'ne_masks/non-indian.shp')
```

### Running ESMValTool
The steps above only need to be done once. The steps below are done every time on PIC.

Loading the environment:\
`module load julia`\
`module load python/miniconda3.8`\
`source /share/apps/python/miniconda3.8/etc/profile.d/conda.sh`\
`conda activate esmvaltool`

To run a single recipe on the login node, start with moving to the directory containing ESMValTool and then run the tool (more about recipes at the end):\
`cd /pic/projects/GCAM/Emissions-MIP`\
`esmvaltool run ESMValTool/esmvaltool/recipes/emissions_mip/Phase1a/global/global_reference.yml`

To run all the recipes consecutively (or any number of recipes) it is better to excecute it as a shell script rather than on the login node. First, print the list of the recipes including their absolute paths:\
`cd /pic/projects/GCAM/Emissions-MIP/ESMValTool/esmvaltool/recipes/emissions_mip/Phase1a`\
`find $(pwd) -type f | grep -E ".yml" > Phase1a_files.txt`

Append `esmvaltool run` to the front of each line and save as a new file:\
`awk -F[_] '{print "esmvaltool run " $0}' < Phase1a_files.txt > Phase1a_recipes.txt`

Now create a shell script with the following contained within:
```
#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 50:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH -n 1
#SBATCH --mail-user <your_email_here>
#SBATCH --mail-type END

#Activate conda environment
module purge
module load julia
module load python/miniconda3.8
source /share/apps/python/miniconda3.8/etc/profile.d/conda.sh
conda activate esmvaltool

#Actually codes starts here
now=$(date)
echo "Current time : $now"

#Execute command in text file line by line
cd /pic/projects/GCAM/Emissions-MIP/ESMValTool/esmvaltool/recipes/emissions_mip/Phase1a
cat Phase1a_recipes.txt | sh -v

now=$(date)
echo "Current time : $now"
```
This approach is generally fine for processing only a few recipes (less than 10). For running a large number of recipes it is recommended to run them in parallel. This is done by splitting the recipes in batches and running each batch as separate shell script. The shell scripts can be executed simultaneously.

### Extracting Results from ESMValTool
The output will be stored in *esmvaltool_output* in your home directory (or wherever you set the output directory to). Explore the contents of the output folder. The plots subdirectory contains a .csv file of the globally averaged values for each variable, as well as a corresponding plot.

Run the following set of commands on PIC to copy the .csv file outputs from *esmvaltool_output* to a new directory called *esmvaltool_copy* (this can be called anything), which would then be the input for the Emissions-MIP_Data repo:
- Change directory to the shared Emissions-MIP project directory on PIC:\
`cd /pic/projects/GCAM/Emissions-MIP`
- Print list of perturbation folders from *esmvaltool_output*\
`ls esmvaltool_output | grep -v "reference" > pert_list.txt`
- Print list of reference folders from *esmvaltool_output*\
`ls esmvaltool_output | grep -E "reference" > ref_list.txt`
- Make *esmvaltool_copy* folder if not already there\
`mkdir -p esmvaltool_copy`
- Remove content from *esmvaltool_copy* if not empty and move to it\
`rm -rf esmvaltool_copy/*`\
`cd esmvaltool_copy`
- Make perturbation folders based on folder name pattern\
`awk -F[_] '{print "mkdir -p " $1 "/" $3 "/" $2}' < ../pert_list.txt | sh -v`

- Copy csv data files from *esmvaltool_output* to *esmvaltool_copy*
```
awk -F[_] '{print "cp -R ../esmvaltool_output/" $0 "/plots/Emissions_MIP_analysis/initial_analysis_output/*.csv " $1 "/" $3 "/" $2}' < ../pert_list.txt | sh -v
```
- Do the same with reference folders\
`awk -F[_] '{print "mkdir -p " $1 "/" $2}' < ../ref_list.txt | sh -v`
```
awk -F[_] '{print "cp -R ../esmvaltool_output/" $0 "/plots/Emissions_MIP_analysis/initial_analysis_output/*.csv " $1 "/" $2}' < ../ref_list.txt | sh -v
```
- Move up one directory and then delete the text files\
`cd ../`\
`rm pert_list.txt ref_list.txt`

After all recipes have been evaluated by ESMValTool, the output .csv files are used to generate timeseries and summary plots. The current results are stored on our [JGCRI/Emissions-MIP_Data](https://github.com/JGCRI/Emissions-MIP_Data) GitHub page. Browse the site for more details on generating plots.

## Running the recipe generator scripts
All recipes for Phase 1 and the scripts used to generate them are stored on the [JGCRI/recipe-generator](https://github.com/JGCRI/recipe-generator) GitHub page.

The recipe files are written in yml language and is essentially a list of instructions for ESMValTool to process the model data and produce various outputs. We generate the recipe files using a series of R scripts. These scripts use the yml R package to build the recipe in the format required by ESMValTool. There are three types of recipe outputs: reference, difference, and percent difference. A set of these recipes are generated for each region.

There is currently a script for each perturbation experiment as well as the reference case. The reference script simply generates the reference recipes. Each perturbation experiment recipe generates either a difference or percent difference recipe. 

After running the scripts, the recipe files will be saved to the Phase1a folder. This folder contains subfolders for each region. Copy the entire Phase1a folder to */pic/projects/GCAM/Emissions-MIP/ESMValTool/esmvaltool/recipes/emissions_mip*. ESMValTool now has access to the recipes needed for running.

## Running 2D difference map diagnostic
Another useful diagnostic that can be run on ESMValTool is the difference map. This is essentially another recipe where one may specify a pair of model runs, the region and the desired variables, and the resulting output will yield a difference map between the two model runs in various formats, including .png and .nc. This is especially useful for visualizing the difference between the perturbation and reference case of a given model. A sample recipe can be seen here: */pic/projects/GCAM/Emissions-MIP/ESMValTool/esmvaltool/recipes/emissions_mip/Phase1a_diff-maps*

Before running the recipe, make sure to overwrite the following files in your personal conda environment (assuming it's called *esmvaltool*) with the ones provided in the [JGCRI/emissions_mip repo](https://github.com/JGCRI/emissions_mip/tree/master/esmvaltool/diff_maps):
- */people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvaltool/diag_scripts/validation.py*
- */people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvaltool/diag_scripts/shared/_validation.py*
- */people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvaltool/config-references.yml*

## Obtaining total column variables
ESMValTool offers the ability to derive total column variables by vertically integrating the 3D variable over its layers. Details on this module can be found in the [tutorial](https://docs.esmvaltool.org/projects/ESMValCore/en/latest/recipe/preprocessor.html#variable-derivation). This is particularly useful for generating the total column BC, SO4, and SO2 variables (i.e., `loadbc`, `loadso4`, `loadso2`). The steps for setting up and running this tool are as follows:
* Copy files *_baseclass.py*, *_shared.py*, *loadso4.py*, *loadso2.py*, and *loadbc.py* from the repo (https://github.com/JGCRI/emissions_mip/tree/master/esmvaltool/total_column) to */qfs/people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvalcore/preprocessor/_derive*
* Add new variables `loadbc` and `loadso2` to the CMIP6 Emon table here */qfs/people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvalcore/cmor/tables/cmip6/Tables/CMIP6_Emon.json* by appending the following chunk:
```
        "loadbc": {
            "frequency": "mon", 
            "modeling_realm": "atmos", 
            "standard_name": "atmosphere_mass_content_of_elemental_carbon_dry_aerosol_particles", 
            "units": "kg m-2", 
            "cell_methods": "area: time: mean", 
            "cell_measures": "area: areacella", 
            "long_name": "Load of Black Carbon Aerosol", 
            "comment": "The total dry mass of black carbon aerosol particles per unit area.", 
            "dimensions": "longitude latitude time", 
            "out_name": "loadbc", 
            "type": "real", 
            "positive": "", 
            "valid_min": "", 
            "valid_max": "", 
            "ok_min_mean_abs": "", 
            "ok_max_mean_abs": ""
        }, 
        "loadso2": {
            "frequency": "mon", 
            "modeling_realm": "atmos", 
            "standard_name": "atmosphere_mass_content_of_sulfur_dioxide", 
            "units": "kg m-2", 
            "cell_methods": "area: time: mean", 
            "cell_measures": "area: areacella", 
            "long_name": "Load of Sulfur Dioxide", 
            "comment": "The total mass of sulfur dioxide per unit area.", 
            "dimensions": "longitude latitude time", 
            "out_name": "loadso2", 
            "type": "real", 
            "positive": "", 
            "valid_min": "", 
            "valid_max": "", 
            "ok_min_mean_abs": "", 
            "ok_max_mean_abs": ""
        }
```
* Running the diagnostic requires the 3D variable of interest (e.g., `loadbc`) as well as the pressure variable `ps` (netCDF file)
* If the 3D variable was generated using the e3sm_to_cmip tool (e.g., CESM1, E3SM) remove *standard name* of the pressure parameter (*ps*) from the 3D variable file. For example, for `mmrso4` this would look like:\
`ncatted -O -a standard_name,ps,d,c,"surface_air_pressure" mmrso4_AERmon_CESM-1-0_nudge-SO2-no-seas_r1i1p1f1_gr_199901-201412.nc`
* A sample recipe for generating `loadbc`, `loadso4`, and `loadso2` for the GISS reference case would look something like this (note the `monthly_statistics` in the preprocessors section):
```
documentation:
  description: Analysis of reference model outputs for Emissions-MIP
  authors:
    - nicholson_matthew
  maintainer:
    - nicholson_matthew
  references:
    - esmvaltool
  projects:
    - esmval
    - emissions_mip

datasets:
        - {dataset: GISS-nudge, project: CMIP6, activity: AerChemMIP, institute: NASA-GISS, exp: reference, ensemble: r1i1p5f1, grid: gn}

preprocessors:
  preproc_mask:
    mask_landsea:
      mask_out: ~
  preproc_nolev:
    regrid:
      target_grid: 1x1
      scheme: linear
    monthly_statistics:
      operator: mean

diagnostics:
  Emissions_MIP_analysis:
    description: Model variable outputs
    themes:
      - phys
    realms:
      - atmos
    variables:
      loadbc:
        preprocessor: preproc_nolev
        derive: true
        force_derivation: true
        mip: Emon
        start_year: 2000
        end_year: 2004
      loadso4:
        preprocessor: preproc_nolev
        derive: true
        force_derivation: true
        mip: Emon
        start_year: 2000
        end_year: 2004
      loadso2:
        preprocessor: preproc_nolev
        derive: true
        force_derivation: true
        mip: Emon
        start_year: 2000
        end_year: 2004
    scripts:
      initial_analysis_output:
        script: /pic/projects/GCAM/Emissions-MIP/ESMValTool/esmvaltool/diag_scripts/emissions_mip/initial_analysis-giss.py
        quickplot:
          plot_type: pcolormesh
```
* The resulting total column files can be found in the *preproc* folder of the designated ESMValTool ouput directory. Rename the netCDF file as needed and move to the appropriate model directory.
