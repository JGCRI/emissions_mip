#!/bin/bash
# Transform E3SM time series variables to CMIP-compatibale data.
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

# Define the variables we want to CMOR-ize -------------------------------------
VariableArray=(so4_a1,         # Concentration of so4_a1, in kg/kg
               so4_a2,         # Concentration of so4_a2, in kg/kg
               so4_a3,         # Concentration of so4_a3, in kg/kg
               so4_c1,         # Concentration of so4_c1 in cloud water, in kg/kg
               so4_c2,         # Concentration of so4_c2 in cloud water, in kg/kg
               so4_c3,         # Concentration of so4_c3 in cloud water, in kg/kg
               SO2,            # Concentration of SO2, in mol/mol
               BURDENSO4,      # Sulfate aerosol burden, in kg/m^2
               SFso4_a1,       # Surface flux of so4_a1, in kg/m^2/s
               SFso4_a2,       # Surface flux of so4_a2, in kg/m^2/s
               SFso4_a3,       # Surface flux of so4_a3, in kg/m^2/s
               so4_a1_CLXF,    # Vertically intergrated external forcing for so4_a1, in molec/cm^2/s
               so4_a2_CLXF,    # Vertically intergrated external forcing for so4_a2, in molec/cm^2/s
               SO2_CLXF,       # Vertically intergrated external forcing for SO2, in molec/cm^2/s
               SO2_XFRC,       # External forcing for SO2, in molec/cm^3/s
               so4_a1DDF,      # Dry deposition flux at bottom (grav + turb) for so4_a1, in kg/m^2/s
               so4_a2DDF,      # Dry deposition flux at bottom (grav + turb) for so4_a2, in kg/m^2/s
               so4_a3DDF,      # Dry deposition flux at bottom (grav + turb) for so4_a3, in kg/m^2/s
               so4_c1DDF,      # Dry deposition flux at bottom (grav + turb) for so4_c1, in kg/m^2/s
               so4_c2DDF,      # Dry deposition flux at bottom (grav + turb) for so4_c2, in kg/m^2/s
               so4_c3DDF,      # Dry deposition flux at bottom (grav + turb) for so4_c3, in kg/m^2/s
               so4_a1SFWET,    # Wet deposition flux at surface for so4_a1, in kg/m^2/s
               so4_a2SFWET,    # Wet deposition flux at surface for so4_a2, in kg/m^2/s
               so4_a3SFWET,    # Wet deposition flux at surface for so4_a3, in kg/m^2/s
               so4_c1SFWET,    # Wet deposition flux at surface for so4_c1, in kg/m^2/s
               so4_c2SFWET,    # Wet deposition flux at surface for so4_c2, in kg/m^2/s
               so4_c3SFWET,    # Wet deposition flux at surface for so4_c3, in kg/m^2/s
               FSNT,           # Net solar flux at top of model, in W/m^2
               FLNT,           # Net longwave flux at top of model, in W/m^2
               FSNT_d1,        # Net solar flux at top of model without aerosol, in W/m^2
               FLNT_d1,        # Net longwave flux at top of model without aerosol, in W/m^2
               FSNT_d2,        # Net solar flux at top of model without Sulfate, in W/m^2
               FLNT_d2,        # Net longwave flux at top of model without Sulfate, in W/m^2
               FSNS,           # Net solar flux at surface, in W/m^2
               FLNS,           # Net longwave flux at surface, in W/m^2
               FSNS_d1,        # Net solar flux at surface without aerosol, in W/m^2
               FLNS_d1,        # Net longwave flux at surface without aerosol, in W/m^2
               FSNS_d2,        # Net solar flux at surface without sulfate, in W/m^2
               FLNS_d2         # Net longwave flux at surface without sulfate, in W/m^2
               )

# Initialize directory variables -----------------------------------------------
MODELS=("FAMIPC5" "FAMIPC5_MERRA2" "FAMIPC5_MERRA2_SO4_NSEAS" "FAMIPC5_SO4_NSEAS")
DIR_ROOT=/pic/projects/GCAM/mnichol/emip  # Root EMIP project directory on pic
DIR_TEST=lib/cmor/cmor/Test               # Cmor repo Test directory
DIR_TABLES=lib/cmor/cmor/Tables           # Cmor repo Tables directory
DIR_INPUT=run                             # pnnl-cesm subdir that holds e3sm model output
DIR_OUTPUT=cmip6                          # pnnl-cesm subdir to store cmor-ized output

# Formulate the function call & pray -------------------------------------------
cd $DIR_ROOT

for model in "${MODELS[@]}"; do
   echo "Processing $model..."
   DIR_PREFIX="$DIR_INPUT/$model"
   CURR_IN="$DIR_PREFIX/$DIR_INPUT"
   CURR_OUT="$DIR_PREFIX/$DIR_OUTPUT"
   e3sm_to_cmip -v $VARS --input $CURR_IN --output $CURR_OUT -t $DIR_TEST -u ????
done