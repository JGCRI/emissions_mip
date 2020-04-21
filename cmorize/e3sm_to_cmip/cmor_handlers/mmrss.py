"""
e3sm_to_cmip cmor handler script

Handler for Mass Mixing Ration of Sea Salt (mmrss)

Matt Nicholson
17 Mar 2020
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cmor
from e3sm_to_cmip.lib import handle_variables

# list of raw variable names needed
RAW_VARIABLES = ['ncl_a1', 'ncl_a2', 'ncl_a3',
                 'ncl_c1', 'ncl_c2', 'ncl_c3']
VAR_NAME = 'mmrss'
VAR_UNITS = 'kg kg-1'
TABLE = 'CMIP6_AERmon.json'
LEVELS = {
    'name' : 'lev',
    'units': 'hPa',
    'e3sm_axis_name': 'lev'
}


def write_data(varid, data, timeval, timebnds, index, **kwargs):
    """
    mmrss = ncl_a1 + ncl_a2 + ncl_a3 + ncl_c1 + ncl_c2 + ncl_c3
    """
    outdata = data['ncl_a1'][index, :] + data['ncl_a2'][index, :] + \
              data['ncl_a3'][index, :] + data['ncl_c1'][index, :] + \
              data['ncl_c2'][index, :] + data['ncl_c3'][index, :]
    
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