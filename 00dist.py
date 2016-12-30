#-------------------------------------------------------------------------------
# Name:        00dist.py
# Purpose:     Build a zip file of the necessary components for consume batch.
#                   NOTE: the intent is that is run from the CI Server
#
# Author:      kjells
#
# Created:     26/04/2013
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import datetime
import zipfile
import os
import shutil
import glob
from glob import iglob # lower memory footprint than glob

DIST_DIR = 'dist'
DISTRIBUTION_BUILDER = '00dist.py'

def make_dist_dir():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.mkdir(DIST_DIR)

def copy_files():
    PYFILES = ['batch_locator.py', 'cmdline.py', 'consume_batch.py', 'post_process.py', 'unit_convert.py']
    for f in PYFILES:
        shutil.copyfile(f, '{}/{}'.format(DIST_DIR, f))
    for f in glob.glob('output*.csv'):
        shutil.copyfile(f, '{}/{}'.format(DIST_DIR, f))
    shutil.copytree('consume', '{}/consume'.format(DIST_DIR))

def make_archive():
    print("In {} ...".format('make_archive'))
    ARCHIVE = "consume.zip"
    
    def clean_files():
        try:
            cmd = "find . -name '*.pyc' -delete"
            os.system(cmd)
            os.unlink(DISTRIBUTION_BUILDER)
        except:
            pass

    def write_archive(archive, filespec):
        dirs = []
        for f in iglob(filespec):
            if os.path.isdir(f):
                dirs.append(f)
                archive.write(f)
            elif not f == ARCHIVE:
                archive.write(f)
        for dir in dirs:
            write_archive(archive, dir + "/*")

    os.chdir(DIST_DIR)
    clean_files()
    archive = zipfile.ZipFile(ARCHIVE, 'w', zipfile.ZIP_DEFLATED)
    write_archive(archive, '*')
    os.chdir('..')



#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    make_dist_dir()
    copy_files()
    make_archive()

if __name__ == '__main__':
    main()
