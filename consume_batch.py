#-------------------------------------------------------------------------------
# Name:        consume_batch.py
# Purpose:     This module wraps the consume module and provides input validation
#              as well as output format specification. Output format can be
#              specified at runtime, or, all calculations can be pickled and the
#              output format chosen later.
#
# Author:      kjells
#
# Created:     10/10/2011
#-------------------------------------------------------------------------------
import consume
import os
import sys
import batch_locator
import cmdline
import pandas as pan
import pickle
import unit_convert

DO_PICKLE_OUTPUT = 'pickle'
DO_RAW_OUTPUT = 'raw'

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

def pickle_output(col_cfg_file):
    ''' use 'pickle' as the argument for the column configuration file
        to simply write out the entire dataset. This allows for loading it
        later when the preferred output format is known
    '''
    return DO_PICKLE_OUTPUT == col_cfg_file.lower().strip() if col_cfg_file else False

def do_raw_output(col_cfg_file):
    ''' use 'raw' as the argument for the column configuration file
        to print the entire dataset with the "flattened" names.
        Useful for debugging and for creating column mapping files.
    '''
    return DO_RAW_OUTPUT == col_cfg_file.lower().strip() if col_cfg_file else False

def can_run():
    ''' Are we in the correct location to run?
    '''
    mod_location = batch_locator.module_path()
    cwd = os.getcwd()
    if mod_location == cwd:
        return True
    else:
        raise(Exception("This program must be run from the location of the exe/script."))

def validate_fuel_loadings(alt_loadings_file):
    ''' Valid currently means that the generator_info element is present
        in the loadings file.
        kjells todo: move this into consume proper?
    '''
    validate = False
    with open(alt_loadings_file, 'r') as infile:
        header = infile.readline()
        valid = True if header.startswith('GeneratorName') else False
    if valid:
        return True
    else:
        print("\n!!! Error !!!\n\t\'{}\' is not a valid fuel loadings file.\n".format(alt_loadings_file))
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

def write_results(all_results, outfile, do_metric, col_cfg_file=None):
    # this is the default set of columns for the output format
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
        ('parameters_pile_black_pct', 'Pile Blackened (%)'),
        ('parameters_units', 'Units') ]

    # calculated results are in a hierarchical dictionary. Flatten the entire structure
    #  so that any chosen datum can be specified
    tmp = {}
    for k,v in flattenDict(all_results).items():
        colname = '_'.join(k)
        colname = colname.replace(' ', '_')
        tmp[colname] = v

    # output format will be done later so simply persist the calculate results
    if pickle_output(col_cfg_file):
        pickle.dump(tmp, open(outfile, 'wb'))
    elif do_raw_output(col_cfg_file):
        for key in sorted(tmp.keys()):
            print('{}:   {}'.format(key, str(tmp[key])))
    else:
        # - pick conversion method
        converter = unit_convert.column_convert if do_metric else unit_convert.column_convert_none

        columns_to_print = default_cols
        if col_cfg_file:
            columns_to_print = read_col_cfg_file(col_cfg_file)

        add_these = []
        for col in columns_to_print:
            key = col[0]
            new_key = col[1]
            if key in tmp.keys():
                add_these.append((new_key, converter(key, tmp[key])))
        newdf = pan.DataFrame.from_items(add_these)
        newdf.to_csv(outfile, index=False)

def run(burn_type, csv_input, do_metric, msg_level, outfile, fuel_loadings=None, col_cfg=None):
    # validate alternate loadings file if provide. Throws exception on invalid
    if fuel_loadings: validate_fuel_loadings(fuel_loadings)

    # obtain a FuelConsumption object
    consumer = consume.FuelConsumption(fccs_file=fuel_loadings, msg_level=msg_level) \
        if fuel_loadings else consume.FuelConsumption(msg_level=msg_level)

    # run the calculator and either pickle results for later output
    #  or output as specified
    consumer.burn_type = burn_type
    if consumer.load_scenario(csv_input, display=False):
        emissions = consume.Emissions(consumer)
        results = emissions.results()
        fuelbed_list = consumer.fuelbed_fccs_ids
        write_results(results, outfile, do_metric, col_cfg_file=col_cfg)
        if not pickle_output(col_cfg):
            print("\nSuccess!!! Results are in \"{}\"".format(outfile))

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    try:
        can_run()
        parser = cmdline.ConsumeParser([DO_PICKLE_OUTPUT, DO_RAW_OUTPUT])
        parser.do_parse(sys.argv)
        run(parser.burn_type, parser.csv_file, parser.do_metric, parser.msg_level, parser.output_filename,
            parser.fuel_loadings_file, parser.col_cfg_file)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()