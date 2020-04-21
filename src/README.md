# Emissions-MIP Initial Analysis framework

The files in this directory create an object-oriented framework to support initial analysis of CMOR-ized CESM output.

## Files in this directory
* `config.py` holds classes and functions used to configure the analysis run, i.e., directory paths, loggers, etc. 
* `date_utils.py` contains functions to convert netCDF time variable values (in days since 01-01-2000) to dates and vice versa.
* `netcdf.py` holds the Netcdf object class, which represents a single CMOR-ized variable timeseries file.  
* `netcdf_variable.py` holds the NetcdfVariable class, which represents a single variable from a a single CMOR-ized variable timeseries file. 
* `path_funcs.py` contains functions to parse directory and file paths.
* `plotting.py` contains plotting functions.
* `var_funcs.py` contains functions that operate on variables, such as computing the annual averages of a variable.

The `test/` directory holds tests for these files.
