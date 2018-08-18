#-------------------------------------------------------------------------------
# Purpose:     Test Step Function calc_mb
#
# Author:      Brian Drye
# Created:     8/18/2018
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
        















