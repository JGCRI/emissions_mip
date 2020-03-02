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
    input_files = sorted(input_files)
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
        raise ValueError('Unable to extract date from CESM history filename: {}'.format(fname))
    return ret_val

def fetch_fnames(dir, model_run, f_type):
    """
    Get a list of filenames of a specified type from a specified directory
    
    Params
    ------
    dir : str
        Path of the directory to look in
    model_run : str
        Model run that produced the history files. Ex: 'FAMIPC5'
    f_type : str
        Type of file to search for. Ex: 'cam', 'cice', 'clm2', etc
    """
    pattern = re.compile(r'^' + re.escape(model_run) + r'\.' + re.escape(f_type) + r'\.h0\.(\d{4}-\d{2})\.nc$')
    fnames = [f for f in os.listdir(dir) if pattern.match(f) and os.path.isfile(os.path.join(dir, f))]
    return sorted(fnames)
    