# PNNL CESM Outputs
This document provides details for the outputs from PNNL's CESM runs as part of the [Emissions-MIP Sensitivity Evaluation project](../README.md).

## Location - NERSC
PNNL's CESM run outputs are located on the National Energy Research Scientific Computing Center's [Cori supercomputer](https://www.nersc.gov/systems/cori/). 

After connecting to Cori, the model output from the four Phase 1 experiments can be found in the `/global/cscratch1/sd/mwu1/CESM_runs` directory. 

This directory contains four subdirectories, one for each experiment: `FAMIPC5`, `FAMIPC5_MERRA2`, `FAMIPC5_MERRA2_SO4_NSEAS`, and `FAMIPC5_SO4_NSEAS`. 

Each experiment directory contains two subdirectories, `bld` and `run`. The `run` subdirectory holds the output files from the model run. 

Note: `/global/cscratch1/sd/mwu1/CESM_runs` also contains two test run subdirectories, `FAMIPC5_test1` and `FAMIPC5_test2`, but we don't care about these.

## Experiments

| Experiment                 | U,V Nudging   | SO2/SO4 seasonality for anthropogenic emission |
| -------------------------- |:-------------:|:----------------------------------------------:|
| `FAMIPC5`                  | Yes, MERRA2   | Yes                                            |
| `FAMIPC5_MERRA2`           | Yes, MERRA2   | No                                             |
| `FAMIPC5_MERRA2_SO4_NSEAS` | No            | Yes                                            |
| `FAMIPC5_SO4_NSEAS`        | No            | No                                             |

## CAM History Files
[CAM](http://www.cesm.ucar.edu/models/atm-cam/) produces a series of [NetCDF](https://www.unidata.ucar.edu/software/netcdf/docs/) history files containing atmospheric gridpoint data generated during the course of a run. This is a very brief overview and more can be learned about CAM history files from the [CAM Users Guide](http://www.cesm.ucar.edu/models/atm-cam/docs/usersguide/node2.html). 

### History File Types
| Type | # of Fields | Write Freq. | Filename Specifier         | Output Precision | Time Samples per File |
|:----:|:-----------:|:-----------:|:---------------------------|:----------------:|:---------------------:|
| 1    | 611         | Monthly     | `%c.cam2.h%t.%y-%m.nc`     | double           | 1                     |
| 7    | 37          | Yearly      | `%c.cam2.i.%y-%m-%d-%s.nc` | double           | 1                     |
