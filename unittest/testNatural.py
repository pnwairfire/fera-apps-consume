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
    
def bracket(load, cons):
    # ensure that results are between 0 and initial load value)
    return np.where(0 > cons, 0, np.where(cons > load, load, cons))
    
def my_print(stuff):
    pass
    #print(stuff)
    
class TestNaturalEquations(unittest.TestCase):

    def setUp(self):
        loadings_file = helper.get_test_loadingsfile()
        self.fc = consume.FuelConsumption(fccs_file=loadings_file)
        self.fc.burn_type = 'natural'
        input_file = helper.get_test_inputfile()
        # debug: my_print(' - Loading input from: {}'.format(input_file))
        self.fc.load_scenario(load_file=input_file)
        self._loadings = self.fc._get_loadings_for_specified_files(self.fc._settings.get('fuelbeds'))

        # Setup ecoregion masks for equations that vary by ecoregion
        self._ecodict = {"maskb": {"boreal": 1, "western": 0, "southern": 0},
                   "masks": {"boreal": 0, "western": 0, "southern": 1},
                   "maskw": {"boreal": 0, "western": 1, "southern": 0}}

        my_print('--- ecoregion settings')
        my_print('\t'.join(self.fc._settings.get('ecoregion')))

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
    
    def check_catagory(self, reference_values, calculated_values, num_places=2):
        self.assertEqual(len(reference_values), len(calculated_values))
        for idx, val in enumerate(reference_values):
            self.assertAlmostEqual(val, calculated_values[idx], places=num_places)
            
    def check_fsr(self, reference_values, calculated_values, num_places=2):
        for i in range(3):
            self.assertAlmostEqual(reference_values[i], calculated_values[i], num_places)

    def extract_shrub_herb_totals(self, ret):
        my_print('\nType: {}'.format(type(ret)))
        my_print(ret)
        totals = np.zeros_like(ret[0][:, ][3])
        for i, v in enumerate(ret):
            totals += v[:, ][3]
        return totals
        
    def test_herb_calc(self): 
        ret = ccn.herb_calc(self._loadings, self._ecoregion_masks)
        totals = self.extract_shrub_herb_totals(ret)
        my_print(totals)
        self.assertEqual(8, len(totals))
        self.check_catagory([0.93, 2.91, 2.78, 5.56, 0.97, 5.56, 0, 0], totals)

    def test_shrub_calc(self):
        ret = ccn.shrub_calc(self.fc.shrub_blackened_pct, self._loadings, self._ecoregion_masks, 0)
        totals = self.extract_shrub_herb_totals(ret)
        my_print(totals)
        self.check_catagory([1, 2.07, 2.67, 4.61, 0.77, 4.61, 0, 0], totals)

    def test_sound_one_calc(self): 
        ret = ccn.sound_one_calc(self._loadings, self._ecos_mask)
        my_print(ret[3])  # print totals
        totals = ret[3]
        self.assertEqual(8, len(totals))
        self.check_catagory([0.4235, 1.24, 1.27, 2.54, 0.41, 2.54, 0, 0], totals)
        self.check_fsr([2.41, 0.13, 0], ret[:,3])

    def test_sound_ten_calc(self): 
        ret = ccn.sound_ten_calc(self._loadings, self._ecos_mask)
        my_print(ret[3])  # print totals
        totals = ret[3]
        self.assertEqual(8, len(totals))
        self.check_catagory([0.42, 0.56, 1.27, 2.54, 0.19, 2.54, 0, 0], totals)
        self.check_fsr([2.29, 0.25, 0], ret[:,3])

    def test_sound_hundred_calc(self): 
        ret = ccn.sound_hundred_calc(self._loadings, self._ecos_mask)
        my_print(ret[3])  # print totals
        totals = ret[3]
        self.assertEqual(8, len(totals))
        self.check_catagory([0.36, 0.86, 1.07, 2.14, 0.29, 2.14, 0, 0], totals)
        self.check_fsr([1.82, 0.21, 0.11], ret[:,3])

    def test_sound_large_wood_calc(self):  
        # test loading amounts are (1,2,1) = 4, (3,6,3) = 12, (5,10,5) = 20
        TEST_FM = 50
        fm_from_file = self.fc.fuel_moisture_1000hr_pct
        self.fc.fuel_moisture_1000hr_pct = TEST_FM
        
        one_k, ten_k, tenk_plus = ccn.sound_large_wood_calc(self._loadings, self.fc.fuel_moisture_1000hr_pct)
        totals = one_k[3] + ten_k[3] + tenk_plus[3]
        my_print(totals)
        
        self.assertEqual(8, len(totals))
        self.check_catagory([1.51, 4.14, 4.14, 6.77, 1.51, 6.77, 0, 0], totals)

        one_k_totals = one_k[3]
        self.check_catagory([.58, 1.59, 1.59, 2.6, .58, 2.6, 0, 0], one_k_totals)
        self.check_fsr([1.56, .78, .26], one_k[:,3])
        
        ten_k_totals = ten_k[3]
        self.check_catagory([.7, 1.91, 1.91, 3.12, .7, 3.12, 0, 0], ten_k_totals)
        self.check_fsr([1.25, 1.25, .62], ten_k[:,3])
        
        tenk_plus_totals = tenk_plus[3]
        self.check_catagory([.23, .64, .64, 1.04, .23, 1.04, 0, 0], tenk_plus_totals)
        self.check_fsr([.21, .42, .42], tenk_plus[:,3])

        self.fc.fuel_moisture_1000hr_pct = fm_from_file
        

    def test_rotten_large_wood_calc(self):  
        # test loading amounts are (1,2,1) = 4, (3,6,3) = 12, (5,10,5) = 20
        TEST_FM = 50
        fm_from_file = self.fc.fuel_moisture_1000hr_pct
        self.fc.fuel_moisture_1000hr_pct = TEST_FM
        
        def calc(load, fm):
            ret = to_tons((1.9024 + to_mgha(load)*0.4933 + fm*-0.0338)[0])
            return bracket(load, ret)
            
        one_k, ten_k, tenk_plus = ccn.rotten_large_wood_calc(self._loadings, self.fc.fuel_moisture_1000hr_pct)
        totals = one_k[3] + ten_k[3] + tenk_plus[3]
        my_print(totals)  # print totals
        self.assertEqual(8, len(totals))
        self.check_catagory([2.07, 6.01, 6.01, 9.96, 2.07, 9.96, 0, 0], totals)

        one_k_totals = one_k[3]
        self.check_catagory([.73, 2.11, 2.11, 3.49, .73, 3.49, 0, 0], one_k_totals, num_places=1)
        self.check_fsr([2.09, 1.05, .35], one_k[:,3])

        ten_k_totals = ten_k[3]
        self.check_catagory([1.03, 3.01, 3.01, 4.98, 1.03, 4.98, 0, 0], ten_k_totals, num_places=1)

        tenk_plus_totals = tenk_plus[3]
        self.check_catagory([.31, .90, .90, 1.49, .31, 1.49, 0, 0], tenk_plus_totals, num_places=1)
        
        self.fc.fuel_moisture_1000hr_pct = fm_from_file

    def test_litter_calc(self):
        #
        # NOTE: loadings are 1,3, and 5 for these catagories
        #
        FM_DUFF = 30
        my_print(self._ecoregion_masks)
        my_print(self._loadings['litter_loading'])
        
        fm_from_file = self.fc.fuel_moisture_duff_pct
        self.fc.fuel_moisture_duff_pct = FM_DUFF
        
        ret = ccn.litter_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_1000hr_pct, self._ecoregion_masks)
        my_print(ret[3])  # print totals
        
        total = ret[3]
        self.assertEqual(8, len(total))
        self.check_catagory([0.59, 2.08, 2.56, 3.31, .69, 4.52, 0, 0], total)
        self.check_fsr([2.98, .33, 0], ret[:,3])

        self.fc.fuel_moisture_duff_pct = fm_from_file

    def test_lichen_calc(self):
        #
        # NOTE: loadings are 1,3, and 5 for these catagories
        #
        FM_DUFF = 30
        my_print(self._ecoregion_masks)
        my_print(self._loadings['lichen_loading'])
        
        fm_from_file = self.fc.fuel_moisture_duff_pct
        self.fc.fuel_moisture_duff_pct = FM_DUFF
        
        ret = ccn.lichen_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_1000hr_pct, self._ecoregion_masks)
        my_print(ret[3])  # print totals
        
        total = ret[3]
        self.assertEqual(8, len(total))
        self.check_catagory([0.59, 2.08, 2.56, 3.31, .69, 4.52, 0, 0], total)
        self.check_fsr([3.14, .17, 0], ret[:,3])

        self.fc.fuel_moisture_duff_pct = fm_from_file

    def test_moss_calc(self):
        #
        # NOTE: loadings are 1,3, and 5 for these catagories
        #
        FM_DUFF = 30
        my_print(self._ecoregion_masks)
        my_print(self._loadings['moss_loading'])
        
        fm_from_file = self.fc.fuel_moisture_duff_pct
        self.fc.fuel_moisture_duff_pct = FM_DUFF
        
        ret = ccn.moss_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_1000hr_pct, self._ecoregion_masks)
        my_print(ret[3])  # print totals
        
        total = ret[3]
        self.assertEqual(8, len(total))
        self.check_catagory([0.59, 2.08, 2.56, 3.31, .69, 4.52, 0, 0], total)
        self.check_fsr([3.14, .17, 0], ret[:,3])

        self.fc.fuel_moisture_duff_pct = fm_from_file

    def test_duff_calc(self):
        #
        # NOTE: loadings are 0.5, 10, and 150 (for each lower, upper duff so 1, 20, 300 for total duff load)
        #
        FM_DUFF = 30
        fm_from_file = self.fc.fuel_moisture_duff_pct
        self.fc.fuel_moisture_duff_pct = FM_DUFF
        
        cons_duff_upper, cons_duff_lower = ccn.duff_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_litter_pct, self._ecoregion_masks)
        total = cons_duff_upper[3] + cons_duff_lower[3]
        my_print(total)  # print totals
        self.assertEqual(8, len(total))
        self.check_catagory([0, 1.96, 11.62, 192.38, .63, 192.38, 0, 0], total)
        
        # upper duff
        total = cons_duff_upper[3]
        self.check_catagory([0, 1.96, 10.0, 150.0, 0.5, 150.0, 0, 0], total)
        self.check_fsr([2.05, 14.38, 4.11], cons_duff_upper[:,3])
        
        # lower duff
        total = cons_duff_lower[3]
        self.check_catagory([0, 0, 1.62, 42.38, 0.13, 42.38, 0, 0], total)

        self.fc.fuel_moisture_duff_pct = fm_from_file


    def test_basal_acc_calc(self):
        #
        # NOTE: loadings are 1, 5, 10 for these catagories
        #
        FM_DUFF = 30
        FM_LITTER = 10
        my_print(self._ecoregion_masks)
        my_print(self._loadings['bas_loading'])
        
        fm_duff_from_file = self.fc.fuel_moisture_duff_pct
        fm_litter_from_file = self.fc.fuel_moisture_litter_pct
        self.fc.fuel_moisture_duff_pct = FM_DUFF
        self.fc.fuel_moisture_litter_pct = FM_LITTER
        
        ret = ccn.basal_accumulation_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_litter_pct, self._ecoregion_masks)
        my_print(ret[3])  # print totals
        
        total = ret[3]
        self.assertEqual(8, len(total))
        self.check_catagory([0, .91, 1.93, 5.16, 0.63, 5.16, 0, 0], total)
        self.check_fsr([0.64, 2.57, 3.21], ret[:,3])

        self.fc.fuel_moisture_duff_pct = fm_duff_from_file
        self.fc.fuel_moisture_litter_pct = fm_litter_from_file

    def test_sq_midden_calc(self):
        #
        # NOTE: loadings are 1, 5, 10 for these catagories
        #
        FM_DUFF = 30
        FM_DUFF = 30
        FM_LITTER = 10
        my_print(self._ecoregion_masks)
        my_print(self._loadings['sqm_loading'])
        
        fm_duff_from_file = self.fc.fuel_moisture_duff_pct
        fm_litter_from_file = self.fc.fuel_moisture_litter_pct
        self.fc.fuel_moisture_duff_pct = FM_DUFF
        self.fc.fuel_moisture_litter_pct = FM_LITTER
        
        ret = ccn.basal_accumulation_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_litter_pct, self._ecoregion_masks)
        my_print(ret[3])  # print totals
        
        total = ret[3]
        self.assertEqual(8, len(total))
        self.check_catagory([0, .91, 1.93, 5.16, 0.63, 5.16, 0, 0], total)

        self.fc.fuel_moisture_duff_pct = fm_duff_from_file
        self.fc.fuel_moisture_litter_pct = fm_litter_from_file
















