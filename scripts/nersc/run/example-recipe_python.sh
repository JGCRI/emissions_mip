#!/bin/bash
# A script to run recipe_python.yml using the config-user_default.yml file.
# I'm too lazy to keep typing the long paths associated with my Win10 linux subsys

# ============================ Variable definitions ============================
CONDA_ENV="emip"
F_CONFIG="~/emip-evt/config/config-user_test.yml"
F_RECIPE="~/emip-evt/recipes/examples/recipe_python.yml"
# ==============================================================================

NOW=$(date '+%a %d %b %Y %X')
echo $NOW

# Load Python & Conda
module load python

# Activate the Conda env.
# NOTE: use "source activate" instead of "conda activate"
echo "Activating Conda env $CONDA_ENV"
source activate $CONDA_ENV

# Call ESMValTool
esmvaltool -c $F_CONFIG $F_RECIPE

echo "Deactivating Conda env $CONDA_ENV"
conda deactivate 

NOW=$(date '+%a %d %b %Y %X')
echo $NOW