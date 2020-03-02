"""
Rename CESM timeseries files to conform to the format that the 
e3sm_to_cmip package expects for input files

Usage
------
python rename-cesm-ts.py /path/to/dir

Matt Nicholson
2 Mar 2020
"""
import argparse
import os
import re


def init_parser():
    """
    Initialize a command line argument parser and parse the args
    
    Params
    -------
    None
    
    Returns
    --------
    args : Parsed argparse ArgumentParser object
    
    Arguments
    ----------
    positional str
        Directory that holds the files we went to rename
    """
    parse_desc = """Rename CESM timeseries files to conform the expected e3sm_to_cmip
    input file format."""
    
    parser = argparse.ArgumentParser(description=parse_desc)
    
    parser.add_argument(metavar='input_dir', dest='input_dir', action='store',
                        type='str', help='Path of the directory holding the files to rename')
    args = parser.parse_args()
    return args
    
    
def fetch_files(dir):
    """
    Get a list of files in the specified directory
    
    Params
    -------
    dir : str
        Path of the directory holding the files to rename
        
    Returns
    --------
    list of str
        List of filenames
    """
    pattern = re.compile(r'^\w+\.cam\.\w+\.\d{6}-\d{6}\.nc$')
    files = [f for f in os.listdir(dir) if pattern.match(f) and os.path.isfile(os.path.join(dir, f))]
    print('{} files found in {}'.format(len(files), dir))
    return files
    
    
def rename_files(dir, files)
    """
    Rename files to conform to e3sm_to_cmip input filename format
    
    Params
    -------
    dir : str
        Path of the directory that holds the files to rename
    files : list of str
        List of filenames in the directory that need to be renamed
        
    Returns
    --------
    list of str
        List of paths of renamed files
    """
    def _rename_file(dir, fname):
        f_old = os.path.join(dir, fname)
        splits = fname.split('.')
        splits[3] = splits[3].replace('-', '_')
        fname_new = '_'.join(splits[:-1])
        fname_new = fname_new + '.nc'
        print('{} --> {}'.format(fname, fname_new))
        f_new = os.path.join(dir, fname_new)
        os.rename(f_old, f_new)
        return f_new
    new_fnames = [_rename_file(dir, f) for f in files]
    return new_fnames
    
    
def main():
    welcome = """
    ****************************************************************************
    ************ Renaming CESM Timeseries files for fun and profit! ************
    ****************************************************************************
    """
    args  = init_parser()
    files = fetch_files(args.dir)
    rename_files(args.dir, files)
    

if __name__ == '__main__':
    main()
    
    