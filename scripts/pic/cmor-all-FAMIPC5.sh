#!/bin/bash
# Transform all E3SM variable time series output to CMIP-compatibale data.
#
# cmor repo:         https://github.com/PCMDI/cmor
# e3sm_to_cmip repo: https://github.com/E3SM-Project/e3sm_to_cmip
#
# Matt Nicholson
# 26 Feb 2020
#
#SBATCH -A ceds
#SBATCH -t 4:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user matthew.nicholson@pnnl.gov
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

VARS_DRY=('drybc' 'drydust' 'dryso4' 'dryss')
VARS_EMI=('emibc' 'emidust' 'emiso2' 'emiss')
VARS_MMR=('mmrbc' 'mmrdust' 'mmrso4' 'mmrss')
VARS_OD=('od550aer' 'od550dust' 'od550so4' 'od550ss')
VARS_LUT=('rlut' 'rsut')
VARS_WET=('wetbc' 'wetdust' 'wetso4' 'wetss')

# Formulate the function call & pray -------------------------------------------
cd $DIR_ROOT

echo "Processing FAMIPC5..."

DIR_INPUT="model-output/pnnl-cesm/FAMIPC5/timeseries"
DIR_OUTPUT="model-output/pnnl-cesm/FAMIPC5/cmip"
e3sm_to_cmip -v $VARS_DRY -i $DIR_INPUT -o $DIR_OUTPUT -t $DIR_TABLES -H $DIR_HANDLER -u $DIR_USR_IN