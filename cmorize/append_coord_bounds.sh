#!/bin/bash
#
# Add lat_bnds, lon_bnds, & time_bnds to CESM timeseries netCDF files.
#
# Matt Nicholson
# 3 April 2020
#
#SBATCH -A ceds
#SBATCH -t 3:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

source activate pyreshaper

DIR_ROOT="/pic/projects/GCAM/mnichol/emip/model-output/pnnl-cesm"

# --- FAMIPC5 output -----------------------------------------------------------
MODEL="FAMIPC5"
echo "Processing $MODEL..."
IN_DIR="$DIR_ROOT/$MODEL/timeseries"
python append_coord_bounds.py $IN_DIR

# --- FAMIPC5_MERRA2 output ----------------------------------------------------
MODEL="FAMIPC5_MERRA2"
echo "Processing $MODEL..."
IN_DIR="$DIR_ROOT/$MODEL/timeseries"
python append_coord_bounds.py $IN_DIR

# --- FAMIPC5_MERRA2_SO4_NSEAS output ------------------------------------------
MODEL="FAMIPC5_MERRA2_SO4_NSEAS"
echo "Processing $MODEL..."
IN_DIR="$DIR_ROOT/$MODEL/timeseries"
python append_coord_bounds.py $IN_DIR

# --- FAMIPC5_SO4_NSEAS output -------------------------------------------------
MODEL="FAMIPC5_SO4_NSEAS"
echo "Processing $MODEL..."
IN_DIR="$DIR_ROOT/$MODEL/timeseries"
python append_coord_bounds.py $IN_DIR

