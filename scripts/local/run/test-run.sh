#!/bin/bash

#SBATCH --account = <NERSC Repository>
#SBATCH -t 30
#SBATCH -N 1
#SBATCH --mail-type = end, fail
#SBATCH --mail-user = matthew.nicholson@pnnl.gov

# Discard active modules & load the ones we need
module purge 
module load python

# Activate the Conda env
source activate emip

# Do whatever...

# Deactivate Conda env
conda deactivate

