import unittest
from consume import input_variables as iv
import helper

class TestInputVariables(unittest.TestCase):

    def setUp(self):
        pass

    def reset_consumer(self):
        pass

    def tearDown(self):
        pass

    def testValidation(self):
        '''
        For each item there are 2 lists. Acceptable values and values that should be
        rejected. Run through them.
        tests = {
            'fuelbeds': { 'good' : [], 'bad' : []},
            'area': { 'good' : [0,1000000], 'bad' : [-1, 1000001, 'a']},
            'ecoregion': { 'good' : ['western', 'boreal', 'southern', ], 'bad' : ['bogusEcoregion']},
            'fm_1000hr': { 'good' : [0,140], 'bad' : [-1, 141, 'a']},
            'fm_duff': { 'good' : [0, 400], 'bad' : [-1, 401, 'a']},
            'can_con_pct': { 'good' : [0, 100], 'bad' : [-1, 101, 'a']},
            'shrub_black_pct': { 'good' :[0, 100], 'bad' : [-1, 101, 'a']},
            'burn_type': { 'good' : ['natural', 'activity'], 'bad' : [1, 'bogus']},
            'units': { 'good' : ['tons_ac'], 'bad' : ['bogusUnit']},
            'slope': { 'good' : [0, 100], 'bad' : [-1, 101, 'a']},
            'windspeed': { 'good' : [0, 35], 'bad' : [-1, 36, 'a']},
            'fm_type': { 'good' : ['MEAS-Th'], 'bad' : ['bogusFM']},
            'days_since_rain': { 'good' : [0, 365], 'bad' : [-1, 366, 'a']},
            'fm_10hr': { 'good' : [0, 100], 'bad' : [-1, 101, 'a']},
            'length_of_ignition': { 'good' : [0,10000], 'bad' : [-1, 10001, 'a']}
            }

        for key, val in tests.iteritems():
            testVar = iv.InputVar(key)
            self.assertTrue(testVar.validate())
            for item in val['good']:
                testVar.value = item
                self.assertTrue(testVar.validate(), msg="\n\tItem is: {} value is:".format(key, item))
            for item in val['bad']:
                testVar.value = item
                self.assertFalse(testVar.validate(), msg="\n\tItem is: '{}' value is: {}".format(key, item))
        '''

    def testLoadScenario(self):
        pass

if __name__ == '__main__':
    unittest.main()
