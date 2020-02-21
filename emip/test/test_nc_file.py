"""
Test the functionality of NCFile & NCVar objects

Matt Nicholson
21 Feb 2020
"""
import unittest
import sys

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import nc_file


class TestNCFile(unittest.TestCase):
    
    def setUp(self):
        # Vars needed for initialization
        self.f_in = r"C:\Users\nich980\data\emip\model-output\FAMIPC5\FAMIPC5.cam.h0.2010-07.nc"
        self.vars = ['so4_a1', 'so4_a2', 'SFso4_a1', 'SFso4_a2']
        self.nc_file = nc_file.NCFile(self.f_in, self.vars)
        
    def test_NCFile_1(self):
        """NCFile constructor returns an NCFile obj
        """
        repr_str = "<NCFile object - FAMIPC5.cam.h0.2010-07.nc>"
        self.assertEqual(repr(self.nc_file), repr_str)
    # --------------------------------------------------------------------------
    
    def test_NCFile_2(self):
        """NCFile contains the correct variables and they were properly 
        initialized
        """
        self.assertEqual(self.vars, list(self.nc_file.nc_vars.keys()))
        for var, var_obj in self.nc_file.nc_vars.items():
            repr_str = "<NCVar object - {}-{}>".format(var_obj.parent, var_obj.name)
            self.assertEqual(repr(var_obj), repr_str)
    # --------------------------------------------------------------------------
    
    def test_NCfile_3(self):
        """NCFile contains the correct variables and they were properly 
        initialized
        """
        # --- Test variable: so4_a1
        nc_var = self.nc_file.nc_vars['so4_a1']
        self.assertEqual(nc_var.get_name_long(), 'so4_a1 concentration')
        self.assertEqual(nc_var.get_units(), 'kg/kg')
        self.assertEqual(nc_var.get_shape(), (1, 30, 96, 144))
        self.assertEqual(nc_var.get_data().shape, nc_var.get_shape())
        # --- Test variable: so4_a2
        nc_var = self.nc_file.nc_vars['so4_a2']
        self.assertEqual(nc_var.get_name_long(), 'so4_a2 concentration')
        self.assertEqual(nc_var.get_units(), 'kg/kg')
        self.assertEqual(nc_var.get_shape(), (1, 30, 96, 144))
        self.assertEqual(nc_var.get_data().shape, nc_var.get_shape())
        # --- Test variable: SFso4_a1
        nc_var = self.nc_file.nc_vars['SFso4_a1']
        self.assertEqual(nc_var.get_name_long(), 'so4_a1 surface flux')
        self.assertEqual(nc_var.get_units(), 'kg/m2/s')
        self.assertEqual(nc_var.get_shape(), (1, 96, 144))
        self.assertEqual(nc_var.get_data().shape, nc_var.get_shape())
        # --- Test variable: SFso4_a2
        nc_var = self.nc_file.nc_vars['SFso4_a2']
        self.assertEqual(nc_var.get_name_long(), 'so4_a2 surface flux')
        self.assertEqual(nc_var.get_units(), 'kg/m2/s')
        self.assertEqual(nc_var.get_shape(), (1, 96, 144))
        self.assertEqual(nc_var.get_data().shape, nc_var.get_shape())
    # --------------------------------------------------------------------------
        
        
   
        
# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()
