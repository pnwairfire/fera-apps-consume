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
import consume.con_calc_natural as ccn
import helper
import numpy as np

CVT_MGHA = 0.44609
def to_mgha(tons):
    return tons / CVT_MGHA

def to_tons(mgha):
    return mgha * CVT_MGHA
    
def print_test_name(name):
    print('\n^^^^^^^^^^^^^^^^^^^\n{}'.format(name))

class TestNaturalEquations(unittest.TestCase):

    def setUp(self):
        loadings_file = helper.get_test_loadingsfile()
        self.fc = consume.FuelConsumption(fccs_file=loadings_file)
        self.fc.burn_type = 'natural'
        self.fc.load_scenario(load_file=helper.get_test_inputfile())
        self._loadings = self.fc._get_loadings_for_specified_files(self.fc._settings.get('fuelbeds'))

        # Setup ecoregion masks for equations that vary by ecoregion
        self._ecodict = {"maskb": {"boreal": 1, "western": 0, "southern": 0},
                   "masks": {"boreal": 0, "western": 0, "southern": 1},
                   "maskw": {"boreal": 0, "western": 1, "southern": 0}}

        print('---')
        print('\t'.join(self.fc._settings.get('ecoregion')))

        ecoregion = self.fc._settings.get('ecoregion')
        self._ecob_mask = [self._ecodict["maskb"][e] for e in ecoregion]
        self._ecos_mask = [self._ecodict["masks"][e] for e in ecoregion]
        self._ecow_mask = [self._ecodict["maskw"][e] for e in ecoregion]
        self._ecoregion_masks = {
            'boreal': self._ecob_mask,
            'southern': self._ecos_mask,
            'western': self._ecow_mask}

    def tearDown(self):
        pass

    def extract_shrub_herb_totals(self, ret):
        print('\nType: {}'.format(type(ret)))
        totals = np.zeros_like(ret[0][:, ][3])
        for i, v in enumerate(ret):
            totals += v[:, ][3]
        print('\n{}'.format(totals))
        return totals
        
    def test_herb_calc(self): 
        print_test_name('test_herb_calc')
        ret = ccn.herb_calc(self._loadings, self._ecoregion_masks)
        totals = self.extract_shrub_herb_totals(ret)
        print(totals)
        self.assertEqual(9, len(totals))
        self.assertAlmostEqual(0.93, totals[0], places=2)    # western
        self.assertAlmostEqual(2.91, totals[1], places=2)    # southern
        self.assertAlmostEqual(2.78, totals[2], places=2)    # western (boreal)
        self.assertAlmostEqual(5.56, totals[3], places=2)    # western
        self.assertAlmostEqual(0.97, totals[4], places=2)    # southern
        self.assertAlmostEqual(5.56, totals[5], places=2)    # western (boreal)
        self.assertAlmostEqual(0.0, totals[6], places=2)    # western
        self.assertAlmostEqual(0.0, totals[7], places=2)    # southern
        self.assertAlmostEqual(0.0, totals[8], places=2)    # western (boreal)

    '''
    def test_shrub_calc(self):
        def western(loading, percent_black, season=0):
            # ks - replace with values from Susan's spreadsheet
            tmp =  0.1102 + 0.1139*to_mgha(loading) + 1.9647*percent_black - 0.3296*season
            return to_tons(tmp**tmp)

        def southern(loading, season):
            # ks - replace with values from Susan's spreadsheet
            log_loading = np.log(to_mgha(loading))
            tmp = -0.1889 + 0.9049*log_loading + 0.0676*season
            return to_tons(np.e**tmp)

        print_test_name('test_shrub_calc')
        shrub_black_pct = 0.8
        ret = ccn.shrub_calc(shrub_black_pct, self._loadings, self._ecoregion_masks)
        totals = self.extract_shrub_herb_totals(ret)
        print(totals)

        self.assertAlmostEqual(0.86, totals[0], places=2)
        self.assertAlmostEqual(southern(3, 0), totals[1], places=4)
        self.assertAlmostEqual(western(3, shrub_black_pct), totals[2], places=4)
        self.assertAlmostEqual(western(6, shrub_black_pct), totals[3], places=4)
        self.assertAlmostEqual(0.77, totals[4], places=2)
        self.assertAlmostEqual(western(6, shrub_black_pct), totals[5], places=4)
        self.assertAlmostEqual(0.0, totals[6], places=4)
        self.assertAlmostEqual(0.0, totals[7], places=4)
        self.assertAlmostEqual(0.0, totals[8], places=4)
    '''

    def test_sound_one_calc(self): 
        ret = ccn.sound_one_calc(self._loadings, self._ecos_mask)
        print_test_name('test_sound_one_calc')
        print(ret[3])  # print totals
        totals = ret[3]
        self.assertEqual(9, len(totals))
        self.assertAlmostEqual(0.4235, totals[0], places=2)
        self.assertAlmostEqual(1.24, totals[1], places=2)
        self.assertAlmostEqual(1.27, totals[2], places=2)
        self.assertAlmostEqual(2.54, totals[3], places=2)
        self.assertAlmostEqual(0.41, totals[4], places=2)
        self.assertAlmostEqual(2.54, totals[5], places=2)
        self.assertAlmostEqual(0.0, totals[6], places=2)
        self.assertAlmostEqual(0.0, totals[7], places=2)
        self.assertAlmostEqual(0.0, totals[8], places=2)

    def test_sound_ten_calc(self): 
        print_test_name('test_sound_ten_calc')  # print totals
        ret = ccn.sound_ten_calc(self._loadings, self._ecos_mask)
        print(ret[3])  # print totals
        totals = ret[3]
        self.assertEqual(9, len(totals))
        self.assertAlmostEqual(0.42, totals[0], places=2)
        self.assertAlmostEqual(0.56, totals[1], places=2)
        self.assertAlmostEqual(1.27, totals[2], places=2)
        self.assertAlmostEqual(2.54, totals[3], places=2)
        self.assertAlmostEqual(0.19, totals[4], places=2)
        self.assertAlmostEqual(2.54, totals[5], places=2)
        self.assertAlmostEqual(0.0, totals[6], places=2)
        self.assertAlmostEqual(0.0, totals[7], places=2)
        self.assertAlmostEqual(0.0, totals[8], places=2)

    def test_sound_hundred_calc(self): 
        print_test_name('test_sound_hundred_calc')  # print totals
        ret = ccn.sound_hundred_calc(self._loadings, self._ecos_mask)
        print(ret[3])  # print totals
        totals = ret[3]
        self.assertEqual(9, len(totals))
        self.assertAlmostEqual(0.36, totals[0], places=2)
        self.assertAlmostEqual(0.86, totals[1], places=2)
        self.assertAlmostEqual(1.07, totals[2], places=2)
        self.assertAlmostEqual(2.14, totals[3], places=2)
        self.assertAlmostEqual(0.29, totals[4], places=2)
        self.assertAlmostEqual(2.14, totals[5], places=2)
        self.assertAlmostEqual(0.0, totals[6], places=2)
        self.assertAlmostEqual(0.0, totals[7], places=2)
        self.assertAlmostEqual(0.0, totals[8], places=2)

    def test_sound_large_wood_calc(self):  
        print_test_name('test_sound_large_wood')
        eq = lambda load, fm: (2.735 + load*0.3285 + fm*-0.0457)[0]
        ret = ccn.sound_large_wood_calc(self._loadings, self.fc.fuel_moisture_1000hr_pct, self._ecos_mask)
        print(ret[3])  # print totals
        totals = ret[3]
        self.assertEqual(9, len(totals))
        self.assertAlmostEqual(eq(1.5, self.fc.fuel_moisture_1000hr_pct), totals[0], places=4)
        self.assertAlmostEqual(eq(4.5, self.fc.fuel_moisture_1000hr_pct), totals[1], places=4)
        self.assertAlmostEqual(eq(4.5, self.fc.fuel_moisture_1000hr_pct), totals[2], places=4)
        self.assertAlmostEqual(eq(9.0, self.fc.fuel_moisture_1000hr_pct), totals[3], places=4)
        self.assertAlmostEqual(eq(1.5, self.fc.fuel_moisture_1000hr_pct), totals[4], places=4)
        self.assertAlmostEqual(eq(9.0, self.fc.fuel_moisture_1000hr_pct), totals[5], places=4)
        self.assertAlmostEqual(eq(0.0, self.fc.fuel_moisture_1000hr_pct), totals[6], places=4)
        self.assertAlmostEqual(eq(0.0, self.fc.fuel_moisture_1000hr_pct), totals[7], places=4)
        self.assertAlmostEqual(eq(0.0, self.fc.fuel_moisture_1000hr_pct), totals[8], places=4)

    def test_rotten_large_wood_calc(self):  
        print_test_name('test_rotten_large_wood')
        
        def calc(load, fm):
            ret = (1.9024 + load*0.4933 + fm*-0.0338)[0]
            return ret if ret > 0 else 0
            
        ret = ccn.rotten_large_wood_calc(self._loadings, self.fc.fuel_moisture_1000hr_pct, self._ecos_mask)
        print(ret[3])  # print totals
        totals = ret[3]
        self.assertEqual(9, len(totals))
        self.assertAlmostEqual(calc(0, self.fc.fuel_moisture_1000hr_pct), totals[0], places=4)
        self.assertAlmostEqual(calc(4.5, self.fc.fuel_moisture_1000hr_pct), totals[1], places=4)
        self.assertAlmostEqual(calc(4.5, self.fc.fuel_moisture_1000hr_pct), totals[2], places=4)
        self.assertAlmostEqual(calc(9.0, self.fc.fuel_moisture_1000hr_pct), totals[3], places=4)
        self.assertAlmostEqual(calc(0, self.fc.fuel_moisture_1000hr_pct), totals[4], places=4)
        self.assertAlmostEqual(calc(9.0, self.fc.fuel_moisture_1000hr_pct), totals[5], places=4)
        self.assertAlmostEqual(calc(0.0, self.fc.fuel_moisture_1000hr_pct), totals[6], places=4)
        self.assertAlmostEqual(calc(0.0, self.fc.fuel_moisture_1000hr_pct), totals[7], places=4)
        self.assertAlmostEqual(calc(0.0, self.fc.fuel_moisture_1000hr_pct), totals[8], places=4)

    def test_litter_calc(self):
        #
        # NOTE: loadings are 1,3, and 5 for these catagories
        #
        print_test_name('test_litter_calc')
        FM_DUFF = 30
        print(self._ecoregion_masks)
        print(self._loadings['litter_loading'])
        
        fm_from_file = self.fc.fuel_moisture_duff_pct
        self.fc.fuel_moisture_duff_pct = FM_DUFF
        
        ret = ccn.litter_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_1000hr_pct, self._ecoregion_masks)
        print(ret)  # print totals
        self.assertEqual(9, len(ret))
        self.assertAlmostEqual(0.59, ret[0], places=2)
        #self.assertAlmostEqual(1.78, ret[1], places=2)
        self.assertAlmostEqual(2.56, ret[2], places=2)
        self.assertAlmostEqual(3.31, ret[3], places=2)
        self.assertAlmostEqual(0.59, ret[4], places=2)
        self.assertAlmostEqual(4.52, ret[5], places=2)
        self.assertAlmostEqual(0.0, ret[6], places=2)
        self.assertAlmostEqual(0.0, ret[7], places=2)
        self.assertAlmostEqual(0.0, ret[8], places=2)

        self.fc.fuel_moisture_duff_pct = fm_from_file

    def test_duff_calc(self):
        #
        # NOTE: loadings are 0.5, 10, and 150 (for each lower, upper duff so 1, 20, 300 for total duff load)
        #
        print_test_name('test_duff_calc')
        FM_DUFF = 30
        print(self._ecoregion_masks)
        print(self._loadings['duff_upper_loading'])
        
        fm_from_file = self.fc.fuel_moisture_duff_pct
        self.fc.fuel_moisture_duff_pct = FM_DUFF
        
        ret = ccn.duff_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_1000hr_pct, self._ecoregion_masks)
        print(ret)  # print totals
        self.assertEqual(9, len(ret))
        #self.assertAlmostEqual(-0.65, ret[0], places=2)
        self.assertAlmostEqual(0, ret[0], places=2)
        self.assertAlmostEqual(1.96, ret[1], places=2)
        self.assertAlmostEqual(11.62, ret[2], places=2)
        self.assertAlmostEqual(192.38, ret[3], places=2)
        self.assertAlmostEqual(0.63, ret[4], places=2)
        self.assertAlmostEqual(192.38, ret[5], places=2)
        self.assertAlmostEqual(0.0, ret[6], places=2)
        self.assertAlmostEqual(0.0, ret[7], places=2)
        self.assertAlmostEqual(0.0, ret[8], places=2)

        self.fc.fuel_moisture_duff_pct = fm_from_file

















