#!/bin/bash
#
# Matt Nicholson
# 28 Feb 2020
#
#SBATCH -A ceds
#SBATCH -t 4:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

# Activate the Conda env -------------------------------------------------------
source activate pyreshaper

# Load required modules --------------------------------------------------------
module purge
module load gcc          # NetCDF requires a compiler module to be loaded as well
module load netcdf       # The cmor-ize script requires netCDF3 or netCDF4
module load openmpi

#python reshape-famipc5.py
python reshape-famipc5_merra2.py
python reshape-famipc5_merra2_so4_nseas.py
python reshape-famipc5_so4_nseas.py