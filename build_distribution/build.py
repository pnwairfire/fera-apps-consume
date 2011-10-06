#-------------------------------------------------------------------------------
# Name:        build.py
# Purpose:     Create the directory structure and copy files to make an installable
#               consume distribution
#
# Author:      kjells
#
# Created:     29/09/2011
# Copyright:   (c) kjells 2011
#-------------------------------------------------------------------------------
import shutil
import os
from contextlib import contextmanager

PKG_DIR = './consume'
PKG_SOURCE_DIR = './consume/consume'
PKG_DATAFILES_DIR = PKG_SOURCE_DIR + '/input_data'

def build_dirs():
    if os.path.exists(PKG_DIR):
        shutil.rmtree(PKG_DIR)
    for dir in [PKG_DIR, PKG_SOURCE_DIR, PKG_DATAFILES_DIR]:
        os.mkdir(dir)

def copy_files(file_list, dest):
    for file in file_list:
        #print("{}\t->\t{}".format(file, dest))
        shutil.copy(file, dest)

def copy_non_source():
    NON_SOURCE_FILES = [
        'AUTHORS.txt',
        'LICENSE.txt',
        'README.txt',
        'setup.py',
        'MANIFEST.in'
    ]
    copy_files(NON_SOURCE_FILES, PKG_DIR)

def copy_source():
    SOURCE_FILES = [
        '../consume/__init__.py',
        '../consume/con_calc_activity.py',
        '../consume/con_calc_natural.py',
        '../consume/data_desc.py',
        '../consume/emissions.py',
        '../consume/emissions_db.py',
        '../consume/fccs_db.py',
        '../consume/fuel_consumption.py',
        '../consume/input_variables.py',
        '../consume/util_consume.py'
    ]
    copy_files(SOURCE_FILES, PKG_SOURCE_DIR)
    all_py_files = [i for i in os.listdir('../consume') if i.endswith('.py')]
    for file in all_py_files:
        if file not in [i.split('/')[2] for i in SOURCE_FILES]:
            print("\n{} is not listed as a source file. It won't be included in the package.".format(file))

def copy_datafiles():
    datafiles = ['../consume/input_data/' + i for i in os.listdir('../consume/input_data')]
    copy_files(datafiles, PKG_DATAFILES_DIR)

def run_setup():
    if os.path.exists(PKG_DIR):
        os.chdir(PKG_DIR)
        CMD = 'python setup.py sdist > NUL'
        os.system(CMD)
        output = os.listdir('./dist')
        if len(output) and 'zip' in output[0]:
            archive = os.path.abspath(os.path.join('./dist', output[0]))
            print("\nSuccess !!!\n\tThe archive is: {}.\n".format(archive))
        else:
            print("\nHmmm... something went wrong building the package.\n")

    else:
        print("\nError: \'{}\' does not exist".format(PKG_DIR))

def change_to_this():
    ''' Return the current working directory. Change to the root of
         the build_distribution directory
    '''
    here = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()
    os.chdir(here)
    return cwd

@contextmanager
def run_enclosed(setup, teardown):
    ''' Encapsulate directory changes
    '''
    cwd = setup()
    yield
    teardown(cwd)


#-------------------------------------------------------------------------------
# Start
#-------------------------------------------------------------------------------
def main():
    with run_enclosed(change_to_this, os.chdir):
        build_dirs()
        copy_source()
        copy_non_source()
        copy_datafiles()
        run_setup()


if __name__ == '__main__':
    main()