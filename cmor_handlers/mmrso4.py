"""
e3sm_to_cmip cmor handler script

Handler for Mass Mixing Ration of SO4 (mmrso4)

Matt Nicholson
17 Mar 2020
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cmor
from e3sm_to_cmip.lib import handle_variables

# list of raw variable names needed
RAW_VARIABLES = ['so4_a1', 'so4_a2', 'so4_a3',
                 'so4_c1', 'so4_c2', 'so4_c3']
VAR_NAME = 'mmrso4'
VAR_UNITS = 'kg kg-1'
TABLE = 'CMIP6_AERmon.json'
LEVELS = {
    'name' : 'lev',
    'units': 'hPa',
    'e3sm_axis_name': 'lev'
}


def write_data(varid, data, timeval, timebnds, index, **kwargs):
    """
    mmrso4 = so4_a1 + so4_a2 + so4_a3 + so4_c1 + so4_c2 + so4_c3
    """
    outdata = data['so4_a1'][index, :] + data['so4_a2'][index, :] +
              data['so4_a3'][index, :] + data['so4_c1'][index, :] +
              data['so4_c2'][index, :] + data['so4_c3'][index, :]
    
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