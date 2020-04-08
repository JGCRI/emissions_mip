"""
Tests Netcdf class

Matt Nicholson
7 April 2020
"""
import netCDF4
import sys
import unittest

import numpy as np

# Insert src directory to Python path for importing
sys.path.insert(1, '..')

import nc_file


class TestNCIO(unittest.TestCase):
    
    def setUp(self):
        self.nc_fname = 'dryso4_AERmon_GISS-E2-1-G_piClim-SO2_r1i1p5f103_gn_200001-201412.nc'
        self.nc_actual = netCDF4.Dataset(self.nc_fname, 'r')
        self.nc_vars = ['time', 'time_bnds', 'lat', 'lat_bnds', 
                        'lon', 'lon_bnds', 'dryso4']
        
    def test_basic_1(self):
        """File can be read into object.
        """
        nc = nc_file.Netcdf(self.nc_fname)
        self.assertTrue(isinstance(nc, nc_file.Netcdf))
        
    def test_basic_2(self):
        """Object has correct attributes & values.
        """
        nc = nc_file.Netcdf(self.nc_fname)
        test_vars = list(nc.variables.keys())
        self.assertEqual(nc.filename, self.nc_fname)
        self.assertTrue(np.array_equal(self.nc_vars, test_vars))
        self.assertEqual(self.nc_actual.source_id, nc.source_id)
        self.assertEqual(self.nc_actual.activity_id, nc.activity_id)
        self.assertEqual(self.nc_actual.mip_era, nc.mip_era)
        self.assertEqual(self.nc_actual.grid, nc.grid)
        self.assertEqual(self.nc_actual.grid_label, nc.grid_label)
        self.assertEqual(self.nc_actual.variable_id, nc.variable_id)
        
    def test_basic_3(self):
        """Object's variables are present & valid.
        """
        nc = nc_file.Netcdf(self.nc_fname)
        var_names = list(nc.variables.keys())
        self.assertEqual(var_names, self.nc_vars)
    
    def test_var_time(self):
        """Time variable is present and valid.
        """
        nc = nc_file.Netcdf(self.nc_fname)
        var_actual = self.nc_actual.variables['time']
        var_test   = nc.variables['time']
        self.assertEqual(var_actual.shape, var_test.shape)
        self.assertEqual(var_actual.bounds, var_test.bounds)
        self.assertEqual(var_actual.units, var_test.units)
        self.assertEqual(var_actual.long_name, var_test.long_name)
        self.assertEqual(var_actual.standard_name, var_test.standard_name)
        
    def test_var_lat_lon(self):
        """Lat & lon variables are present and valid.
        """
        nc = nc_file.Netcdf(self.nc_fname)
        for var in ['lat', 'lon']:
            var_actual = self.nc_actual.variables[var]
            var_test   = nc.variables[var]
            self.assertEqual(var_actual.shape, var_test.shape)
            self.assertEqual(var_actual.bounds, var_test.bounds)
            self.assertEqual(var_actual.units, var_test.units)
            self.assertEqual(var_actual.axis, var_test.axis)
            self.assertEqual(var_actual.long_name, var_test.long_name)
            self.assertEqual(var_actual.standard_name, var_test.standard_name)
    
    def test_var_dryso4(self):
        """DrySO4 variable (the variable we actually care about) is present and valid.
        """
        nc = nc_file.Netcdf(self.nc_fname)
        var_actual = self.nc_actual.variables['dryso4']
        var_test   = nc.variables['dryso4']
        self.assertEqual(var_actual.shape, var_test.shape)
        self.assertEqual(var_actual.units, var_test.units)
        self.assertEqual(var_actual.long_name, var_test.long_name)
        self.assertEqual(var_actual.standard_name, var_test.standard_name)
        
if __name__ == '__main__':
    unittest.main()