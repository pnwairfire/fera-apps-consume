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

# (1 ton/acre)*(2.471052 acre/ha)*(907.1847 kg/ton) = 2241.70231 kg/ha
# (2241.70231 kg/ha)*(1 ha/10000m^2) = .224170231 kg/m^2
# (.224170231 kg/m^2)*(1Mg / 1000kg)*(10000m^2/1ha) = 2.24170231 Mg/ha (aka tonnes/ha)

CONS_CONV = 2.24170231 

# from google  (1 lb_ac = 1.12085116 kg_ha)
EMIS_CONV = 1.12085116

# http://www.translatorscafe.com/cafe/EN/units-converter/heat-flux-density/2-23/kilowatt%2Fmeter%C2%B2-Btu_(th)%2Fhour%2Ffoot%C2%B2/
HEATRELEASE_CONV = 0.1892754465477

def column_convert_none(colname, col):
    return col

# if --metric flag is used, the emissions will get converted from lbs_ac to kg_ha
# and consumption columns get converted from tons_ac to Mg_ha (aka tonnes_ha)
# note the "units" column in the input file is ignored
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