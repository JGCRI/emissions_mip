Dev Notes for the Emissions-MIP project and [ESMValTool](https://github.com/ESMValGroup/ESMValTool) software package.

Last updated 20 May 2020.

Matt Nicholson

# Emissions-MIP

## Phase 1 Model Configurations

|   Run   |   Archive  |  Base/Perturb. | Wind Nudging | Seasonality | Modified Model Name    | Experiment Name |
| :------ |:---------- | :------------- |:------------ | :---------- | :--------------------- | :-------------- |
| BNW1999 | r1i1p5f101 | base           | no           | yes         | GISS-base              | season-so2      |
| PWN1999 | r1i1p5f102 | perturbation   | no           | no          | GISS-pert              | reference       |
| PW1999  | r1i1p5f103 | perturbation   | yes          | no          | GISS-pert-nudge        | reference       |
| BW1999  | r1i1p5f104 | base           | yes          | yes         | GISS-base-nudge        | season-so2      |

## Win10 Linux Sub-Sys Paths
### Input
* ROOT: `/home/nich980/emip/input`
* Unmodified GISS output
  * ROOT: `/home/nich980/emip/input/GISS-ORIGINAL`
  * `nc` path: `ROOT/AerChemMIP/NASA-GISS/GISS-E2-1-G/piClim-SO2/<archive>/AERmon/<var>/gn/v20191120/<var_nc>`
* EMIP-Modified GISS output
  * ROOT: `/home/nich980/emip/input/GISS-EMIP`
  * `nc` path: `ROOT/AerChemMIP/NASA-GISS/GISS-E2-1-G/<experiment>/<archive>/AERmon/<var>/gn/v20191120/<var_nc>`
* Filename convention: `<var_name>_<mip>_<model>_<experiment>_<ensemble>_<grid>_<start_date>-<end_date>.nc`
* Sample Diagnostic Input: `IN_ROOT/input4mips`

### Output
* ROOT: `/home/nich980/emip/output`
* Custom Diag Plots: `ROOT/diagnostics`
* ESMValTool Output
  * Plots: `ROOT/<recipe_name>/plots/<diagnostic_name>/<script_name>`
  * Logs:  `ROOT/<recipe_name>/run/<diagnostic_name>/<script_name>`

### JGCRI ESMValTool Fork
* ROOT: `/home/nich980/esmvaltool/jgcri-fork/ESMValTool/esmvaltool`
* User config: `/home/nich980/esmvaltool/jgcri-fork/ESMValTool/config-user`
* Recipes: `/home/nich980/esmvaltool/jgcri-fork/ESMValTool/recipes/emissions_mip`
* Diag scripts: `/home/nich980/esmvaltool/jgcri-fork/ESMValTool/diag_scripts/emissions_mip`

### Windows Partition
| Directory |              Path                |
| :-------- |:-------------------------------- |
| root      | `/mnt/c/users/nich980/`          |
| EMIP repo | `/mnt/c/users/nich980/code/emip` |
| Output    | `/mnt/c/users/nich980/data/emip` |
