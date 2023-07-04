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
import pandas as pd

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
    
# Use the consumption column key as the key into this
COMBUSTION_PHASE_TABLE = {
    'c_wood_1hr': [.95,.05,0.0],
    'c_wood_10hr': [.90,.1,0.0],
    'c_wood_100hr': [.85,.10,0.05],
    'c_wood_s1000hr': [.6,.3,.1],
    'c_wood_s10khr': [.4,.4,.2],
    'c_wood_s+10khr': [.2,.4,.4],
    'c_wood_r1000hr': [.2,.3,.5],
    'c_wood_r10khr': [.1,.3,.6],
    'c_wood_r+10khr': [.1,.3,.6],
    'c_upperduff': [.1,.7,.2],
    'c_lowerduff': [.0,.2,.8],
    'c_basal_accum': [.1,.4,.5],
    'c_squirrel': [.1,.3,.6],
    'c_litter': [.9,.1,.0],
    'c_lichen': [.95,.05,0.0],
    'c_moss': [.95,.05,0.0],
    'c_herb': [.95,.05,0.0],
    'c_shrub': [.90, .10, 0.0]
}
    
SOUTHERN_EXPECTED_FILE = 'southern_unittest.csv'
WESTERN_EXPECTED_FILE = 'western_unittest.csv'
    
class TestNaturalEquations(unittest.TestCase):
    @classmethod    
    def setUpClass(self):
        '''
        Expected values come from a spreadsheet in the Consume docs repo.
        Run a script there to extract and format the expected values into .csv file.
        Current, copy the files to this repo. Consider using CI server in the future.
        '''
        self._south_exp = pd.read_csv(helper.imp(SOUTHERN_EXPECTED_FILE))
        self._west_exp = pd.read_csv(helper.imp(WESTERN_EXPECTED_FILE))
        
        # unfortunately, the basal acc. and sq. midden calculations use proportional duff consumption
        self._duff_proportional_consumption = None
        
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
    
    def check_catagory(self, reference_values, calculated_values, num_places=2):
        self.assertEqual(len(reference_values), len(calculated_values))
        for idx, val in enumerate(reference_values):
            self.assertAlmostEqual(val, calculated_values[idx], places=num_places)
            
    def check_fsr(self, reference_values, calculated_values, phase_coeffs):
        for j in range(2):
            my_print('\nvvv\n{}'.format(reference_values*phase_coeffs[j]))
            my_print('{}\n^^^'.format(calculated_values[j]))
            close_enough = np.isclose(reference_values*phase_coeffs[j], calculated_values[j], rtol=1e-04).all()
            self.assertTrue(True, close_enough)
            
    def get_expected_list(self, keyname):
        '''
        gets the low, medium, high, and zero values for the western expected 
        catagory specified by keyname (column name). Then extends the list 
        with the southern versions
        '''
        tmp = [i for i in self._west_exp.get(keyname)]
        tmp.extend([i for i in self._south_exp.get(keyname)])
        return np.array(tmp)

    def test_herb_calc(self): 
        ret = ccn.herb_calc(self._loadings, self._ecoregion_masks)
        totals = ret[0][:, ][3] + ret[1][:, ][3]
        exp_totals = self.get_expected_list('c_herb')
        self.check_catagory(exp_totals, totals)
        self.check_fsr(exp_totals, totals, COMBUSTION_PHASE_TABLE['c_herb'])

    def test_shrub_calc(self):
        ret = ccn.shrub_calc(self.fc.shrub_blackened_pct, self._loadings, self._ecoregion_masks, 0)
        totals = ret[0][:, ][3] + ret[1][:, ][3]
        exp_totals = self.get_expected_list('c_shrub')
        self.check_catagory(exp_totals, totals)
        self.check_fsr(exp_totals, totals, COMBUSTION_PHASE_TABLE['c_shrub'])

    def test_sound_one_calc(self): 
        ret = ccn.sound_one_calc(self._loadings, self._ecos_mask)
        my_print(ret[3])
        totals = ret[3]
        self.assertEqual(8, len(totals))
        exp_totals = self.get_expected_list('c_wood_1hr')
        self.check_catagory(exp_totals, totals)
        self.check_fsr(exp_totals, ret[0:3,:], COMBUSTION_PHASE_TABLE['c_wood_1hr'])

    def test_sound_ten_calc(self): 
        ret = ccn.sound_ten_calc(self._loadings, self._ecos_mask)
        my_print(ret[3])
        totals = ret[3]
        self.assertEqual(8, len(totals))
        exp_totals = self.get_expected_list('c_wood_10hr')
        self.check_catagory(exp_totals, totals)
        self.check_fsr(exp_totals, ret[0:3,:], COMBUSTION_PHASE_TABLE['c_wood_10hr'])

    def test_sound_hundred_calc(self): 
        ret = ccn.sound_hundred_calc(self._loadings, self._ecos_mask)
        my_print(ret[3])
        totals = ret[3]
        self.assertEqual(8, len(totals))
        exp_totals = self.get_expected_list('c_wood_100hr')
        self.check_catagory(exp_totals, totals)
        self.check_fsr(exp_totals, ret[0:3,:], COMBUSTION_PHASE_TABLE['c_wood_100hr'])

    def test_sound_large_wood_calc(self):  
        one_k, ten_k, tenk_plus = ccn.sound_large_wood_calc(self._loadings, self.fc.fuel_moisture_1000hr_pct, self.fc.sound_cwd_pct_available)
        totals = one_k[3] + ten_k[3] + tenk_plus[3]
        my_print(totals)
        
        one_k_totals = one_k[3]
        exp_totals = self.get_expected_list('c_wood_s1000hr')
        self.check_catagory(exp_totals, one_k_totals)
        self.check_fsr(exp_totals, one_k[0:3,:], COMBUSTION_PHASE_TABLE['c_wood_s1000hr'])
        
        ten_k_totals = ten_k[3]
        exp_totals = self.get_expected_list('c_wood_s10khr')
        self.check_catagory(exp_totals, ten_k_totals)
        self.check_fsr(exp_totals, ten_k[0:3,:], COMBUSTION_PHASE_TABLE['c_wood_s10khr'])
        
        tenk_plus_totals = tenk_plus[3]
        exp_totals = self.get_expected_list('c_wood_s+10khr')
        self.check_catagory(exp_totals, tenk_plus_totals)
        self.check_fsr(exp_totals, tenk_plus[0:3,:], COMBUSTION_PHASE_TABLE['c_wood_s+10khr'])

    def test_rotten_large_wood_calc(self):  
        one_k, ten_k, tenk_plus = ccn.rotten_large_wood_calc(self._loadings, self.fc.fuel_moisture_1000hr_pct, self.fc.rotten_cwd_pct_available)
        totals = one_k[3] + ten_k[3] + tenk_plus[3]
        my_print(totals)  # print totals

        one_k_totals = one_k[3]
        exp_totals = self.get_expected_list('c_wood_r1000hr')
        self.check_catagory(exp_totals, one_k_totals, num_places=1)
        self.check_fsr(exp_totals, one_k[0:3,:], COMBUSTION_PHASE_TABLE['c_wood_r1000hr'])

        ten_k_totals = ten_k[3]
        exp_totals = self.get_expected_list('c_wood_r10khr')
        self.check_catagory(exp_totals, ten_k_totals, num_places=1)
        self.check_fsr(exp_totals, ten_k[0:3,:], COMBUSTION_PHASE_TABLE['c_wood_r10khr'])

        tenk_plus_totals = tenk_plus[3]
        exp_totals = self.get_expected_list('c_wood_r+10khr')
        self.check_catagory(exp_totals, tenk_plus_totals, num_places=1)
        self.check_fsr(exp_totals, tenk_plus[0:3,:], COMBUSTION_PHASE_TABLE['c_wood_r+10khr'])

    def test_litter_calc(self):
        my_print(self._loadings['litter_loading'])
        
        ret, proportion_litter_consumed = ccn.litter_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_1000hr_pct, self._ecoregion_masks)
        my_print(ret[3])
        
        total = ret[3]
        exp_totals = self.get_expected_list('c_litter')
        self.check_catagory(exp_totals, total, num_places=4)
        self.check_fsr(exp_totals, ret[0:3,:], COMBUSTION_PHASE_TABLE['c_litter'])

    def test_lichen_calc(self):
        my_print(self._ecoregion_masks)
        my_print(self._loadings['lichen_loading'])
        
        _, proportion_litter_consumed = ccn.litter_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_1000hr_pct, self._ecoregion_masks)
        
        ret = ccn.lichen_calc(self._loadings, self.fc.fuel_moisture_duff_pct,
                self.fc.fuel_moisture_1000hr_pct, self._ecoregion_masks, proportion_litter_consumed)
        my_print(ret[3])
        
        total = ret[3]
        exp_totals = self.get_expected_list('c_lichen')
        self.check_catagory(exp_totals, total, num_places=4)
        self.check_fsr(exp_totals, ret[0:3,:], COMBUSTION_PHASE_TABLE['c_lichen'])

    def test_moss_calc(self):
        my_print(self._ecoregion_masks)
        my_print(self._loadings['moss_loading'])
        
        _, proportion_litter_consumed = ccn.litter_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_1000hr_pct, self._ecoregion_masks)
        
        ret = ccn.moss_calc(self._loadings, self.fc.fuel_moisture_duff_pct,
                self.fc.fuel_moisture_1000hr_pct, self._ecoregion_masks, proportion_litter_consumed)
        my_print(ret[3])
        
        total = ret[3]
        exp_totals = self.get_expected_list('c_moss')
        self.check_catagory(exp_totals, total, num_places=4)
        self.check_fsr(exp_totals, ret[0:3,:], COMBUSTION_PHASE_TABLE['c_moss'])

    def test_duff_calc(self):
        cons_duff_upper, cons_duff_lower, proportion_duff_consumed = ccn.duff_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_litter_pct, self._ecoregion_masks, self.fc.duff_pct_available)
        
        total = cons_duff_upper[3] + cons_duff_lower[3]
        
        # upper duff
        total = cons_duff_upper[3]
        exp_totals = self.get_expected_list('c_upperduff')
        self.check_catagory(exp_totals, total)
        self.check_fsr(exp_totals, cons_duff_upper[0:3,:], COMBUSTION_PHASE_TABLE['c_upperduff'])
        
        # lower duff
        total = cons_duff_lower[3]
        exp_totals = self.get_expected_list('c_lowerduff')
        self.check_catagory(exp_totals, total)
        self.check_fsr(exp_totals, cons_duff_lower[0:3,:], COMBUSTION_PHASE_TABLE['c_lowerduff'])

    def test_basal_acc_calc(self):
        my_print(self._loadings['bas_loading'])
        
        # need proportion of duff consumed...
        _, _, proportion_duff_consumed = ccn.duff_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_litter_pct, self._ecoregion_masks, self.fc.duff_pct_available)
        self.assertTrue(len(proportion_duff_consumed))
                
        ret = ccn.basal_accumulation_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct,
                self.fc.fuel_moisture_litter_pct,
                self._ecoregion_masks,
                proportion_duff_consumed)
        my_print(ret[3])  # print totals
        
        total = ret[3]
        exp_totals = self.get_expected_list('c_basal_accum')
        self.check_catagory(exp_totals, total)
        self.check_fsr(exp_totals, ret[0:3,:], COMBUSTION_PHASE_TABLE['c_basal_accum'])

    def test_sq_midden_calc(self):
        my_print(self._loadings['sqm_loading'])
        
        # need proportion of duff consumed...
        _, _, proportion_duff_consumed = ccn.duff_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct, self.fc.fuel_moisture_litter_pct, self._ecoregion_masks, self.fc.duff_pct_available)
        self.assertTrue(len(proportion_duff_consumed))
                        
        ret = ccn.squirrel_midden_calc(self._loadings,
                self.fc.fuel_moisture_duff_pct,
                self.fc.fuel_moisture_litter_pct,
                self._ecoregion_masks,
                proportion_duff_consumed)
        my_print(ret[3])  # print totals
        
        total = ret[3]
        exp_totals = self.get_expected_list('c_squirrel')
        self.check_catagory(exp_totals, total)
        self.check_fsr(exp_totals, ret[0:3,:], COMBUSTION_PHASE_TABLE['c_squirrel'])
















