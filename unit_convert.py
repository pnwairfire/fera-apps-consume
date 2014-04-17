#-------------------------------------------------------------------------------
# Name:        unit_convert.py
# Purpose:     Do metric conversion from english units
#
# Author:      kjells
#
# Created:     17/04/2014
# Copyright:   (c) kjells 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

# from google
CONS_CONV = 2.24170231

# from google
EMIS_CONV = 1.12085116

# http://www.translatorscafe.com/cafe/EN/units-converter/heat-flux-density/2-23/kilowatt%2Fmeter%C2%B2-Btu_(th)%2Fhour%2Ffoot%C2%B2/
HEATRELEASE_CONV = 0.1892754465477

def column_convert_none(colname, col):
    return col

def column_convert(colname, col):
    cname = colname[:4]
    if 'cons' == cname:
        return col*CONS_CONV
    elif 'emis' == cname:
        return col*EMIS_CONV
    elif 'heat' == cname:
        return col*HEATRELEASE_CONV
    else:
        return col

def main():
    pass

if __name__ == '__main__':
    main()