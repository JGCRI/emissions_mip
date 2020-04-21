"""
e3sm_to_cmip cmor handler script

Handler for Outgoing Solar Flux at TOA (rsut)

Matt Nicholson
18 Mar 2020
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cmor
from e3sm_to_cmip.lib import handle_variables

# list of raw variable names needed
RAW_VARIABLES = ['FSUTOA']
VAR_NAME = 'rsut'
VAR_UNITS = 'W m-2'
TABLE = 'CMIP6_AERmon.json'
LEVELS = {
    'name' : 'lev',
    'units': 'hPa',
    'e3sm_axis_name': 'lev'
}


def write_data(varid, data, timeval, timebnds, index, **kwargs):
    """
    rsut = FSUTOA
    """
    outdata = data['FSUTOA'][index, :]
    
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