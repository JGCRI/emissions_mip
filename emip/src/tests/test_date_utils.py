"""
Test functions in date_utils.py

Matt Nicholson
7 April 2020
"""
import unittest
import netCDF4
import sys
import os

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import date_utils

class TestCedsIO(unittest.TestCase):
    
    def setUp(self):
        f_in = 'dryso4_AERmon_GISS-E2-1-G_piClim-SO2_r1i1p5f103_gn_200001-201412.nc'
        self.nc_file = netCDF4.Dataset(f_in, 'r')
        
    def test_time_val_to_date_1(self):
        """Basic time_val_to_date functionality
        
        The time variable values are days since 2000-01-01
        """
        time_var = self.nc_file.variables['time']
        time_val = 15.5
        test_date = date_utils.time_val_to_date(time_var, test_val)
        expected_date = '2000-01-16'
        
        self.assertTrue(isinstance(test_date, str))
        self.assertEqual(test_date, expected_date)
        # ---
        time_val = 45.0
        test_date = date_utils.time_val_to_date(time_var, test_val)
        expected_date = '2000-02-15'
        
        self.assertTrue(isinstance(test_date, str))
        self.assertEqual(test_date, expected_date)
        # ---
        time_val = 500.5
        test_date = date_utils.time_val_to_date(time_var, test_val)
        expected_date = '2001-05-15'
        
        self.assertTrue(isinstance(test_date, str))
        self.assertEqual(test_date, expected_date)
        # ---
        time_val = 5033.5
        test_date = date_utils.time_val_to_date(time_var, test_val)
        expected_date = '2013-10-12'
        
        self.assertTrue(isinstance(test_date, str))
        self.assertEqual(test_date, expected_date)
        
        
if __name__ == '__main__':
    unittest.main()