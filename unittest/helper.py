#-------------------------------------------------------------------------------
# Name:        helper.py
# Author:      kjells
# Created:     22/06/2011
# Copyright:   (c) kjells 2011
# Purpose:     Unit test helper facilities
#-------------------------------------------------------------------------------
import os

UNITTEST_DIR = 'unittest'
UNITTEST_LOADINGSFILE = 'unittest_loadings.csv'
UNITTEST_INPUTFILE = 'test_input.csv'

def imp(the_file):
    parent_path = ''.format('{}/{}'.format(UNITTEST_DIR, the_file))
    return parent_path if os.path.exists(parent_path) else the_file

def get_test_loadingsfile():
    ''' In-editor unit tests versus command line unit tests have a different
    working directory. Make both work.'''
    return imp(UNITTEST_LOADINGSFILE)

def get_test_inputfile():
    ''' In-editor unit tests versus command line unit tests have a different
    working directory. Make both work.'''
    return imp(UNITTEST_INPUTFILE)
