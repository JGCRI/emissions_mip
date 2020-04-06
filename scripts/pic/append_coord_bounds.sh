#!/bin/bash
#
# Add lat_bnds & lon_bnds to CESM timeseries output netCDF files.
#
# Matt Nicholson
# 3 April 2020
#
#SBATCH -A ceds
#SBATCH -t 4:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

source activate emip

DIR_ROOT="/pic/projects/GCAM/mnichol/emip/model-output/pnnl-cesm"
MODELS=("FAMIPC5" "FAMIPC5_MERRA2" "FAMIPC5_MERRA2_SO4_NSEAS" "FAMIPC5_SO4_NSEAS")

for MODEL in "${MODELS[@]}"; do
   echo "Processing $MODEL..."
   IN_DIR="$DIR_ROOT/$MODEL/timeseries"
   python append_coord_bounds.py $IN_DIR