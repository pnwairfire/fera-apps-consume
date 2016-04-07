#-------------------------------------------------------------------------------
# Name:        helper.py
# Author:      kjells
# Created:     22/06/2011
# Copyright:   (c) kjells 2011
# Purpose:     Unit test helper facilities
#-------------------------------------------------------------------------------
import os

def get_test_loadingsfile():
    """ In-editor unit tests versus command line unit tests have a different
    working directory. Make both work."""
    infile = ""
    if os.path.exists("unittest/test.csv"):
        infile = "unittest/test.csv"
    else:
        infile = "test.csv"
    return infile

def get_test_inputfile():
    """ In-editor unit tests versus command line unit tests have a different
    working directory. Make both work."""
    infile = ""
    if os.path.exists("unittest/test_input.csv"):
        infile = "unittest/test_input.csv"
    else:
        infile = "test_input.csv"
    return infile
