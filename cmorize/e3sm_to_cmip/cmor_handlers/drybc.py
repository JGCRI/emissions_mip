"""
e3sm_to_cmip cmor handler script

Handler for Dry Deposition Rate of BC (drybc)

Input Variable(s)
------------------
* bc_a1DDF : bc_a1 dry deposition flux at bottom (grav + turb), in kg m-2 s-1
* bc_a4DDF : bc_a4 dry deposition flux at bottom (grav + turb), in kg m-2 s-1
* bc_c1DDF : bc_c1 dry deposition flux at bottom (grav + turb), in kg m-2 s-1
* bc_c4DDF : bc_c4 dry deposition flux at bottom (grav + turb), in kg m-2 s-1

Matt Nicholson
3 Mar 2020
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cmor
from e3sm_to_cmip.lib import handle_variables

# list of raw variable names needed
RAW_VARIABLES = ['bc_a1DDF', 'bc_a4DDF',
                 'bc_c1DDF', 'bc_c4DDF']
VAR_NAME = 'drybc'
VAR_UNITS = 'kg m-2 s-1'
TABLE = 'CMIP6_AERmon.json'
LEVELS = {
    'name': 'lev',
    'units': 'hPa',
    'e3sm_axis_name': 'lev'
}


def write_data(varid, data, timeval, timebnds, index, **kwargs):
    """
    drybc = bc_a1DDF + bc_c1DDF + bc_a4DDF + bc_c4DDF
    """
    outdata = data['bc_a1DDF'][index, :] + data['bc_c1DDF'][index, :] + \
              data['bc_a4DDF'][index, :] + data['bc_c4DDF'][index, :]
        
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
        infiles (List): a list of strings of file names for the raw input data
        tables (str): path to CMOR tables
        user_input_path (str): path to user input json file
    Returns
    -------
        var name (str): the name of the processed variable after processing is complete
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