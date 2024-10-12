#-------------------------------------------------------------------------------
# Name:        test_driver.py
# Author:      kjells
# Created:     9/22/2011
# Copyright:   (c) kjells 2011
# Purpose:     Use to generate results and run regression tests.
#-------------------------------------------------------------------------------

import sys
import os
import random
import traceback

INPUT_FILES_NATURAL = [
    './test/regression_input_southern.csv',
    './test/regression_input_western.csv'
]

INPUT_FILES_ACTIVITY = [
   './test/regression_input_southern-activity.csv',
    './test/regression_input_western-activity.csv'
]

CONSUME_DRIVER = 'consume_batch.py'
TYPE_NATURAL = 'natural'
TYPE_ACTIVITY = 'activity'

def exception_wrapper(func, *args):
    print("Running {}".format(func.__name__))
    try:
        func(*args)
        return 0
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('\nException running {}'.format(func.__name__))
        traceback.print_tb(exc_traceback, limit=-10, file=sys.stdout)
        print('\t{}'.format(e))
        return 1

#-------------------------------------------------------------------------------
# Uncomment to regenerate "expected" output files, comment out test cases below. 
#-------------------------------------------------------------------------------
# for ifile in INPUT_FILES_NATURAL:
#     outfile = './test/expected/regression_expected_{}_sera.csv'.format(ifile.split('_')[-1].split('.')[0])
#     cmd = 'python3.12 {} {} {} -o {}'.format(CONSUME_DRIVER, TYPE_NATURAL, ifile, outfile)
#     print(cmd, '\n')
#     os.system(cmd)
#     outfile = './test/expected/regression_expected_{}_nosera.csv'.format(ifile.split('_')[-1].split('.')[0])
#     cmd = 'python3.12 {} --nosera {} {} -o {}'.format(CONSUME_DRIVER, TYPE_NATURAL, ifile, outfile)
#     print(cmd, '\n')
#     os.system(cmd)
# 
# for ifile in INPUT_FILES_ACTIVITY:
#     outfile = './test/expected/regression_expected_{}_sera.csv'.format(ifile.split('_')[-1].split('.')[0])
#     cmd = 'python3.12 {} {} {} -o {}'.format(CONSUME_DRIVER, TYPE_ACTIVITY, ifile, outfile)
#     print(cmd, '\n')
#     os.system(cmd)
#     outfile = './test/expected/regression_expected_{}_nosera.csv'.format(ifile.split('_')[-1].split('.')[0])
#     cmd = 'python3.12 {} --nosera {} {} -o {}'.format(CONSUME_DRIVER, TYPE_ACTIVITY, ifile, outfile)
#     print(cmd, '\n')
#     os.system(cmd)
# 
# print('\nRecreated expected csv files.')
# exit()

#-------------------------------------------------------------------------------
# Start
#-------------------------------------------------------------------------------
errors = 0
for ifile in INPUT_FILES_NATURAL:
    cmd = 'python3.12 {} {} {}'.format(CONSUME_DRIVER, TYPE_NATURAL, ifile)
    print(cmd, '\n')
    errors += os.system(cmd)
    cmd = 'diff {} {}'.format('./consume_results.csv', './test/expected/regression_expected_{}_sera.csv'.format(ifile.split('_')[-1].split('.')[0]))
    print(cmd, '\n')
    errors += os.system(cmd)
    cmd = 'python3.12 {} --nosera {} {}'.format(CONSUME_DRIVER, TYPE_NATURAL, ifile)
    print(cmd, '\n')
    errors += os.system(cmd)
    cmd = 'diff {} {}'.format('./consume_results.csv', './test/expected/regression_expected_{}_nosera.csv'.format(ifile.split('_')[-1].split('.')[0]))
    print(cmd, '\n')
    errors += os.system(cmd)

for ifile in INPUT_FILES_ACTIVITY:
    cmd = 'python3.12 {} {} {}'.format(CONSUME_DRIVER, TYPE_ACTIVITY, ifile)
    print(cmd, '\n')
    errors += os.system(cmd)
    cmd = 'diff {} {}'.format('./consume_results.csv', './test/expected/regression_expected_{}_sera.csv'.format(ifile.split('_')[-1].split('.')[0]))
    print(cmd, '\n')
    errors += os.system(cmd)
    cmd = 'python3.12 {} --nosera {} {}'.format(CONSUME_DRIVER, TYPE_ACTIVITY, ifile)
    print(cmd, '\n')
    errors += os.system(cmd)
    cmd = 'diff {} {}'.format('./consume_results.csv', './test/expected/regression_expected_{}_nosera.csv'.format(ifile.split('_')[-1].split('.')[0]))
    print(cmd, '\n')
    errors += os.system(cmd)

if errors:
    print('\nFailed !!!\n')
else:
    print('\nSuccess !!!\n')

exit(1 if errors else 0)

