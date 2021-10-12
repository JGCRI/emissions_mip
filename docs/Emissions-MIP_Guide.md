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

Acquire the following files and place them in the current directory:\
- Download horizontal remapping file [*map_ne30np4_to_cmip6_180x360_aave.20181001.nc*](https://web.lcrc.anl.gov/public/e3sm/mapping/maps/) that is required for the E3SM workflow
- *vrt_remap_plev19.nc*
- *cesm_user_config_draft.json*
- *e3sm_user_config_picontrol.json*

Create the following directories (they will hold processed data):\
`mkdir native_add_bounds native_grid regrid_timeseries`

Clone a copy of the CMIP6 Controlled Vocabulary tables:
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
- For CESM variables only, add lat_bnds and lon_bnds to the native grid output files. The modified files will be put in the *native_add_bounds* directory.\
`cd native_grid`
```
for fl in `ls *.nc ; do
ncap2 -s ' defdim("vrt_nbr",2); lon_bnds=make_bounds(lon,$vrt_nbr); lat_bnds=make_bounds(lat,$vrt_nbr);' ${fl} ../native_add_bounds/${fl}
done
```
- Finally, run the CMOR handlers by invoking the converter as a python module:\
`cd /qfs/people/[USER]/e3sm_to_cmip/e3sm_to_cmip`
```
python -m e3sm_to_cmip -v [3Dvar1, 3Dvar2, 3Dvar3] -u /qfs/people/[USER]/e3sm_to_cmip/[e3sm_user_config_picontrol.json or cesm_user_config_draft.json] -i /qfs/people/[USER]/e3sm_to_cmip_test/[regrid_timeseries or native_add_bounds] -o /qfs/people/[USER]/e3sm_to_cmip/e3sm_to_cmip/CMIP6 -t /qfs/people/[USER]/e3sm_to_cmip/cmip6-cmor-tables/Tables -H /qfs/people/[USER]/e3sm_to_cmip/e3sm_to_cmip/e3sm_to_cmip/cmor_handlers
```
- Again, the final CMORized output files will be in the CMIP6 directory.

## Setting up and running ESMValTool
ESMValTool is a climate model diagnostics and evaluation package. We use it to extract timeseries data for each climate model. Visit the [GitHub page](https://github.com/ESMValGroup/ESMValTool) for detailed documentation. It is highly recommended to view the [tutorial](https://esmvalgroup.github.io/ESMValTool_Tutorial/) alongside the following instructions.

From your home directory on PIC, clone the forked ESMValTool repository from the JGCRI/ESMValTool GitHub page:\
`git clone https://github.com/JGCRI/ESMValTool.git`

Set up conda environment on PIC and install ESMValTool package:
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
```

Make changes to the configuration file */qfs/people/[USER]/.esmvaltool/config-user.yml*:\
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
Make changes to the configuration file */qfs/people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvaltool/config-references.yml*:\
- Add author to list:
```
  nicholson_matthew:
    name: Nicholson, Matthew
    institute: PNNL, US
    orcid:
```
- Add project to list:
`emissions_mip: Model Intercomparison Project, PNNL`

Add new shapefiles for masking different regions of the globe, such as hemispheric land or ocean, to */qfs/people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvalcore/preprocessor/ne_masks*. These files will be provided.

Add the list of new shapefiles to */qfs/people/[USER]/.conda/envs/esmvaltool/lib/python3.8/site-packages/esmvalcore/preprocessor/_mask.py*. Under `def mask_landsea`, add the following to the list of shapefiles:
```
'sea_n-land': os.path.join(cwd, 'ne_masks/sea_n-land.shp'),
'sea_s-land': os.path.join(cwd, 'ne_masks/sea_s-land.shp'),
'land_n-sea': os.path.join(cwd, 'ne_masks/land_n-sea.shp'),
'land_s-sea': os.path.join(cwd, 'ne_masks/land_s-sea.shp'),
'non-arctic': os.path.join(cwd, 'ne_masks/non-arctic.shp'),
'non-pacific': os.path.join(cwd, 'ne_masks/non-pacific.shp'),
'non-atlantic': os.path.join(cwd, 'ne_masks/non-atlantic.shp')
```
The steps above only need to be done once. The steps below are done every time on PIC.

Loading the environment:\
`module load julia`\
`module load python/miniconda3.8`\
`source /share/apps/python/miniconda3.8/etc/profile.d/conda.sh`\
`conda activate esmvaltool`

To run a single recipe start with moving to the directory containing ESMValTool and then run the tool (more about recipes at the end):\
`cd /pic/projects/GCAM/Emissions-MIP`\
`esmvaltool run ESMValTool/esmvaltool/recipes/emissions_mip/Phase1a/global/global_reference.yml`



