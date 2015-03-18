#-------------------------------------------------------------------------------
# Name:        00setup_repo.py
# Purpose:     Clone/update the 2 git repos on which this project depends.
#
# Author:      kjells
#
# Created:     
#-------------------------------------------------------------------------------
import os

EMITCALC = 'emitcalc'
LOOKUP = 'fccs2ef'

def update(update_dir):
    os.chdir(update_dir)
    os.system('git pull')

def get_emissions():
    if not os.path.exists(EMITCALC):
        os.mkdir(EMITCALC)
        os.chdir(EMITCALC)
        cmd = 'git clone https://github.com/pnwairfire/emitcalc.git .'
        os.system(cmd)
        os.chdir('..')
    else:
        update(EMITCALC)
    if not os.path.exists(LOOKUP):
        os.mkdir(LOOKUP)
        os.chdir(LOOKUP)
        cmd = 'git clone https://github.com/pnwairfire/fccs2ef.git .'
        os.system(cmd)
        os.chdir('..')
    else:
        update(LOOKUP)

get_emissions()