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
        p = cmd.ConsumeParser()
        p.do_parse(['app_name_placeholder', 'activity', 'consume_batch.py'])
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.burn_type, 'activity')

    def testPassingWithPickle(self):
        ''' Use consume_batch.py as a file that should always be there
        '''
        p = cmd.ConsumeParser('pickle')
        p.do_parse(['app_name_placeholder', 'activity', 'consume_batch.py'])
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.burn_type, 'activity')

    def testPassingWithMsgLevel(self):
        ''' Use consume_batch.py as a file that should always be there
        '''
        p = cmd.ConsumeParser()
        p.do_parse(['app_name_placeholder', 'activity', 'consume_batch.py', '-l', '3'])
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.burn_type, 'activity')
        self.assertEqual(p.msg_level, 10)   # - logging.DEBUG

    def testPassingWithLoadingsFile(self):
        ''' Use consume_batch.py as a file that should always be there
        '''
        p = cmd.ConsumeParser()
        p.do_parse(['app_name_placeholder', 'activity', 'consume_batch.py', '-f', 'consume_batch.py'])
        self.assertEqual(p.burn_type, 'activity')
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.fuel_loadings_file, os.path.abspath('consume_batch.py'))

    def testPassingWithLoadingsFileAndColCfgFile(self):
        ''' Use consume_batch.py as a file that should always be there
        '''
        p = cmd.ConsumeParser()
        p.do_parse(['app_name_placeholder', 'activity', 'consume_batch.py', '-f', 'consume_batch.py', '-x', 'consume_batch.py'])
        self.assertEqual(p.burn_type, 'activity')
        self.assertEqual(p.csv_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.fuel_loadings_file, os.path.abspath('consume_batch.py'))
        self.assertEqual(p.col_cfg_file, os.path.abspath('consume_batch.py'))

    def testBadBurnType(self):
        p = cmd.ConsumeParser()
        try:
            p.do_parse('bogus', 'consume_batch.py')
            self.assertFalse()
        except(cmd.ConsumeParserException):
            pass
        except:
            self.assertFalse

    def testNonExistentFile(self):
        p = cmd.ConsumeParser()
        try:
            p.do_parse('activity', 'non_existent.py')
            self.assertFalse()
        except(cmd.ConsumeParserException):
            pass
        except:
            self.assertFalse

    def testLoadingsFileDoesntExist(self):
        p = cmd.ConsumeParser()
        try:
            p.do_parse('activity', 'consume_batch.py', '-f', 'non_existent.py')
            self.assertFalse()
        except(cmd.ConsumeParserException):
            pass
        except:
            self.assertFalse

    def testColCfgFileDoesntExist(self):
        p = cmd.ConsumeParser()
        try:
            p.do_parse('activity', 'consume_batch.py', '-x', 'non_existent.py')
            self.assertFalse()
        except(cmd.ConsumeParserException):
            pass
        except:
            self.assertFalse



