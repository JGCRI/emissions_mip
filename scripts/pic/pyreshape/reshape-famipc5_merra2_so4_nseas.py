"""
Convert CESM FAMIPC5_MERRA2_SO4_NSEAS time-slice output to time-series output via PyReshape

Matt Nicholson
28 Feb 2020
"""
import os
from pyreshaper import specification, reshaper

import conversion_utils

# --- Set up -------------------------------------------------------------------
class dirs:
    ROOT   = '/pic/projects/GCAM/mnichol/emip'
    INPUT  = 'model-output/pnnl-cesm/FAMIPC5_MERRA2_SO4_NSEAS/run'
    OUTPUT = 'model-output/pnnl-cesm/FAMIPC5_MERRA2_SO4_NSEAS/timeseries'
    
# Change working directory to root project path
os.chdir(dirs.ROOT)

# Define which model output history files we want to convert
# input_fnames = ['FAMIPC5_MERRA2_SO4_NSEAS.cam.h0.2010-09.nc',
#                 'FAMIPC5_MERRA2_SO4_NSEAS.cam.h0.2010-10.nc']
input_fnames = conversion_utils.fetch_fnames(dirs.INPUT, 'FAMIPC5_MERRA2_SO4_NSEAS', 'cam')
input_files  = [os.path.join(dirs.INPUT, f) for f in input_fnames]

# Create output directory if it doesn't already exist
is not os.path.isdir(OUTPUT):
    os.makedirs(OUTPUT)

# Converted time-series file prefix & suffix
prefix = 'FAMIPC5_MERRA2_SO4_NSEAS.cam.'
output_prefix = os.path.join(dirs.OUTPUT, prefix)
output_suffix = conversion_utils.parse_output_suffix(input_fnames)

# --- Create PyReshaper specifier object ---------------------------------------
specifier = specification.create_specifier()

# Define specifier input needed perform the conversion
specifier.input_file_list = input_files
specifier.netcdf_format = "netcdf4"
specifier.compression_level = 1
specifier.output_file_prefix = output_prefix
specifier.output_file_suffix = output_suffix
specifier.time_variant_metadata = ["time", "time_bounds"]
# specifier.exclude_list = ['HKSAT','ZLAKE']

# Create the PyReshaper object
rshpr = reshaper.create_reshaper(specifier,
                                 serial=False,
                                 verbosity=1,
                                 wmode='s')

# --- Run the conversion (slice-to-series) process -----------------------------
rshpr.convert()

# --- Print timing diagnostics -------------------------------------------------
rshpr.print_diagnostics()