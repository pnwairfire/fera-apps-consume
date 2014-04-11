import unittest
import tempfile as tf
import os
from consume.input_settings import ConsumeInputSettings
import pandas as pan



class TestInputSettings(unittest.TestCase):

    def setUp(self):
        pass

    def reset_consumer(self):
        pass

    def tearDown(self):
        pass

    def testInitial(self):
        ''' Everything should be empty '''
        s = ConsumeInputSettings()
        self.assertFalse(s.units)
        self.assertFalse(s.burn_type)
        self.assertFalse(s.fm_type)
        settings = ConsumeInputSettings.NaturalSNames + ConsumeInputSettings.ActivitySNames
        for i in settings:
            self.assertFalse(s.get(i))

    def testSetProperties(self):
        ''' Exercise setting the 1-value properties '''
        s = ConsumeInputSettings()
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
        ''' Add settings and check:
                - need to specify burn_type first
                - individual values will be turned into a sequence if necessary
                - the object knows when it has all required settings
        '''
        s = ConsumeInputSettings()
        items = [1, 2, 4]
        self.assertFalse(s.set('fuelbeds', items))  # need to specify burn_type before adding settings
        s.burn_type = 'activity'
        self.assertTrue(s.set('fuelbeds', items))
        fb = s.get('fuelbeds')
        i = 0
        while i < len(fb):
            self.assertEqual(fb[i], str(items[i]))
            i += 1
        self.assertTrue(s.set('slope', [1, 2, 4]))
        self.assertTrue(s.set('windspeed', [1, 2, 4]))
        self.assertTrue(s.set('days_since_rain', [1, 2, 4]))
        self.assertTrue(s.set('fm_10hr', 2))    ### - manufacture a sequence if necessary
        self.assertTrue(s.set('length_of_ignition', [1, 2, 4]))
        self.assertTrue(s.set('area', [1, 2, 4]))
        self.assertTrue(s.set('ecoregion', ['western', 'southern', 'boreal']))
        self.assertTrue(s.set('fm_1000hr', [1, 2, 4]))
        self.assertTrue(s.set('fm_duff', [1, 2, 4]))
        self.assertTrue(s.set('can_con_pct', 4))    ### - manufacture a sequence if necessary
        self.assertTrue(s.set('shrub_black_pct', [1, 2, 4]))
        self.assertTrue(s.set('pile_black_pct', [1, 2, 4]))
        s.fm_type = 'MEAS-Th'
        self.assertFalse(s.settings_are_complete())
        s.units = 'kg_ha'
        self.assertTrue(s.settings_are_complete())

    def testDisplaySettings(self):
        items = [1, 2, 4]
        s = ConsumeInputSettings()
        s.burn_type = 'activity'
        self.assertTrue(s.set('fuelbeds', items))
        fb = s.get('fuelbeds')
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
        s.fm_type = 'MEAS-Th'
        s.units = 'kg_ha'
        result = s.display_settings()
        ### - todo, no test here yet

    # -------------------------------------------------------------------------
    #   File loading tests
    # -------------------------------------------------------------------------
    ### - natural test data
    ncols = ['area', 'can_con_pct', 'ecoregion', 'fm_1000hr', 'fm_duff', 'fuelbeds', 'shrub_black_pct', 'units', 'pile_black_pct']
    nrows = [
        ['10', '20', 'western', '30', '40', '1', '50', 'kg_ha', '90'],
        ['20', '30', 'western', '40', '50', '1', '60', 'kg_ha', '90']]
        
    ### - activity test data
    acols = ['area', 'can_con_pct', 'ecoregion', 'fm_1000hr', 'fm_duff', \
        'fuelbeds', 'shrub_black_pct', 'units', 'slope', 'windspeed', 'days_since_rain', \
        'fm_10hr', 'length_of_ignition', 'fm_type', 'pile_black_pct']
    arows = [
        ['10', '20', 'western', '30', '40', '1', '50', 'kg_ha', '5', '10', '3', '20', '30', 'NFDRS-Th', '90'],
        ['15', '21', 'western', '35', '35', '2', '45', 'kg_ha', '10', '15', '4', '25', '35', 'NFDRS-Th', '90'],
        ['20', '22', 'western', '40', '30', '3', '40', 'kg_ha', '15', '20', '5', '30', '40', 'NFDRS-Th', '90']
        ]
        
    nat_data = pan.DataFrame(nrows, columns=ncols)
    act_data =  pan.DataFrame(arows, columns=acols)
   
    def write_file(self, in_data):
        tmp_file = tf.mkstemp()
        in_data.to_csv(tmp_file[1], index=False)
        os.close(tmp_file[0])
        return tmp_file

    def test_load_natural(self):
        ''' Write a temp file, load the temp file and verify that the settings are equal to the 
            values written. Close tempfile
        '''
        data = TestInputSettings.nat_data
        s1 = set(data.columns)
        s2 = set(ConsumeInputSettings.NaturalSNames)
        s2.add("units")
        self.assertEqual(s1, s2)

        infile = self.write_file(data)
        s = ConsumeInputSettings()
        s.burn_type = 'natural'
        self.assertTrue(s.load_from_file(infile[1]))
        self.assertEqual(s.burn_type, 'natural')
        self.assertEqual(s.units, 'kg_ha')
        self.assertEqual(list(s.get('area')), [float(x) for x in list(data.area)])
        self.assertEqual(list(s.get('can_con_pct')), [float(x) for x in list(data.can_con_pct)])
        self.assertEqual(list(s.get('ecoregion')), list(data.ecoregion))
        self.assertEqual(list(s.get('fm_1000hr')), [float(x) for x in list(data.fm_1000hr)])
        self.assertEqual(list(s.get('fm_duff')), [float(x) for x in list(data.fm_duff)])
        self.assertEqual(list(s.get('fuelbeds')), [str(x) for x in list(data.fuelbeds)])
        self.assertEqual(list(s.get('shrub_black_pct')), [float(x) for x in list(data.shrub_black_pct)])
        os.unlink(infile[1])

    def test_load_activity(self):
        ''' Write a temp file, load the temp file and verify that the settings are equal to the 
            values written. Close tempfile
        '''
        data = TestInputSettings.act_data
        s1 = set(data.columns)
        s2 = set(ConsumeInputSettings.AllSNames)
        s2.add("units")
        s2.add("fm_type")
        self.assertEqual(s1, s2)

        infile = self.write_file(data)
        s = ConsumeInputSettings()
        s.burn_type = 'activity'
        self.assertTrue(s.load_from_file(infile[1]))
        self.assertEqual(s.burn_type, 'activity')
        self.assertEqual(s.units, 'kg_ha')
        self.assertEqual(s.fm_type, 'NFDRS-Th')

        self.assertEqual(list(s.get('area')), [float(x) for x in list(data.area)])
        self.assertEqual(list(s.get('can_con_pct')), [float(x) for x in list(data.can_con_pct)])
        self.assertEqual(list(s.get('ecoregion')), list(data.ecoregion))
        self.assertEqual(list(s.get('fm_1000hr')), [float(x) for x in list(data.fm_1000hr)])
        self.assertEqual(list(s.get('fm_duff')), [float(x) for x in list(data.fm_duff)])
        self.assertEqual(list(s.get('fuelbeds')), [str(x) for x in list(data.fuelbeds)])
        self.assertEqual(list(s.get('shrub_black_pct')), [float(x) for x in list(data.shrub_black_pct)])

        self.assertEqual(list(s.get('slope')), [float(x) for x in list(data.slope)])
        self.assertEqual(list(s.get('windspeed')), [float(x) for x in list(data.windspeed)])
        self.assertEqual(list(s.get('days_since_rain')), [float(x) for x in list(data.days_since_rain)])
        self.assertEqual(list(s.get('fm_10hr')), [float(x) for x in list(data.fm_10hr)])
        self.assertEqual(list(s.get('length_of_ignition')), [float(x) for x in list(data.length_of_ignition)])
        
        os.unlink(infile[1])

    def test_load_same_column_values(self):
        ''' Some columns must contain the same values. Test that things fail if they don't
            
        '''
        def do_failed_load(data, col_name, value):
            try:
                tmp_data = data.copy()
                tmp_data.get(col_name)[1] = value
                infile = self.write_file(tmp_data)
                s = ConsumeInputSettings()
                self.assertFalse(s.load_from_file(infile[1]))
            finally:
                os.unlink(infile[1])
        
        data = TestInputSettings.act_data
        do_failed_load(data, 'units', 'tons_ac')
        do_failed_load(data, 'fm_type', 'MEAS-Th')
        do_failed_load(data, 'ecoregion', 'southern')
            

            


