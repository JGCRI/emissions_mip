# Description
This repository contains the R scripts used for generating the yml recipes for running ESMValTool. These scripts use the "yml" R package to build the recipe in the format required by ESMValTool. The recipe files are written in the yml language and is essentially a list of instructions for ESMValTool to process the model data and produce various outputs. There are three types of recipe outputs: reference, difference, and percent difference. A set of these recipes are generated for each region.

## Directories
### code
This folder contains scripts for generating Emissions-MIP Phase 1a and Phase 1b recipes. There is a script for the reference case as well as for each perturbation experiment. The reference script simply generates the reference recipes. Each perturbation experiment recipe generates either a difference or percent difference recipe.

### Phase1a
After running the scripts labeled Phase 1a, the recipe files will be saved to the Phase 1a folder. This folder contains subfolders for each region.

### Phase1b
This folder contains the recipes generated for Phase 1b.
