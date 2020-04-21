"""
e3sm_to_cmip cmor handler script

Handler for Wet Deposition Rate of Sea Salt (wetss)

Matt Nicholson
20 Mar 2020
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cmor
from e3sm_to_cmip.lib import handle_variables

# list of raw variable names needed
RAW_VARIABLES = ['ncl_a1SFWET', 'ncl_a2SFWET', 'ncl_a3SFWET',
                 'ncl_c1SFWET', 'ncl_c2SFWET', 'ncl_c3SFWET']
VAR_NAME = 'wetso4'
VAR_UNITS = 'kg m-2 s-1'
TABLE = 'CMIP6_AERmon.json'
LEVELS = {
    'name': 'lev',
    'units': 'hPa',
    'e3sm_axis_name': 'lev'
}


def write_data(varid, data, timeval, timebnds, index, **kwargs):
    """
    wetso4 = ncl_a1SFWET + ncl_a2SFWET + ncl_a3SFWET + ncl_c1SFWET +
             ncl_c2SFWET + ncl_c3SFWET
    """
    outdata = data['ncl_a1SFWET'][index, :] + data['ncl_a2SFWET'][index, :] + \
              data['ncl_a3SFWET'][index, :] + data['ncl_c1SFWET'][index, :] + \
              data['ncl_c2SFWET'][index, :] + data['ncl_c3SFWET'][index, :]
        
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