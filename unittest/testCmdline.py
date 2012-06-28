import unittest
import os
import cmdline as cmd


class TestCmdline(unittest.TestCase):

    def setUp(self):
        pass

    def reset_consumer(self):
        pass

    def tearDown(self):
        pass

    def testPassing(self):
        p = cmd.ConsumeParser(['app_name_placeholder', 'activity', 'consume_batch.py'])
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.burn_type, 'activity')
        
    def testPassingWithLoadingsFile(self):
        p = cmd.ConsumeParser(['app_name_placeholder', 'activity', 'consume_batch.py', '-f', 'consume_batch.py'])
        self.assertEqual(p.burn_type, 'activity')
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.fuel_loadings_file, os.path.abspath('consume_batch.py'))
        
    def testPassingWithLoadingsFileAndColCfgFile(self):
        p = cmd.ConsumeParser(['app_name_placeholder', 'activity', 'consume_batch.py', '-f', 'consume_batch.py', '-x', 'consume_batch.py'])
        self.assertEqual(p.burn_type, 'activity')
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.fuel_loadings_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.col_cfg_file, os.path.abspath('consume_batch.py'))

    def testBadBurnType(self):
        self.assertRaises(cmd.ConsumeParserException, cmd.ConsumeParser, ('bogus', 'consume_batch.py'))

    def testBadFileType(self):
        self.assertRaises(cmd.ConsumeParserException, cmd.ConsumeParser, ('activity', 'non_existent.py'))
        
    def testLoadingsFileDoesntExistType(self):
        self.assertRaises(cmd.ConsumeParserException, cmd.ConsumeParser, ('activity', 'consume_batch.py', '-f', 'non_existent.py'))
        
    def testColCfgFileDoesntExistType(self):
        self.assertRaises(cmd.ConsumeParserException, cmd.ConsumeParser, ('activity', 'consume_batch.py', '-x', 'non_existent.py'))
        
        
        