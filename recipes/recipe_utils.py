"""
Utility functions for EMIP recipe scripts.

Matt Nicholson
12 April 2020
"""

def parse_name_str(name_str):
    """
    Parse/split a namestring into the institution and forcing index.
    
    Parameters
    ----------
    name_str : str
        Namestring to parse. Format: <institution>-<forcing_index>.
    
    Returns
    -------
    list of str : [institution, forcing_index]
    """
    return name_str.split('-')