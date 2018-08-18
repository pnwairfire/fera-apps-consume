#-------------------------------------------------------------------------------
# Purpose:     Test new Consume consumption equations.
#               The general pattern is:
#                   - Run the new consumption function. Written 'test_<catagory>'
#                       Compare results to numbers from a spreadsheet Susan
#                       developed. Use loading totals 0.5, 1.5, and 3.0
#
# Author:      kjells
# Created:     1/6/2016
#-------------------------------------------------------------------------------
import unittest
import consume
import consume.con_calc_activity as cca
import helper
import numpy as np
import pandas as pd

class TestActivityEquations(unittest.TestCase):
            
    #test step function
    def test_calc_mb(self):                        
        ret = cca.calc_mb(1, "NFDRS-Th", 0, 0, 1, .6)
        self.assertEqual(5.07, ret)
        















