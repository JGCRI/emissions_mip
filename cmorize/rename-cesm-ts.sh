#!/bin/bash
#
# Rename CAM5 model output in preparation for CMORizing via e3sm_to_cmip package.
#
# Matt Nicholson
# 3 April 2020
#
#SBATCH -A ceds
#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

module purge
module load python

BASE_DIR="/pic/projects/GCAM/mnichol/emip/model-output/pnnl-cesm"

for MODEL in FAMIPC5 FAMIPC5_MERRA2 FAMIPC5_MERRA2_SO4_NSEAS FAMIPC5_SO4_NSEAS
do
  python rename-cesm-ts.py "$BASE_DIR/$MODEL/timeseries"
done
