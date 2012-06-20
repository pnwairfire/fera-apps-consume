import unittest
import tempfile as tf
import os
from input_settings import ConsumeInputSettings


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
        def write_file(columns, values):
            tmp_file = tf.mkstemp()
            header = ",".join(columns)
            header += '\n'
            os.write(tmp_file[0], header)
            for line in values:
                out_line = ",".join(line)
                out_line += '\n'
                os.write(tmp_file[0], out_line)
            os.close(tmp_file[0])
            return tmp_file

        def write_simplest_natural():
            cols = ['area', 'burn_type', 'can_con_pct', 'ecoregion', 'fm_1000hr', 'fm_duff', 'fuelbeds', 'shrub_black_pct', 'units']
            row = [['10', 'natural', '20', 'western', '30', '40', '1', '50', 'kg_ha']]
            
            s1 = set(cols)
            s2 = set(ConsumeInputSettings.NaturalSNames)
            s2.add("burn_type")
            s2.add("units")
            self.assertEqual(s1, s2)

            infile = write_file(cols, row)
            s = ConsumeInputSettings()
            print(" ---> {}".format(infile[1]))
            self.assertTrue(s.load_from_file(infile[1]))
            self.assertEqual(s.burn_type, 'natural')
            self.assertEqual(s.units, 'kg_ha')
            self.assertEqual(s.get('area'), 10)
            self.assertEqual(s.get('can_con_pct'), 20)
            self.assertEqual(s.get('ecoregion'), 'western')
            self.assertEqual(s.get('fm_1000hr'), 30)
            self.assertEqual(s.get('fm_duff'), 40)
            self.assertEqual(s.get('fuelbeds'), 1)
            self.assertEqual(s.get('shrub_black_pct'), 50)
            os.unlink(infile[1])

        def write_activity():
            cols = ['area', 'burn_type', 'can_con_pct', 'ecoregion', 'fm_1000hr', 'fm_duff', 'fuelbeds', 'shrub_black_pct', 'units']
            cols.append('slope')
            cols.append('windspeed')
            cols.append('days_since_rain')
            cols.append('fm_10hr')
            cols.append('length_of_ignition')
            row = [
                ['10', 'activity', '20', 'western', '30', '40', '1', '50', 'kg_ha', '5', '10', '3', '20', '30', 'NFDRS-Th'],
                ['15', 'activity', '21', 'western', '35', '35', '2', '45', 'kg_ha', '10', '15', '4', '25', '35', 'NFDRS-Th'],
                ['20', 'activity', '22', 'western', '40', '30', '3', '40', 'kg_ha', '15', '20', '5', '30', '40', 'NFDRS-Th']
                ]
            
            s1 = set(cols)
            s2 = set(ConsumeInputSettings.AllSNames)
            s2.add("burn_type")
            s2.add("units")
            cols.append('fm_type')
            self.assertEqual(s1, s2)

            infile = write_file(cols, row)
            s = ConsumeInputSettings()
            print(" ---> {}".format(infile[1]))
            self.assertTrue(s.load_from_file(infile[1]))
            self.assertEqual(s.burn_type, 'activity')
            self.assertEqual(s.units, 'kg_ha')
            self.assertEqual(s.fm_type, 'NFDRS-Th')
            os.unlink(infile[1])

        write_simplest_natural()            
        write_activity()
            

            


