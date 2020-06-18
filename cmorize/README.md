This directory contains scripts dedicated to CMOR-izing CESM output via the [e3sm_to_cmip](https://github.com/E3SM-Project/e3sm_to_cmip) package.

# Tasks

## Append missing netcdf variables
In order to run e3sm_to_cmip, `lat_bnd`, `lon_bnd`, and `time_bnd` variables need to be added to the CESM output files. This is accomplished through the `append-<...>.sh` scripts. These scripts are batch job scripts that call their respective Python scripts to manually add the variables to the netcdf files. 

### Usage
Within the bash scripts, set the `IN_DIR` variable for each model configuration to the path of the directory holding the model timeseries files. Then submit the job.

**NOTE** Files must be converted from time-slice to time-series. See [PyReshaper](https://github.com/NCAR/PyReshaper) for info on how to do the conversion.

## CMOR-ize CESM output
CMOR-izing the CESM output is done through the [e3sm_to_cmip](https://github.com/E3SM-Project/e3sm_to_cmip) package. The package requires that every CMOR variable have its own Python handler script that maps the CESM variables to the CMOR variable. On pic, these scripts are currently located in the `/pic/projects/GCAM/mnichol/emip/lib/e3sm_to_cmip/cmor_handlers` directory. 

`e3sm_to_cmip` also required CMOR tables in order to execute. These tables are located in the `/pic/projects/GCAM/mnichol/emip/lib/cmor/cmor/Tables` directory.

### Installing e3sm_to_cmip
See [their docs](https://github.com/E3SM-Project/e3sm_to_cmip#installation)

### Usage on pic
Scripts in the `/pic/projects/GCAM/mnichol/emip/scripts` directory named `cmor-<...>.sh` are job scripts to run e3sm_to_cmip on pic.

Below is a list of arguments e3sm_to_cmip can take. Note not all are defined in the batch scripts.

```
usage: e3sm_to_cmip [-h]

Convert ESM model output into CMIP compatible format

optional arguments:
  -h, --help            show this help message and exit
  -v  [ ...], --var-list  [ ...]
                        space seperated list of variables to convert from e3sm
                        to cmip. Use 'all' to convert all variables
  -i , --input          path to directory containing e3sm data with single
                        variables per file
  -o , --output         where to store cmorized output
  -u <user_input_json_path>, --user-input <user_input_json_path>
                        path to user input json file for CMIP6 metadata
  -n <nproc>, --num-proc <nproc>
                        optional: number of processes, default = 6
  -t <tables-path>, --tables <tables-path>
                        Path to directory containing CMOR Tables directory
  -H <handler_path>, --handlers <handler_path>
                        path to cmor handlers directory, default =
                        ./cmor_handlers
  -N, --proc-vars       Set the number of process to the number of variables
  --version             print the version number and exit
  --debug               Set output level to debug
```
#### Example
Here's an example e3sm_to_cmip job script:
```
#SBATCH -A <allocation>
#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user your_email@where.ever
#SBATCH --mail-type END

# Activate the Conda env -------------------------------------------------------
source activate e3sm_to_cmip

# Load required modules --------------------------------------------------------
module purge
module load gcc          # NetCDF requires a compiler module to be loaded as well
module load netcdf       # The cmor-ize script requires netCDF3 or netCDF4

# Initialize directory variables -----------------------------------------------
DIR_ROOT="/pic/projects/GCAM/mnichol/emip"    # Root EMIP project directory on pic
DIR_TEST="lib/cmor/cmor/Test"                 # Cmor repo Test directory
DIR_TABLES="lib/cmor/cmor/Tables"             # Cmor repo Tables directory
DIR_HANDLER="lib/e3sm_to_cmip/cmor_handlers"  # $DIR_ROOT/lib/e3sm_to_cmip/cmor_handlers
DIR_USR_IN="lib/e3sm_to_cmip/user_input/e3sm_user_config_emip.json"  # User-defined CMIP6 metadata file

# Formulate the function call & pray -------------------------------------------
cd $DIR_ROOT

echo "Processing FAMIPC5..."

DIR_INPUT="model-output/pnnl-cesm/FAMIPC5/timeseries"
DIR_OUTPUT="model-output/pnnl-cesm/FAMIPC5/cmip"
e3sm_to_cmip -v 'drybc' -i $DIR_INPUT -o $DIR_OUTPUT -t $DIR_TABLES -H $DIR_HANDLER -u $DIR_USR_IN
```
This script is telling e3sm_to_cmip to CMOR-ize the `drybc` variable from the `FAMIPC5` CESM run. The call to `e3sm_to_cmip` takes place in the very last line, the rest of the script is loading necessary libraries and defining the paths of files `e3sm_to_cmip` takes as inputs. 
