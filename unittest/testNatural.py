import unittest
import consume
import consume.con_calc_natural as ccn
import helper
import numpy as np

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
        print(self.fc._settings.get('ecoregion'))

        ecoregion = self.fc._settings.get('ecoregion')
        self._ecob_mask = [self._ecodict["maskb"][e] for e in ecoregion]
        self._ecos_mask = [self._ecodict["masks"][e] for e in ecoregion]
        self._ecow_mask = [self._ecodict["maskw"][e] for e in ecoregion]
        self._ecoregion_masks = {
            'boreal': self._ecob_mask,
            'southern': self._ecos_mask,
            'western': self._ecow_mask}
        # print(ecoregion_masks)

    def tearDown(self):
        pass

    def compute_shrub_totals(self, ret):
        print('\nType: '.format(type(ret)))
        totals = np.zeros_like(ret[0][:, ][3])
        for i, v in enumerate(ret):
            totals += v[:, ][3]
        print('\n{}'.format(totals))
        return totals

    def test_ccon_shrub(self):
        ''' this simply gets values against which to compare '''
        shrub_black_pct = 0.8
        ret = ccn.ccon_shrub(shrub_black_pct, self._loadings)
        self.compute_shrub_totals(ret)

    def test_shrub_calc(self):
        shrub_black_pct = 0.8
        ret = ccn.shrub_calc(shrub_black_pct, self._loadings, self._ecoregion_masks)
        totals = self.compute_shrub_totals(ret)
        self.assertAlmostEqual(0.78, totals[0], places=2)
        self.assertAlmostEqual(2.22, totals[1], places=2)
        self.assertAlmostEqual(1.09, totals[2], places=2)
        self.assertAlmostEqual(1.9, totals[3], places=2)
        self.assertAlmostEqual(0.82, totals[4], places=2)
        self.assertAlmostEqual(1.9, totals[5], places=2)
        self.assertAlmostEqual(0.0, totals[6], places=2)
        self.assertAlmostEqual(0.0, totals[7], places=2)
        self.assertAlmostEqual(0.0, totals[8], places=2)

    def test_ccon_one(self):
        ret = ccn.ccon_one_nat(self._loadings)
        print(ret[3])  # print totals

    def test_sound_one_nat(self):
        ret = ccn.sound_one_nat(self._loadings)
        print(ret[3])  # print totals
        totals = ret[3]
        self.assertEquals(9, len(totals))
        self.assertAlmostEqual(0.5, totals[0], places=2)
        self.assertAlmostEqual(1.5, totals[1], places=2)
        self.assertAlmostEqual(1.5, totals[2], places=2)
        self.assertAlmostEqual(3.0, totals[3], places=2)
        self.assertAlmostEqual(0.5, totals[4], places=2)
        self.assertAlmostEqual(3.0, totals[5], places=2)
        self.assertAlmostEqual(0.0, totals[6], places=2)
        self.assertAlmostEqual(0.0, totals[7], places=2)
        self.assertAlmostEqual(0.0, totals[8], places=2)

    def test_ccon_ten(self):
        ret = ccn.ccon_ten_nat(self._loadings)
        print(ret[3])  # print totals

    def test_sound_ten_nat(self):
        CONSUMPTION_FACTOR = 0.8581
        ret = ccn.sound_ten_nat(self._loadings)
        print(ret[3])  # print totals
        totals = ret[3]
        self.assertEquals(9, len(totals))
        self.assertAlmostEqual(0.5 * CONSUMPTION_FACTOR, totals[0], places=4)
        self.assertAlmostEqual(1.5 * CONSUMPTION_FACTOR, totals[1], places=4)
        self.assertAlmostEqual(1.5 * CONSUMPTION_FACTOR, totals[2], places=4)
        self.assertAlmostEqual(3.0 * CONSUMPTION_FACTOR, totals[3], places=4)
        self.assertAlmostEqual(0.5 * CONSUMPTION_FACTOR, totals[4], places=4)
        self.assertAlmostEqual(3.0 * CONSUMPTION_FACTOR, totals[5], places=4)
        self.assertAlmostEqual(0.0 * CONSUMPTION_FACTOR, totals[6], places=4)
        self.assertAlmostEqual(0.0 * CONSUMPTION_FACTOR, totals[7], places=4)
        self.assertAlmostEqual(0.0 * CONSUMPTION_FACTOR, totals[8], places=4)

    def test_ccon_hun_nat(self):
        ret = ccn.ccon_hun_nat(self._ecos_mask, self._loadings)
        print(ret[3])  # print totals

    def test_sound_hundred_nat(self):
        CONSUMPTION_FACTOR = 0.7166
        CONSUMPTION_FACTOR_SOUTHERN = 0.4022
        ret = ccn.sound_hundred_nat(self._loadings, self._ecos_mask)
        print(ret[3])  # print totals
        totals = ret[3]
        self.assertEquals(9, len(totals))
        self.assertAlmostEqual(0.5 * CONSUMPTION_FACTOR, totals[0], places=4)
        self.assertAlmostEqual(1.5 * CONSUMPTION_FACTOR_SOUTHERN, totals[1], places=4)
        self.assertAlmostEqual(1.5 * CONSUMPTION_FACTOR, totals[2], places=4)
        self.assertAlmostEqual(3.0 * CONSUMPTION_FACTOR, totals[3], places=4)
        self.assertAlmostEqual(0.5 * CONSUMPTION_FACTOR_SOUTHERN, totals[4], places=4)
        self.assertAlmostEqual(3.0 * CONSUMPTION_FACTOR, totals[5], places=4)
        self.assertAlmostEqual(0.0 * CONSUMPTION_FACTOR, totals[6], places=4)
        self.assertAlmostEqual(0.0 * CONSUMPTION_FACTOR_SOUTHERN, totals[7], places=4)
        self.assertAlmostEqual(0.0 * CONSUMPTION_FACTOR, totals[8], places=4)


