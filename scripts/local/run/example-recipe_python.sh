#!/bin/bash
# A script to run recipe_python.yml using the config-user_default.yml file.
# I'm too lazy to keep typing the long paths associated with my Win10 linux subsys

# ============================ Variable definitions ============================
CONDA_ENV="esmvaltool"
F_CONFIG="~/esmvaltool/config/config-user_default.yml"
F_RECIPE="~/esmvaltool/recipes/examples/recipe_python.yml"
# ==============================================================================

NOW=$(date '+%a %d %b %Y %X')
echo $NOW

# Activate the Conda env. Not sure this is necessary though
echo "Activating Conda env $CONDA_ENV"
conda activate $CONDA_ENV

# Call ESMValTool
esmvaltool -c $F_CONFIG $F_RECIPE

echo "Deactivating Conda env $CONDA_ENV"
conda deactivate 

NOW=$(date '+%a %d %b %Y %X')
echo $NOW