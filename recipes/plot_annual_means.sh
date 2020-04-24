#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

module purge
source activate emip

now=$(date)
echo "Current time : $now"

python plot_annual_means.py

now=$(date)
echo "Current time : $now"