"""
This recipe creates a plot of the annual average of a variable produced by
various models or model configurations.

CONFIGURATION
-------------
* Variable to plot
    * Change VARIABLE to the name of the variable you wish to plot. 
      To create plots for more than one variable, set the value of VARIABLE
      to a list of the variables you wish to plot. Only one variable per plot.
* Models/model configurations to use


Matt Nicholson
12 April 2020
"""
import sys

sys.path.insert(1, '../src')

import netcdf
import plotting
import path_funcs


# === User Configuration ======================================================

# SET THIS VARIABLE TO THE NAME OF THE VARIABLE YOU WISH TO PLOT
VARIABLES = ['dryso2', 'dryso4', 'emiso2', 'emiso4', 'mmrso4', 'od550aer',
             'so2', 'wetso2', 'wetso4']

# SET THIS VARIABLE TO A LIST CONTAINING THE MODEL SOURCES & CONFIGURATIONS
# WHOSE OUTPUT YOU WISH TO PLOT
OUTPUT_SOURCES = ['r1i1p5f101', 'r1i1p5f102', 'r1i1p5f103', 'r1i1p5f104']

# =============================================================================

if not isinstance(VARIABLES, list):
    VARIABLES = [VARIABLES]
for VAR in VARIABLES:
    print('Processing {}...'.format(VAR))
    output_files = [path_funcs.get_var_path(src, VAR) for src in OUTPUT_SOURCES]
    nc_files = [netcdf.Netcdf(fname) for fname in output_files]
    plotting.plot_global_mean_annual(VAR, nc_files)
