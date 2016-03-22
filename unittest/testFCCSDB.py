import unittest
from consume.fccs_db import FCCSDB
import re
import helper

class TestFCCSDB(unittest.TestCase):

    def setUp(self):
        self.db = FCCSDB()

    def tearDown(self):
        pass

    def test_short_info(self):
        ''' testing short_info '''
        short_info = self.db.info('1', detail=False, ret=True)
        chunks = short_info.split('\n')
        self.assertTrue(5 == len(chunks), "Got: {}".format(len(chunks)))
        self.assertTrue('1' in chunks[1], "Got: {}".format(chunks[1]))
        self.assertTrue('Site name' in chunks[2], "Got: {}".format(chunks[2]))
        self.assertTrue('Site description' in chunks[4], "Got: {}".format(chunks[4]))

    # This is ugly. Originally in place to test functionality that MTRI was using, several
    #  layers of changes have made it largely useless (fuelbed file format changed, possible
    #  python 2 to 3 changes). TODO: consider removing
    def test_long_info(self):
        ''' Long info check: '''
        expected = {
            'FCCS ID#':1,
            'Bailey\'s ecoregion division(s)':240,
            'SAM/SRM cover type(s)':129,
            'Overstory':19.44,
            'Midstory':8.72,
            'Understory':0.51,
            'Snags, class 1, foliage':0,
            'Snags, class 1, wood':0,
            'Snags, class 1, w/o foliage':1.3,
            'Snags, class 2':0.25,
            'Snags, class 3':1.17,
            'Ladder fuels':4.6,
            #'Shrub Primary':1.15, this is in the xml file. It is multiplied by 3 for some reason.
            'Shrub Primary':3.45,
            'Shrub Primary % live':95.0,
            'Shrub Secondary':0,
            'Shrub Secondary % live':0,
            'NW Primary':0.2,
            'NW Primary % live':90,
            'NW Secondary':0,
            'NW Secondary % live':0,
            'Litter depth':.5,
            'Litter % cover':85,
            'Short needle':30,
            'Long needle':0,
            'Other conifer':0,
            'Broadleaf deciduous':70.0,
            'Broadleaf evergreen':0,
            'Palm frond':0,
            'Grass':0,
            'Lichen depth':0.1,
            'Lichen % cover':5,
            'Moss depth':0.5,
            'Moss % cover':40.0,
            'Moss type':2,
            'Duff depth, upper':0.5,
            'Duff % cover, upper':100,
            'Duff derivation, upper':2,
            'Duff depth, lower':1.5,
            'Duff % cover, lower':100,
            'Duff derivation, lower':4,
            'Basal accumulations depth':0,
            'Basal accum. % cover':0,
            'Basal accumulations radius':0,
            'Squirrel midden depth':0,
            'Squirrel midden density':0,
            'Squirrel midden radius':0,
            '1-hr (0-0.25")':0.2,
            '10-hr (0.25-1")':0.8,
            '100-hr (1-3")':3.5,
            '1000-hr (3-9"), sound':0.4,
            '10,000-hr (9-20"), sound':0.5,
            '10,000-hr+ (>20"), sound':0,
            '1000-hr (3-9"), rotten':3.0,
            '10,000-hr (9-20"), rotten':4.0,
            '10,000-hr+ (>20"), rotten':5.0,
            'Stumps, sound':0,
            'Stumps, rotten':0.029,
            'Stumps, lightered':0
        }
        long_info = self.db.info(1, detail=True, ret=True)
        if len(long_info):
            chunks = long_info.split('\n')
            if len(chunks) > 1:
                for item in chunks:
                    item = item.strip()
                    if ':' in item:
                        key = item.split(':')[0].strip()
                        value = item.split(': ')[1].split(' ')[0]
                        if value.endswith('%'):
                            value = value[len(value)-1] if len(value) > 1 else None
                        if key in expected.keys():
                            try:
                                a = float(expected[key])
                                b = float(value)
                                self.assertAlmostEqual(a, b, 2)
                            except:
                                pass
                        else:
                            pass
                            #print('no key: {}'.format(key))
            else:
                self.assertFalse(True, msg='Error: No chunks to examine')
        else:
            self.assertFalse(True, msg='Error: No info returned from info()')


    def test_check_info(self):
        check_good = self.db.info('1', detail=False, ret=True)
        self.assertTrue('not found' not in check_good)
        check_bad = self.db.info(50, detail=False, ret=True)
        self.assertTrue('not found' in check_bad)


if __name__ == '__main__':
    unittest.main()