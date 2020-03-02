"""
Testing utilities

Matt Nicholson
2 Mar 2020
"""

def read_famipc_fnames():
    """
    Return a sorted list of FAMIPC5 CESM history filenames
    """
    f_in = 'famipc5_hist_files.txt'
    with open(f_in, 'r') as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    return sorted(lines)