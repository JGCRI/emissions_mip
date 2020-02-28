"""
Utility functions for converting CESM time-slice output files to time-series

Matt Nicholson
28 Feb 2020
"""
import os
import re

def parse_output_suffix(input_files):
    """
    Given a list of input files, create the output file suffix
    
    Ex: 
        input_files   = ['FAMIPC5.cam.h0.2010-09.nc', 'FAMIPC5.cam.h0.2010-10.nc']
        output_suffix = '201009-201010.nc'
    
    Params
    -------
    input_files : list of str
        List of input time-slice files to convert
    
    Return
    -------
    str
    """
    d_first = parse_file_date(input_files[0])
    d_first = d_first.replace('-', '')
    d_last  = parse_file_date(input_files[-1])
    d_last  = d_last.replace('-', '')
    ret_val = '.{}-{}.nc'.format(d_first, d_last)
    return ret_val

def parse_file_date(fname):
    """
    Extract the date from a CESM history file filename. Fails if unable to extract
    the date from the filename.
    
    Params
    -------
    fname : str
        CESM history filename
    
    Return
    -------
    str
        Date corresponding to the CESM history file in the format YYYYMM
    """
    pattern = r'\.(\d{4}-\d{2})\.nc'
    match = re.search(pattern, fname)
    if (match):
        ret_val = match.group(1)
    else:
        raise ValueError('Unable to extract date from CESM history filename')
    return ret_val
        