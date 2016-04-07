import unittest
import consume
import consume.con_calc_natural as ccn
import helper
import numpy as np

class TestNaturalEquations(unittest.TestCase):

    def setUp(self):
        loadings_file = helper.get_test_loadingsfile()
        self.fc = consume.FuelConsumption(fccs_file=loadings_file)

    def tearDown(self):
        pass
        
    def test_ccon_shrub(self):
        self.fc.burn_type = 'natural'
        self.fc.load_scenario(load_file=helper.get_test_inputfile())
        loadings = self.fc._get_loadings_for_specified_files(self.fc._settings.get('fuelbeds'))
        shrub_black_pct = 0.8
        ret = ccn.ccon_shrub(shrub_black_pct, loadings)
        print(type(ret))
        totals = np.zeros_like(ret[0][:,][3])
        for i, v in enumerate(ret):
            totals += v[:,][3]
        print('\n{}'.format(totals))

    def test_shrub_calc(self):
        # Setup ecoregion masks for equations that vary by ecoregion
        ecodict = {"maskb": {"boreal":1, "western":0, "southern":0},
                     "masks": {"boreal":0, "western":0, "southern":1},
                     "maskw": {"boreal":0, "western":1, "southern":0}}

        self.fc.burn_type = 'natural'
        self.fc.load_scenario(load_file=helper.get_test_inputfile())
        shrub_black_pct = 0.8
        loadings = self.fc._get_loadings_for_specified_files(self.fc._settings.get('fuelbeds'))
        print(loadings.shrub_prim)
        print('---')
        print(self.fc._settings.get('ecoregion'))

        ecoregion = self.fc._settings.get('ecoregion')
        ecob_mask = [ecodict["maskb"][e] for e in ecoregion]
        ecos_mask = [ecodict["masks"][e] for e in ecoregion]
        ecow_mask = [ecodict["maskw"][e] for e in ecoregion]
        ecoregion_masks = {'boreal': ecob_mask, 'southern': ecos_mask, 'western': ecow_mask}
        print(ecoregion_masks)

        ret = ccn.shrub_calc(shrub_black_pct, loadings, ecoregion_masks)
        totals = np.zeros_like(ret[0][:,][3])
        for i, v in enumerate(ret):
            totals += v[:,][3]
        print('\n{}'.format(totals))
        self.assertAlmostEqual(0.78, totals[0], places=2)
        self.assertAlmostEqual(2.22, totals[1], places=2)
        self.assertAlmostEqual(1.09, totals[2], places=2)
        self.assertAlmostEqual(1.9, totals[3], places=2)
        self.assertAlmostEqual(0.82, totals[4], places=2)
        self.assertAlmostEqual(1.9, totals[5], places=2)
        self.assertAlmostEqual(0.0, totals[6], places=2)
