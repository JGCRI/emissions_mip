"""
e3sm_to_cmip cmor handler script

Handler for Dry Deposition Rate of Sea Salt (dryss)

Matt Nicholson
3 Mar 2020
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cmor
from e3sm_to_cmip.lib import handle_variables

# list of raw variable names needed
RAW_VARIABLES = ['ncl_a1DDF', 'ncl_a2DDF', 'ncl_a3DDF'
                 'ncl_c1DDF', 'ncl_c2DDF', 'ncl_c3DDF']
VAR_NAME = 'dryss'
VAR_UNITS = 'kg m-2 s-1'
TABLE = 'CMIP6_AERmon.json'
LEVELS = {
    'name': 'lev',
    'units': 'hPa',
    'e3sm_axis_name': 'lev'
}


def write_data(varid, data, timeval, timebnds, index, **kwargs):
    """
    dryss = ncl_a1DDF + ncl_a2DDF + ncl_a3DDF +
            ncl_c1DDF + ncl_c2DDF + ncl_c3DDF
    """
    outdata = data['ncl_a1DDF'][index, :] + data['ncl_a2DDF'][index, :] + \
              data['ncl_a3DDF'][index, :] + data['ncl_c1DDF'][index, :] + \
              data['ncl_c2DDF'][index, :] + data['ncl_c3DDF'][index, :]
        
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