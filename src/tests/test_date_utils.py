"""
Test functions in date_utils.py

Matt Nicholson
7 April 2020
"""
import netCDF4
import sys
import unittest

import numpy as np

# Insert src directory to Python path for importing
sys.path.insert(1, '..')

import date_utils
import netcdf
import testing_utils

class TestDateUtils(unittest.TestCase):
    
    def setUp(self):
        f_in = 'dryso4_AERmon_GISS-E2-1-G_piClim-SO2_r1i1p5f103_gn_200001-201412.nc'
        self.nc_file = netCDF4.Dataset(f_in, 'r')
        self.netcdf_obj = netcdf.Netcdf(f_in)
        
    def test_time_val_to_date_1(self):
        """
        Basic functionality
        
        * Various time variable value conversions.
        
        Notes
        -----
        The time variable values are days since 2000-01-01
        """
        time_var = self.nc_file.variables['time']
        time_val = 15.5
        test_date = date_utils.time_val_to_date(time_var, time_val)
        expected_date = '2000-01-16'
        self.assertEqual(test_date, expected_date)

        time_val = 45.0
        test_date = date_utils.time_val_to_date(time_var, time_val)
        expected_date = '2000-02-15'
        self.assertEqual(test_date, expected_date)

        time_val = 500.5
        test_date = date_utils.time_val_to_date(time_var, time_val)
        expected_date = '2001-05-15'
        self.assertEqual(test_date, expected_date)

        time_val = 5033.5
        test_date = date_utils.time_val_to_date(time_var, time_val)
        expected_date = '2013-10-12'
        self.assertEqual(test_date, expected_date)
        
    def test_date_to_time_val_1(self):
        """
        Basic functionality
        
        * Various date to time variable value conversions.
        """
        time_var = self.nc_file.variables['time']
        date = '2000-1-1'
        test_val = date_utils.date_to_time_val(time_var, date)
        expected_val = 15.5
        self.assertEqual(test_val, expected_val)

        date = '2002-06-15'
        test_val = date_utils.date_to_time_val(time_var, date)
        expected_val = 896.0
        self.assertEqual(test_val, expected_val)

        date = '2008-12-06'
        test_val = date_utils.date_to_time_val(time_var, date)
        expected_val = 3269.5
        self.assertEqual(test_val, expected_val)
        
    def test_time_var_to_dates_1(self):
        """
        Basic functionality
        
        * Various time variable array to dates array conversions.
        """
        time_var = self.nc_file.variables['time']
        test_dates = date_utils.time_var_to_dates(time_var)
        self.assertTrue(np.array_equal(time_var[:], testing_utils.test_utils.TIME_VALS))
        self.assertTrue(np.array_equal(test_dates, testing_utils.test_utils.DATES))
        
        
if __name__ == '__main__':
    unittest.main()