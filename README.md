# Emissions-MIP

This repository holds scripts and files used for contributions to the Emissions-MIP Sensitivity Evaluation project

## Repository Overview
In addition to containing the framework to perform initial analysis for the EMIP project, this repository also hold scripts and handler files needed to transform raw model output files to the [Climate Model Output Rewriter (CMOR)](https://cmor.llnl.gov/) format. 

* `cmor_handlers` contains variable handler scripts needed to CMOR-ize CESM output via [e3sm_to_cmip](https://github.com/E3SM-Project/e3sm_to_cmip).
* `docs` contains variaous documents pertaining to model output variables and their mappings.
* `recipes` contains recipes to run the EMIP initial analysis.
* `scripts` contains various scripts to process raw model output.
* `src` contains the files that make up the initial analysis framework.
