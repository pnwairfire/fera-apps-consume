#-------------------------------------------------------------------------------
# Name:        jenkins_tester.py
# Purpose:     Run regression tests on the jenkins server
#
# Author:      kjells
#
# Created:     21/03/2012
#-------------------------------------------------------------------------------
from subprocess import Popen, PIPE
import os

def check_lines(results):
    ERROR_NUMBER_BAR = 1
    failing_scenarios = []
    for line in results:
        errors = int(line.split()[0])
        if not ERROR_NUMBER_BAR > errors:
            failing_scenarios.append(line)
    return failing_scenarios

def check_results(output):
    NUMBER_OF_TESTS = 13
    results = []
    for line in output:
        if '= failed,' in line:
            results.append(line)

    return_value = False
    if len(results):
        failing_scenarios = check_lines(results)
        intro = "All tests were run" if len(results) == NUMBER_OF_TESTS else "Error not all tests run"
        print("\n{} - {} failures found".format(intro, len(failing_scenarios)))
        if len(failing_scenarios):
            for failure in failing_scenarios:
                print("\t{}".format(failure))
        return_value = (0 == len(failing_scenarios) and len(results) == NUMBER_OF_TESTS)
    else:
        print("\nError - major problem. No comparison results found.\n")
        for item in output:
            print(item)
    return return_value

def remove_file(file):
    if os.path.exists(file):
        os.remove(file)

def run_test():
    OUTFILE = "test_results.txt"
    remove_file(OUTFILE)
    linux_cmd = 'export PYTHONPATH=$PYTHONPATH:./consume && python ./test/test_driver.py'
    windows_cmd = 'set PYTHONPATH=%PYTHONPATH%;%cd%\consume && python ./test/test_driver.py'
    cmd = linux_cmd if os.name == 'posix' else windows_cmd
    cmd += " > {}".format(OUTFILE)
    print(cmd)
    os.system(cmd)
    retval = 1
    if os.path.exists(OUTFILE):
        with open(OUTFILE, 'r') as infile:
            retval = 0 if check_results(infile.readlines()) else 1
    else:
        print("{} failed".format(cmd))

    remove_file(OUTFILE)
    return retval

'''
def run_test():
    print(os.path.abspath(os.curdir))
    linux_cmd = 'export PYTHONPATH=$PYTHONPATH:./consume && python ./test/test_driver.py'
    #windows_cmd = 'set PYTHONPATH=%PYTHONPATH%;%cd%\consume && python .\test\test_driver.py'
    cmd = linux_cmd if os.name == 'posix' else windows_cmd
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell='True')
    stdout, stderr = p.communicate()
    return check_results(stdout)
'''
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
exit(run_test())
