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
        self.path_colum_dryso4 = ('/pic/projects/GCAM/mnichol/emip/model-output/'
                                  'AerChemMIP/NASA-GISS/GISS-E2-1-G/piClim-SO2/'
                                  'r1i1p5f103/AERmon/dryso4/gn/v20191120')
        
    def test_get_var_path(self):
        """get_var_path() returns properly-constructed path.
        """
        test_path_1 = path_funcs.get_var_path('r1i1p5f103', 'drys04')
        test_path_1 = path_funcs.get_var_path('r1i1p5f104', 'drys04')
        self.assertEqual(test_path_1, self.path_colum_dryso4)
        self.assertEqual(test_path_2, self.path_colum_dryso4)
        
    def test_ensemble_lut(self)
        """ensemble_lut() returns correct metadata
        """
        ensembles = ['r1i1p5f101', 'r1i1p5f102', 'r1i1p5f103', 'r1i1p5f104']
        metadata = {'r1i1p5f101' : {'run' : 'base', 'wind_nudging' : False, 'seasonality' : True},
                    'r1i1p5f102' : {'run' : 'perturb', 'wind_nudging' : False, 'seasonality' : False},
                    'r1i1p5f103' : {'run' : 'perturb', 'wind_nudging' : True, 'seasonality' : False},
                    'r1i1p5f104' : {'run' : 'base', 'wind_nudging' : True, 'seasonality' : True}
                    }
        for ens in ensembles:
            test_meta = path_funcs.ensemble_lut(ens)
            self.assertEqual(test_meta, metadata[ens])
        
        
if __name__ == '__main__':
    unittest.main()