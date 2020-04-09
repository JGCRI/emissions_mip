"""
Tests functions in var_funcs.py

Matt Nicholson
9 April 2020
"""
import netCDF4
import sys
import unittest

import numpy as np

# Insert src directory to Python path for importing
sys.path.insert(1, '..')

import netcdf
import var_funcs


class TestNetcdf(unittest.TestCase):
    
    def setUp(self):
        self.nc_fname = 'dryso4_AERmon_GISS-E2-1-G_piClim-SO2_r1i1p5f103_gn_200001-201412.nc'
        # self.nc_actual = netCDF4.Dataset(self.nc_fname, 'r')
        self.netcdf_obj = netcdf.Netcdf(self.nc_fname)

    def test_chunk_var_annual_1(self):
            """
            Basic functionality.
            
            * 15 years are present.
            * Every element of the returned chunk list is a NumPy array.
            * Each chunked annual array has the shape (12, 90, 144).
            """
            nc  = self.netcdf_obj
            var = nc.get_var('dryso4')
            chunks = var_funcs.chunk_var_annual(nc, var)
            self.assertEqual(len(chunks), 15)
            self.assertTrue(all(isinstance(n, np.ndarray) for n in chunks))
            self.assertTrue(all(n.shape == (12, 90, 144) for n in chunks))
        
    def test_global_mean_monthly_1(self):
        """Basic functionality.
        """
        nc  = self.netcdf_obj
        var_name = 'dryso4'
        avgs = var_funcs.global_mean_monthly(nc, var_name)
        self.assertEqual(avgs.shape[0], nc.variables['time'].shape[0])
		
if __name__ == '__main__':
    unittest.main()