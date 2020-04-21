"""
This recipe creates a plot of the monthly average of a variable produces by
various models or model configurations.

CONFIGURATION
-------------
* Variable to plot
    * Change VARIABLE to the name of the variable you with to plot.
* Models/model configurations to use
    * Add the namestrings of the models/model configurations you wish to 
      plot output from to OUTPUT_SOURCES. 
      Namestring format: <institution>-<forcing_index>.
        Ex: 'columbia-103'.

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
OUTPUT_SOURCES = ['nasa-101', 'nasa-102', 'columbia-103', 'columbia-104']

# =============================================================================
if not isinstance(VARIABLES, list):
    VARIABLES = [VARIABLES]
for VAR in VARIABLES:
    print('Processing {}...'.format(VAR))
    output_files = [path_funcs.get_var_path(src, VAR) for src in OUTPUT_SOURCES]
    nc_files = [netcdf.Netcdf(fname) for fname in output_files]
    plotting.plot_global_mean_annual(VAR, nc_files)
