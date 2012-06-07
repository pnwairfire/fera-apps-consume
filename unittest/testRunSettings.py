import unittest
import run_settings as setting

class TestRunSettings(unittest.TestCase):

    def setUp(self):
        pass

    def reset_consumer(self):
        pass

    def tearDown(self):
        pass

    def testInitial(self):
        ''' Everything should be empty '''
        s = setting.RunSettings()
        self.assertFalse(s.units)
        self.assertFalse(s.burn_type)
        self.assertFalse(s.fm_type)
        settings = setting.RunSettings.NaturalSNames + setting.RunSettings.ActivitySNames
        for i in settings:
            self.assertFalse(s.get(i))

    def testSetProperties(self):
        ''' Exercise setting the 1-value properties '''
        s = setting.RunSettings()
        s.burn_type = 'natural'
        self.assertEqual('natural', s.burn_type)
        s.burn_type = 'activity'
        self.assertEqual('activity', s.burn_type)
        s.burn_type = 'kjell'
        self.assertEqual('activity', s.burn_type)

        s.units = 'kg_ha'
        self.assertEqual('kg_ha', s.units)
        s.units = 'kjell'
        self.assertEqual('kg_ha', s.units)

        s.fm_type = 'MEAS-Th'
        self.assertEqual('MEAS-Th', s.fm_type)
        s.fm_type = 'kjell'
        self.assertEqual('MEAS-Th', s.fm_type)

    def testAddSettings(self):
        ''' Add settings and verify completeness '''
        s = setting.RunSettings()
        items = [1, 2, 4]
        self.assertFalse(s.set('fuelbeds', items))  # need to specify burn_type before adding settings
        s.burn_type = 'activity'
        self.assertTrue(s.set('fuelbeds', items))
        fb = s.get('fuelbeds')
        i = 0
        while i < len(fb):
            self.assertEqual(fb[i], items[i])
            i += 1
        self.assertTrue(s.set('slope', [1, 2, 4]))
        self.assertTrue(s.set('windspeed', [1, 2, 4]))
        self.assertTrue(s.set('days_since_rain', [1, 2, 4]))
        self.assertTrue(s.set('fm_10hr', [1, 2, 4]))
        self.assertTrue(s.set('length_of_ignition', [1, 2, 4]))
        self.assertTrue(s.set('area', [1, 2, 4]))
        self.assertTrue(s.set('ecoregion', ['western', 'southern', 'boreal']))
        self.assertTrue(s.set('fm_1000hr', [1, 2, 4]))
        self.assertTrue(s.set('fm_duff', [1, 2, 4]))
        self.assertTrue(s.set('can_con_pct', [1, 2, 4]))
        self.assertTrue(s.set('shrub_black_pct', [1, 2, 4]))
        self.assertTrue(s.set('efg', [1, 2, 4]))
        s.fm_type = 'MEAS-Th'
        s.units = 'kg_ha'
        self.assertTrue(s.settings_are_complete())
            


