"""
Rename CESM timeseries files to conform to the format that the 
e3sm_to_cmip package expects for input files.

e3sm_to_cmip input file format: {e3sm_var}_YYYYMM_YYYYMM.nc

Usage
------
python rename-cesm-ts.py /path/to/dir

Matt Nicholson
2 Mar 2020
"""
import os
import sys
import re
    
    
def fetch_files(in_dir):
    """
    Get a list of files in the specified directory
    
    Params
    -------
    in_dir : str
        Path of the directory holding the files to rename
        
    Returns
    --------
    list of str
        List of filenames
    """
    pattern = re.compile(r'^\w+\.cam\.\w+\.\d{6}-\d{6}\.nc$')
    files = [f for f in os.listdir(in_dir) if pattern.match(f)
             and os.path.isfile(os.path.join(in_dir, f))]
    print('{} files found in {}'.format(len(files), in_dir))
    return files
    
    
def rename_files(in_dir, files)
    """
    Rename files to conform to e3sm_to_cmip input filename format
    
    Params
    -------
    in_dir : str
        Path of the directory that holds the files to rename
    files : list of str
        List of filenames in the directory that need to be renamed
        
    Returns
    --------
    list of str
        List of paths of renamed files
    """
    def _rename_file(in_dir, fname):
        fname_old = os.path.join(in_dir, fname)
        splits = fname.split('.')
        splits[3] = splits[3].replace('-', '_')
        fname_new = '{}_{}.nc'.format(splits[2], splits[3].replace('-', '_'))
        print('{} --> {}'.format(fname, fname_new))
        fname_new = os.path.join(in_dir, fname_new)
        os.rename(fname_old, fname_new)
        return fname_new
    new_fnames = [_rename_file(in_dir, f) for f in files]
    return new_fnames
    

if __name__ == '__main__':
    welcome = """
    ****************************************************************************\n
    ************ Renaming CESM Timeseries files for fun and profit! ************\n
    ****************************************************************************\n
    """
    print(welcome)
    input_dir = sys.argv[1]
    files = fetch_files(input_dir)
    rename_files(input_dir, files)
    
    