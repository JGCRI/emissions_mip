#!/bin/bash
# Transform E3SM SO2 time series output to CMIP-compatibale data.
#
# cmor repo:         https://github.com/PCMDI/cmor
# e3sm_to_cmip repo: https://github.com/E3SM-Project/e3sm_to_cmip
#
# Matt Nicholson
# 24 Feb 2020

# Activate the Conda env -------------------------------------------------------
conda activate e3sm_to_cmip

# Load required modules --------------------------------------------------------
module purge
module load gcc          # NetCDF requires a compiler module to be loaded as well
module load netcdf       # The cmor-ize script requires netCDF3 or netCDF4

# Initialize directory variables -----------------------------------------------
VAR="SO2"                                     # Variable(s) to convert
DIR_ROOT="/pic/projects/GCAM/mnichol/emip"    # Root EMIP project directory on pic
DIR_TEST="lib/cmor/cmor/Test"                 # Cmor repo Test directory
DIR_TABLES="lib/cmor/cmor/Tables"             # Cmor repo Tables directory
DIR_PREFIX="model-output/pnnl-cesm"           # $DIR_ROOT/model-output/pnnl-cesm
DIR_INPUT="run"                               # $DIR_ROOT/model-output/pnnl-cesm/<model>/run
DIR_OUTPUT="cmip6"                            # $DIR_ROOT/model-output/pnnl-cesm/<model>/cmip6
DIR_HANDLER="lib/e3sm_to_cmip/cmor_handlers"  # $DIR_ROOT/lib/e3sm_to_cmip/cmor_handlers
DIR_USR_IN="lib/e3sm_to_cmip/user_input/e3sm_user_config_emip.json"  # User-defined CMIP6 metadata file
# List of models whose output we need to convert
MODELS=("FAMIPC5" "FAMIPC5_MERRA2" "FAMIPC5_MERRA2_SO4_NSEAS" "FAMIPC5_SO4_NSEAS")

# Formulate the function call & pray -------------------------------------------
cd $DIR_ROOT

for MODEL in "${MODELS[@]}"; do
   echo "Processing $MODEL..."
   CURR_IN="$DIR_PREFIX/$MODEL/$DIR_INPUT"
   CURR_OUT="$DIR_PREFIX/$DIR_OUTPUT"
   e3sm_to_cmip -v $VAR -i $CURR_IN -o $CURR_OUT --tables $DIR_TABLES --handlers $DIR_HANDLER --user-input $DIR_USR_IN
done