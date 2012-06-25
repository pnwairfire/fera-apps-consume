import unittest
import tempfile as tf
import os
from input_settings import ConsumeInputSettings
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
        ''' Add settings and verify completeness '''
        s = ConsumeInputSettings()
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
        self.assertTrue(s.set('fm_10hr', 2))    ### - manufacture a sequence if necessary
        self.assertTrue(s.set('length_of_ignition', [1, 2, 4]))
        self.assertTrue(s.set('area', [1, 2, 4]))
        self.assertTrue(s.set('ecoregion', ['western', 'southern', 'boreal']))
        self.assertTrue(s.set('fm_1000hr', [1, 2, 4]))
        self.assertTrue(s.set('fm_duff', [1, 2, 4]))
        self.assertTrue(s.set('can_con_pct', 4))    ### - manufacture a sequence if necessary
        self.assertTrue(s.set('shrub_black_pct', [1, 2, 4]))
        #self.assertTrue(s.set('efg', [1, 2, 4]))
        s.fm_type = 'MEAS-Th'
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
        #self.assertTrue(s.set('efg', [1, 2, 4]))
        s.fm_type = 'MEAS-Th'
        s.units = 'kg_ha'
        result = s.display_settings()
        ### - todo, no test here yet

    '''
    ActivityInputVarParameters = {
        'slope' : ['Slope (%)',  [0,100], validate_range],
        'windspeed' : ['Mid-flame windspeed (mph)', [0, 35], validate_range],
        'days_since_rain' : ['Days since sgnf. rainfall', [0,365], validate_range],
        'fm_10hr' : ['Fuel moisture (10-hr, %)', [0,100], validate_range],
        'length_of_ignition' : ['Length of ignition (min.)', [0,10000], validate_range]}
    NaturalInputVarParameters = {
        'fuelbeds' : ['FCCS fuelbeds (ID#)', [1,10000], validate_range],
        'area' : ['Fuelbed area (acres)', [0,1000000], validate_range],
        'ecoregion' : ['Fuelbed ecoregion',  dd.list_valid_ecoregions(), validate_list],
        'fm_1000hr' : ['Fuel moisture (1000-hr, %)', [0,140], validate_range],
        'fm_duff' : ['Fuel moisture (duff, %)', [0,400], validate_range],
        'can_con_pct' : ['Canopy consumption (%)', [0,100], validate_range],
        'shrub_black_pct' : ['Shrub blackened (%)', [0,100], validate_range],
        }
    '''

    def testLoadFromFile(self):        
        ### - natural test data
        ncols = ['area', 'burn_type', 'can_con_pct', 'ecoregion', 'fm_1000hr', 'fm_duff', 'fuelbeds', 'shrub_black_pct', 'units']
        nrows = [
            ['10', 'natural', '20', 'western', '30', '40', '1', '50', 'kg_ha'],
            ['20', 'natural', '30', 'western', '40', '50', '1', '60', 'kg_ha']]
            
        ### - activity test data
        acols = ['area', 'burn_type', 'can_con_pct', 'ecoregion', 'fm_1000hr', 'fm_duff', \
            'fuelbeds', 'shrub_black_pct', 'units', 'slope', 'windspeed', 'days_since_rain', \
            'fm_10hr', 'length_of_ignition', 'fm_type']
        arows = [
            ['10', 'activity', '20', 'western', '30', '40', '1', '50', 'kg_ha', '5', '10', '3', '20', '30', 'NFDRS-Th'],
            ['15', 'activity', '21', 'western', '35', '35', '2', '45', 'kg_ha', '10', '15', '4', '25', '35', 'NFDRS-Th'],
            ['20', 'activity', '22', 'western', '40', '30', '3', '40', 'kg_ha', '15', '20', '5', '30', '40', 'NFDRS-Th']
            ]
            
        nat_data = pan.DataFrame(nrows, columns=ncols)
        act_data =  pan.DataFrame(arows, columns=acols)
       
        def write_file(in_data):
            tmp_file = tf.mkstemp()
            in_data.to_csv(tmp_file[1], index=False)
            os.close(tmp_file[0])
            return tmp_file

        def load_natural():
            ''' Write a temp file, load the temp file and verify that the settings are equal to the 
                values written. Close tempfile
            '''
            s1 = set(nat_data.columns)
            s2 = set(ConsumeInputSettings.NaturalSNames)
            s2.add("burn_type")
            s2.add("units")
            self.assertEqual(s1, s2)

            infile = write_file(nat_data)
            s = ConsumeInputSettings()
            self.assertTrue(s.load_from_file(infile[1]))
            self.assertEqual(s.burn_type, 'natural')
            self.assertEqual(s.units, 'kg_ha')
            self.assertEqual(list(s.get('area')), [float(x) for x in list(nat_data.area)])
            self.assertEqual(list(s.get('can_con_pct')), [float(x) for x in list(nat_data.can_con_pct)])
            self.assertEqual(list(s.get('ecoregion')), list(nat_data.ecoregion))
            self.assertEqual(list(s.get('fm_1000hr')), [float(x) for x in list(nat_data.fm_1000hr)])
            self.assertEqual(list(s.get('fm_duff')), [float(x) for x in list(nat_data.fm_duff)])
            self.assertEqual(list(s.get('fuelbeds')), [float(x) for x in list(nat_data.fuelbeds)])
            self.assertEqual(list(s.get('shrub_black_pct')), [float(x) for x in list(nat_data.shrub_black_pct)])
            os.unlink(infile[1])

        def load_activity():
            ''' Write a temp file, load the temp file and verify that the settings are equal to the 
                values written. Close tempfile
            '''
            s1 = set(act_data.columns)
            s2 = set(ConsumeInputSettings.AllSNames)
            s2.add("burn_type")
            s2.add("units")
            s2.add("fm_type")
            self.assertEqual(s1, s2)

            infile = write_file(act_data)
            s = ConsumeInputSettings()
            self.assertTrue(s.load_from_file(infile[1]))
            self.assertEqual(s.burn_type, 'activity')
            self.assertEqual(s.units, 'kg_ha')
            self.assertEqual(s.fm_type, 'NFDRS-Th')

            self.assertEqual(list(s.get('area')), [float(x) for x in list(act_data.area)])
            self.assertEqual(list(s.get('can_con_pct')), [float(x) for x in list(act_data.can_con_pct)])
            self.assertEqual(list(s.get('ecoregion')), list(act_data.ecoregion))
            self.assertEqual(list(s.get('fm_1000hr')), [float(x) for x in list(act_data.fm_1000hr)])
            self.assertEqual(list(s.get('fm_duff')), [float(x) for x in list(act_data.fm_duff)])
            self.assertEqual(list(s.get('fuelbeds')), [float(x) for x in list(act_data.fuelbeds)])
            self.assertEqual(list(s.get('shrub_black_pct')), [float(x) for x in list(act_data.shrub_black_pct)])

            self.assertEqual(list(s.get('slope')), [float(x) for x in list(act_data.slope)])
            self.assertEqual(list(s.get('windspeed')), [float(x) for x in list(act_data.windspeed)])
            self.assertEqual(list(s.get('days_since_rain')), [float(x) for x in list(act_data.days_since_rain)])
            self.assertEqual(list(s.get('fm_10hr')), [float(x) for x in list(act_data.fm_10hr)])
            self.assertEqual(list(s.get('length_of_ignition')), [float(x) for x in list(act_data.length_of_ignition)])
            
            os.unlink(infile[1])
        # - Start function ----------------------------------------------------
        load_natural()            
        load_activity()
            

            


