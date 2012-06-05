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
        s = setting.RunSettings()
        self.assertFalse(s.units)
        self.assertFalse(s.burn_type)
        self.assertFalse(s.fm_type)
        settings = setting.RunSettings.NaturalSNames + setting.RunSettings.ActivitySNames
        for i in settings:
            self.assertFalse(s.get(i))

    def testSetProperties(self):
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
        s = setting.RunSettings()
        items = [1, 2, 4]
        self.assertFalse(s.add('fuelbeds', items))  # need to specify burn_type before adding settings
        s.burn_type = 'activity'
        self.assertTrue(s.add('fuelbeds', items))
        fb = s.get('fuelbeds')
        i = 0
        while i < len(fb):
            self.assertEqual(fb[i], items[i])
            i += 1
        self.assertTrue(s.add('slope', [1, 2, 4]))
        self.assertTrue(s.add('windspeed', [1, 2, 4]))
        self.assertTrue(s.add('days_since_rain', [1, 2, 4]))
        self.assertTrue(s.add('fm_10hr', [1, 2, 4]))
        self.assertTrue(s.add('length_of_ignition', [1, 2, 4]))
        self.assertTrue(s.add('area', [1, 2, 4]))
        self.assertTrue(s.add('ecoregion', ['western', 'southern', 'boreal']))
        self.assertTrue(s.add('fm_1000hr', [1, 2, 4]))
        self.assertTrue(s.add('fm_duff', [1, 2, 4]))
        self.assertTrue(s.add('can_con_pct', [1, 2, 4]))
        self.assertTrue(s.add('shrub_black_pct', [1, 2, 4]))
        self.assertTrue(s.add('efg', [1, 2, 4]))
        s.fm_type = 'MEAS-Th'
        s.units = 'kg_ha'
        self.assertTrue(s.settings_are_complete())
            


