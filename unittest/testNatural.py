import unittest
import consume
import consume.con_calc_natural as ccn
import helper

class TestNaturalEquations(unittest.TestCase):

    def setUp(self):
        loadings_file = helper.get_test_inputfile()
        self.fc = consume.FuelConsumption(fccs_file=loadings_file)

    def tearDown(self):
        pass
        
    def test_test(self):
        idxs = ['1','2','3']
        loadings = self.fc._get_loadings_for_specified_files(idxs)
        ret = ccn.ccon_shrub(0.5, loadings)
        for idx, _ in enumerate(idxs):
            print(ret[idx][3])        
        self.assertFalse(True)            
        
    def test_shrub_calc(self):
        # Setup ecoregion masks for equations that vary by ecoregion
        ecodict = {"maskb": {"boreal":1, "western":0, "southern":0},
                     "masks": {"boreal":0, "western":0, "southern":1},
                     "maskw": {"boreal":0, "western":1, "southern":0}}
        ecoregion = ['western']
        ecob_mask = [ecodict["maskb"][e] for e in ecoregion]
        ecos_mask = [ecodict["masks"][e] for e in ecoregion]
        ecow_mask = [ecodict["maskw"][e] for e in ecoregion]
        ecoregion_masks = {'boreal':ecob_mask, 'southern':ecos_mask , 'western':ecow_mask}    
        
        idxs = ['1','2','3']
        loadings = self.fc._get_loadings_for_specified_files(idxs)
        ret = ccn.shrub_calc(0.5, loadings, ecoregion_masks)
        print(ret)
        print(ret / 2.0)
        self.assertFalse(True)