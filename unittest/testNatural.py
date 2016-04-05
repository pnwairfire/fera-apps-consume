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
        
    def test_ccon_shrub(self):
        idxs = ['1','2','3']
        loadings = self.fc._get_loadings_for_specified_files(idxs)
        shrub_black_pct = 0.8
        ret = ccn.ccon_shrub(shrub_black_pct, loadings)
        print(ret)
        print(type(ret))

    def test_shrub_calc(self):
        # Setup ecoregion masks for equations that vary by ecoregion
        ecodict = {"maskb": {"boreal":1, "western":0, "southern":0},
                     "masks": {"boreal":0, "western":0, "southern":1},
                     "maskw": {"boreal":0, "western":1, "southern":0}}

        self.fc.burn_type = 'natural'
        self.fc.load_scenario(load_file='test_input.csv')
        shrub_black_pct = 0.8
        loadings = self.fc._get_loadings_for_specified_files(self.fc._settings.get('fuelbeds'))
        print(loadings)
        print('---')
        print(self.fc._settings.get('ecoregion'))

        ecoregion = self.fc._settings.get('ecoregion')
        ecob_mask = [ecodict["maskb"][e] for e in ecoregion]
        ecos_mask = [ecodict["masks"][e] for e in ecoregion]
        ecow_mask = [ecodict["maskw"][e] for e in ecoregion]
        ecoregion_masks = {'boreal': ecob_mask, 'southern': ecos_mask, 'western': ecow_mask}
        print(ecoregion_masks)

        ret = ccn.shrub_calc(shrub_black_pct, loadings, ecoregion_masks)
        print(ret)
        self.assertAlmostEqual(0.78, ret[0], places=2)
        self.assertAlmostEqual(1.09, ret[2], places=2)
        self.assertAlmostEqual(1.9, ret[3], places=2)
        self.assertAlmostEqual(1.9, ret[5], places=2)
        self.assertAlmostEqual(2.22, ret[1], places=2)
        self.assertAlmostEqual(0.82, ret[4], places=2)
