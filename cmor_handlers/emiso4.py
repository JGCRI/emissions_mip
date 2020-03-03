"""
e3sm_to_cmip cmor handler script

Handler for Total Direct Emission Rate of SO4 (emiso4)

Input Variable(s)
------------------
* SFso4_a1    : Surface flux of so4_a1, in kg m-2 s-1
* SFso4_a2    : Surface flux of so4_a2, in kg m-2 s-1
* SFso4_a3    : Surface flux of so4_a3, in kg m-2 s-1
* so4_a1_CLXF : Vertically intergrated external forcing for so4_a1, in molec cm-2 s-1
* so4_a2_CLXF : Vertically intergrated external forcing for so4_a2, in molec cm-2 s-1
* so4_a3_CLXF : Vertically intergrated external forcing for so4_a3, in molec cm-2 s-1

Matt Nicholson
3 Mar 2020
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cmor
from e3sm_to_cmip.lib import handle_variables

# list of raw variable names needed
RAW_VARIABLES = ['SFso4_a1', 'SFso4_a2', 'SFso4_a3',
                 'so4_a1_CLXF', 'so4_a2_CLXF', 'so4_a3_CLXF']
VAR_NAME = 'emiso4'
VAR_UNITS = 'kg m-2 s-1'
TABLE = str('CMIP6_AERmon.json')
LEVELS = {
    'name' : 'lev',
    'units': 'hPa',
    'e3sm_axis_name': 'lev'
}


def write_data(varid, data, timeval, timebnds, index, **kwargs):
    """
    emiso4 = SFso4_a1 + SFso4_a2 + SFso4_a3 + so4_a1_CLXF + so4_a2_CLXF + so4_a3_CLXF
    """
    outdata = data['SFso4_a1'][index, :]
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