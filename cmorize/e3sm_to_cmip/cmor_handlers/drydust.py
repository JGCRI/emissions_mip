"""
e3sm_to_cmip cmor handler script

Handler for Dry Deposition Rate of Dust (drydust)

Matt Nicholson
3 Mar 2020
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cmor
from e3sm_to_cmip.lib import handle_variables

# list of raw variable names needed
RAW_VARIABLES = ['dst_a1DDF', 'dst_a3DDF',
                 'dst_c1DDF', 'dst_c3DDF']
VAR_NAME = 'drydust'
VAR_UNITS = 'kg m-2 s-1'
TABLE = 'CMIP6_AERmon.json'
LEVELS = {
    'name': 'lev',
    'units': 'hPa',
    'e3sm_axis_name': 'lev'
}


def write_data(varid, data, timeval, timebnds, index, **kwargs):
    """
    drydust = dst_a1DDF + dst_a3DDF + dst_c1DDF + dst_c3DDF
    """
    outdata = data['dst_a1DDF'][index, :] + data['dst_a3DDF'][index, :] + \
              data['dst_c1DDF'][index, :] + data['dst_c3DDF'][index, :]
        
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