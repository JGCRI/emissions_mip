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
| Directory      | Path                                                                                              |
| :------------- |:------------------------------------------------------------------------------------------------- |
| root           | `/home/nich980/emip/input`                                                                        |
| GISS-Orig-root | `/home/nich980/emip/input/GISS-ORIGINAL`                                                          |
| GISS-Orig-nc   | `ROOT/AerChemMIP/NASA-GISS/GISS-E2-1-G/piClim-SO2/<archive>/AERmon/<var>/gn/v20191120/<var_nc>`   |
| GISS-EMIP-root | `/home/nich980/emip/input/GISS-EMIP`                                                              |
| GISS-EMIP-nc   | `ROOT/AerChemMIP/NASA-GISS/GISS-E2-1-G/<experiment>/<archive>/AERmon/<var>/gn/v20191120/<var_nc>` |
| Sample Input   | `/home/nich980/emip/input/input4mips`                                                             |

### Output
| Directory         | Path                                                                         |
| :---------------- |:---------------------------------------------------------------------------- |
| root              | `/home/nich980/emip/output`                                                  |
| Recipes           | `/home/nich980/esmvaltool/jgcri-fork/ESMValTool/recipes/emissions_mip`       |
| Diagnostics       | `/home/nich980/esmvaltool/jgcri-fork/ESMValTool/diag_scripts/emissions_mip`  |
| Output - Plots    | `/home/nich980/emip/output/diagnostics`                                      |
| Output - EVT Logs | `/home/nich980/emip/output<recipe_name>/run/<diagnostic_name>/<script_name>` |


### JGCRI ESMValTool Fork
| Directory   | Path                                                                        |
| :---------- |:--------------------------------------------------------------------------- |
| root        | `/home/nich980/esmvaltool/jgcri-fork/ESMValTool/esmvaltool`                 |
| Usr config  | `/home/nich980/esmvaltool/jgcri-fork/ESMValTool/config-user`                |
| Recipes     | `/home/nich980/esmvaltool/jgcri-fork/ESMValTool/recipes/emissions_mip`      |
| Diagnostics | `/home/nich980/esmvaltool/jgcri-fork/ESMValTool/diag_scripts/emissions_mip` |

### Windows Partition
| Directory | Path                             |
| :-------- |:-------------------------------- |
| root      | `/mnt/c/users/nich980/`          |
| EMIP repo | `/mnt/c/users/nich980/code/emip` |
| Output    | `/mnt/c/users/nich980/data/emip` |

---

# ESMValTool
## CMOR Data Reference Syntax & Data Finder
The [Data Finder](https://esmvaltool.readthedocs.io/projects/ESMValCore/en/latest/quickstart/find_data.html) is how ESMValTool finds datasets specified in recipes. 

