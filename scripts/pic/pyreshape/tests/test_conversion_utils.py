"""
Test functions in conversion_utils.py
"""
import unittest
import sys
import re

sys.path.insert(1, '..')

import conversion_utils
import testing_utils

class TestConversionUtils(unittest.TestCase):
    
    def setUp(self):
        self.model_run      = 'FAMIPC5'
        self.f_type         = 'cam'
        self.famipc5_fnames = self.fetch_fnames(testing_utils.read_famipc_fnames())
    # --------------------------------------------------------------------------
    
    def fetch_fnames(self, fnames):
        """
        Mimic conversion_utils.fetch_fnames() to filter non-netCDF files
        """
        MODEL  = self.model_run
        F_TYPE = self.f_type
        pattern = re.compile(r'^' + re.escape(MODEL) + r'\.' + re.escape(F_TYPE) + r'\.h0\.(\d{4}-\d{2})\.nc$')
        filtered_names = [f for f in fnames if pattern.match(f)]
        return filtered_names
    # --------------------------------------------------------------------------

    def test_fetch_fnames_1(self):
        """
        fetch_fnames only returns FAMIPC5 history filenames
        """
        self.assertEqual(len(self.famipc5_fnames), 192)
    # --------------------------------------------------------------------------
        
    def test_parse_file_date(self):
        """
        fetch_fnames only returns FAMIPC5 history filenames
        """
        first_date = conversion_utils.parse_file_date(self.famipc5_fnames[0])
        last_date  = conversion_utils.parse_file_date(self.famipc5_fnames[-1])
        self.assertEqual(first_date, '1999-01')
        self.assertEqual(last_date, '2014-12')
    # --------------------------------------------------------------------------
     
    def test_parse_output_suffix(self):
        """
        parse_output_suffix returns the correct output file suffix
        """
        suffix = conversion_utils.parse_output_suffix(self.famipc5_fnames)
        self.assertEqual(suffix, '.199901-201412.nc')
    # --------------------------------------------------------------------------
    
if __name__ == '__main__':
    unittest.main()