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
import netcdf_variable
import date_utils
import var_funcs
import plotting
import recipe_utils

# SET THIS VARIABLE TO THE NAME OF THE VARIABLE YOU WISH TO PLOT
VARIABLE = 'dryso4'

OUTPUT_SOURCES = 
