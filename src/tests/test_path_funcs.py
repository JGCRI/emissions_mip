"""
Tests functions in path_funcs.py.

Matt Nicholson
8 April 2020
"""
import sys
import unittest

import numpy as np

# Insert src directory to Python path for importing
sys.path.insert(1, '..')

import path_funcs


class TestPathFuncs(unittest.TestCase):
    
    def setUp(self):
        self.path_colum_dryso4 = ('/pic/projects/GCAM/mnichol/emip/columbia/'
                                  'gpfsm/dnb53/projects/p117/pub/CMIP6/AerChemMIP/'
                                  'NASA-GISS/GISS-E2-1-G/piClim-SO2/r1i1p5f103/'
                                  'AERmon/dryso4/gn/v20191120')
        
    def test_get_var_path(self):
        """get_var_path() returns properly-constructed path.
        """
        test_path_1 = path_funcs.get_var_path('columbia', 'drys04', 103)
        test_path_1 = path_funcs.get_var_path('columbia', 'drys04', 104)
        self.assertEqual(test_path_1, self.path_colum_dryso4)
        self.assertEqual(test_path_2, self.path_colum_dryso4)
        
        
if __name__ == '__main__':
    unittest.main()