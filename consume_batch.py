#-------------------------------------------------------------------------------
# Name:        consume_batch.py
# Purpose:
#
# Author:      kjells
#
# Created:     10/10/2011
# Copyright:   (c) kjells 2011
#-------------------------------------------------------------------------------
import consume
import os
import sys
from custom_col import CustomCol
import batch_locator
import cmdline
import pandas as pan

RESULTS_FILE = 'batch_results.csv'

# -- From stackoverflow.com ---
from collections import *
from itertools import *

same = lambda x:x  # identity function
add = lambda a,b:a+b
_tuple = lambda x:(x,)  # python actually has coercion, avoid it like so

def flattenDict(dictionary, keyReducer=add, keyLift=_tuple, init=()):

    # semi-lazy: goes through all dicts but lazy over all keys
    # reduction is done in a fold-left manner, i.e. final key will be
    #     r((...r((r((r((init,k1)),k2)),k3))...kn))

    def _flattenIter(pairs, _keyAccum=init):
        atoms = ((k,v) for k,v in pairs if not isinstance(v, Mapping))
        submaps = ((k,v) for k,v in pairs if isinstance(v, Mapping))
        def compress(k):
            return keyReducer(_keyAccum, keyLift(k))
        return chain(
            (
                (compress(k),v) for k,v in atoms
            ),
            *[
                _flattenIter(submap.items(), compress(k))
                for k,submap in submaps
            ]
        )
    return dict(_flattenIter(dictionary.items()))
# -- end from stackoverflow.com ---

def can_run():
    mod_location = batch_locator.module_path()
    cwd = os.getcwd()
    if mod_location == cwd:
        return True
    else:
        raise(Exception("This program must be run from the location of the exe/script."))

def validate_fuel_loadings(alt_loadings_file):
    ''' Valid currently means that the generator_info element is present
        kjells todo: move this into consume proper?
    '''
    from xml.etree import ElementTree as ET
    tree = ET.parse(alt_loadings_file)
    root = tree.getroot()
    del tree

    node = root.find('generator_info')
    if None != node:
        name = node.find('generator_name')
        version = node.find('generator_version')
        date = node.find('date_generated')
        return True
    return False

def get_input_file(fuel_loadings):
    ''' Judge the location of the input file based on its relation to this file
    '''
    if validate_fuel_loadings(fuel_loadings):
        return fuel_loadings
    else:
        msg.error("\n\'{}\' is not a valid fuel loadings file.\n".format(fuel_loadings))
        sys.exit(1)

def read_col_cfg_file(filename):
    retval = []
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.strip()
            if len(line) and not line.startswith('#'):
                chunks = line.split(',')
                if 2 == len(chunks):
                    retval.append((chunks[0].strip(), chunks[1].strip()))
                else:
                    assert false, "Malformed line: {}".format(line)
    return retval

def write_results(all_results, col_cfg_file=None):
    default_cols = [
        ('parameters_fuelbeds', 'Fuelbeds'),
        ('consumption_summary_total_total', 'Total Consumption'),
        ('consumption_summary_canopy_total', 'Canopy Consumption'),
        ('consumption_summary_ground_fuels_total', 'GroundFuel Consumption'),
        ('consumption_summary_litter-lichen-moss_total', 'LLM Consumption'),
        ('consumption_summary_nonwoody_total', 'NonWoody Consumption'),
        ('consumption_summary_shrub_total', 'Shrub Consumption'),
        ('consumption_summary_woody_fuels_total', 'Woody Consumption'),
        ('emissions_ch4_total', 'CH4 Emissions'),
        ('emissions_co2_total', 'CO2 Emissions'),
        ('emissions_co_total', 'CO Emissions'),
        ('emissions_nmhc_total', 'NMHC Emissions'),
        ('emissions_pm10_total', 'PM10 Emissions'),
        ('emissions_pm25_total', 'PM25 Emissions'),
        ('emissions_pm_total', 'PM Emissions'),
        ('heat_release_total', 'Total Heat Release'),
        ('parameters_area', 'Area'),
        ('parameters_burn_type', 'Burn Type'),
        ('parameters_can_con_pct', 'Canopy Consumption (%)'),
        ('parameters_ecoregion', 'Region'),
        ('parameters_emissions_fac_group', 'Emmissions Factor Group'),
        ('parameters_fm_1000hr', '1000hr Fuel Moisture'),
        ('parameters_fm_duff', 'Duff Fuel Moisture'),
        ('parameters_shrub_black_pct', 'Shrub Blackened (%)'),
        ('parameters_units', 'Units') ]

    columns_to_print = default_cols
    if col_cfg_file:
        columns_to_print = read_col_cfg_file(col_cfg_file)

    tmp = {}
    for k,v in flattenDict(all_results).iteritems():
        colname = '_'.join(k)
        colname = colname.replace(' ', '_')
        tmp[colname] = v
    add_these = []
    for col in columns_to_print:
        key = col[0]
        new_key = col[1]
        if tmp.has_key(key):
            add_these.append((new_key, tmp[key]))
    newdf = pan.DataFrame.from_items(add_these)
    newdf.to_csv(RESULTS_FILE, index=False)

def run(burn_type, csv_input, msg_level, fuel_loadings=None, col_cfg=None):
    consumer = consume.FuelConsumption(fccs_file=fuel_loadings, msg_level=msg_level) \
        if fuel_loadings else consume.FuelConsumption(msg_level=msg_level)
    consumer.burn_type = burn_type
    if consumer.load_scenario(csv_input, display=False):
        emissions = consume.Emissions(consumer)
        results = emissions.results()
        fuelbed_list = consumer.fuelbed_fccs_ids
        write_results(results, col_cfg_file=col_cfg)
        print("\nSuccess!!! Results are in \"{}\"".format(RESULTS_FILE))

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    try:
        can_run()
        parser = cmdline.ConsumeParser(sys.argv)
        run(parser.burn_type, parser.csv_file, parser.msg_level, parser.fuel_loadings_file, parser.col_cfg_file)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
