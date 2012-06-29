import unittest
import os
import cmdline as cmd


class TestCmdline(unittest.TestCase):
    ''' This file tests the consume_batch (wrapper around consume module) command line parser 
    '''
    def setUp(self):
        pass

    def reset_consumer(self):
        pass

    def tearDown(self):
        pass

    def testPassing(self):
        ''' Use consume_batch.py as a file that should always be there
        '''
        p = cmd.ConsumeParser(['app_name_placeholder', 'activity', 'consume_batch.py'])
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.burn_type, 'activity')
        
    def testPassingWithMsgLevel(self):
        ''' Use consume_batch.py as a file that should always be there
        '''
        p = cmd.ConsumeParser(['app_name_placeholder', 'activity', 'consume_batch.py', '-l', '3'])
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.burn_type, 'activity')
        self.assertEqual(p.msg_level, 10)   # - logging.DEBUG
        
    def testPassingWithLoadingsFile(self):
        ''' Use consume_batch.py as a file that should always be there
        '''
        p = cmd.ConsumeParser(['app_name_placeholder', 'activity', 'consume_batch.py', '-f', 'consume_batch.py'])
        self.assertEqual(p.burn_type, 'activity')
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.fuel_loadings_file, os.path.abspath('consume_batch.py'))
        
    def testPassingWithLoadingsFileAndColCfgFile(self):
        ''' Use consume_batch.py as a file that should always be there
        '''
        p = cmd.ConsumeParser(['app_name_placeholder', 'activity', 'consume_batch.py', '-f', 'consume_batch.py', '-x', 'consume_batch.py'])
        self.assertEqual(p.burn_type, 'activity')
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.fuel_loadings_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.col_cfg_file, os.path.abspath('consume_batch.py'))

    def testBadBurnType(self):
        self.assertRaises(cmd.ConsumeParserException, cmd.ConsumeParser, ('bogus', 'consume_batch.py'))

    def testNonExistentFile(self):
        self.assertRaises(cmd.ConsumeParserException, cmd.ConsumeParser, ('activity', 'non_existent.py'))
        
    def testLoadingsFileDoesntExist(self):
        self.assertRaises(cmd.ConsumeParserException, cmd.ConsumeParser, ('activity', 'consume_batch.py', '-f', 'non_existent.py'))
        
    def testColCfgFileDoesntExist(self):
        self.assertRaises(cmd.ConsumeParserException, cmd.ConsumeParser, ('activity', 'consume_batch.py', '-x', 'non_existent.py'))
        
        
        
