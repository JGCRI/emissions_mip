"""
e3sm_to_cmip cmor handler script

Handler for Dry Deposition Rate of SO4 (dryso4)

Input Variable(s)
------------------
* so4_a1DDF : so4_a1 dry deposition flux at bottom (grav + turb), in kg m-2 s-1
* so4_c1DDF : so4_c1 dry deposition flux at bottom (grav + turb), in kg m-2 s-1
* so4_a2DDF : so4_a2 dry deposition flux at bottom (grav + turb), in kg m-2 s-1
* so4_c2DDF : so4_c2 dry deposition flux at bottom (grav + turb), in kg m-2 s-1
* so4_a3DDF : so4_a3 dry deposition flux at bottom (grav + turb), in kg m-2 s-1
* so4_c3DDF : so4_c3 dry deposition flux at bottom (grav + turb), in kg m-2 s-1

Matt Nicholson
3 Mar 2020
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cmor
from e3sm_to_cmip.lib import handle_variables

# list of raw variable names needed
RAW_VARIABLES = ['so4_a1DDF', 'so4_a2DDF', 'so4_a3DDF',
                 'so4_c1DDF', 'so4_c2DDF', 'so4_c3DDF']
VAR_NAME = 'dryso4'
VAR_UNITS = 'kg m-2 s-1'
TABLE = str('CMIP6_AERmon.json')
LEVELS = {
    'name' : 'lev',
    'units': 'hPa',
    'e3sm_axis_name': 'lev'
}


def write_data(varid, data, timeval, timebnds, index, **kwargs):
    """
    dryso4 = so4_a1DDF + so4_c1DDF + so4_a2DDF + so4_c2DDF + so4_a3DDF + so4_c3DDF
    """
    outdata = data['so4_a1DDF'][index, :]
    for var in RAW_VARIABLES[1:]:
        outdata = outdata + data[var][index, :]
        
    cmor.write(
        varid,
        outdata,
        time_vals=timeval,
        time_bnds=timebnds)
# ------------------------------------------------------------------


def handle(infiles, tables, user_input_path, **kwargs):
    """
    Parameters
    ----------
    infiles : list of str
        A list of strings of file names for the raw input data
    tables : str
        Path to CMOR tables
    user_input_path : str
        Path to user input json file
            
    Returns
    -------
    var name : str
        Name of the processed variable after processing is complete
    """
    return handle_variables(
        metadata_path=user_input_path,
        tables=tables,
        table=TABLE,
        infiles=infiles,
        raw_variables=RAW_VARIABLES,
        write_data=write_data,
        outvar_name=VAR_NAME,
        outvar_units=VAR_UNITS,
        serial=kwargs.get('serial'),
        levels=LEVELS,
        logdir=kwargs.get('logdir'))
# ------------------------------------------------------------------