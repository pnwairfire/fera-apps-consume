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
import traceback
import batch_locator
import cmdline
import pandas as pd
import pickle
import unit_convert
import numpy as np
import time

DO_PICKLE_OUTPUT = 'pickle'
DO_RAW_OUTPUT = 'raw'

PRECISION = 2

# -- From stackoverflow.com ---
import collections.abc as colls
import itertools as it

same = lambda x:x  # identity function
add = lambda a,b:a+b
_tuple = lambda x:(x,)  # python actually has coercion, avoid it like so

def flattenDict(dictionary, keyReducer=add, keyLift=_tuple, init=()):

    # semi-lazy: goes through all dicts but lazy over all keys
    # reduction is done in a fold-left manner, i.e. final key will be
    #     r((...r((r((r((init,k1)),k2)),k3))...kn))

    def _flattenIter(pairs, _keyAccum=init):
        atoms = ((k,v) for k,v in pairs if not isinstance(v, colls.Mapping))
        submaps = ((k,v) for k,v in pairs if isinstance(v, colls.Mapping))
        def compress(k):
            return keyReducer(_keyAccum, keyLift(k))
        return it.chain(
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
        time.sleep(1)    #wait a second, and try again
        with open(alt_loadings_file, 'r') as infile:
            header = infile.readline()
            valid = True if header.startswith('GeneratorName') else False
        if valid:
            return True
        else:
            print("\n!!! Error !!!\n\t\'{}\' Header line missing from fuel loadings file.\n".format(alt_loadings_file))
            print("Example (add to first line of csv): GeneratorName=FCCS 4.0,GeneratorVersion=3.0.0,DateCreated=08/28/2024.\n")
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
                    assert False, "Malformed line: {}".format(line)
    return retval

def write_feps_emissions_input(all_results, feps_input_filename):
    '''
    FEPS expects an input file that looks like this:
        Phase,CO2,CO,CH4,PM25,PM10,NOx,SO2,NH3,VOC,Total
        Flame,598943.21,15372.26,552.77,1829.97,2157.84,0.00,0.00,0.00,669.01,619525.06
        Smold,425497.69,40625.54,2086.30,4798.19,5166.86,0.00,0.00,0.00,1377.66,479552.23
        Resid,501526.64,47997.12,2463.88,5730.09,6153.71,0.00,0.00,0.00,1621.53,565492.98
        Total,1525967.54,103994.91,5102.95,12358.26,13478.41,0.00,0.00,0.00,3668.19,1664570.26

    NOTE: Consume doesn't supply NOx, SO2, or NH3 -- we simply supply 0 for those pollutants.
    '''
    

    LBS_PER_TON = 2000
    '''
    emissions = {
        'Phase' : ['Flame', 'Smold', 'Resid'],
        'CO2' : [np.sum(all_results['emissions_co2_flaming']), np.sum(all_results['emissions_co2_smoldering']),
                    np.sum(all_results['emissions_co2_residual'])],
        'CO' : [np.sum(all_results['emissions_co_flaming']), np.sum(all_results['emissions_co_smoldering']),
                    np.sum(all_results['emissions_co_residual'])],
        'CH4' : [np.sum(all_results['emissions_ch4_flaming']), np.sum(all_results['emissions_ch4_smoldering']),
                    np.sum(all_results['emissions_ch4_residual'])],
        'PM25' : [np.sum(all_results['emissions_pm25_flaming']), np.sum(all_results['emissions_pm25_smoldering']),
                    np.sum(all_results['emissions_pm25_residual'])],
        'PM10' : [np.sum(all_results['emissions_pm10_flaming']), np.sum(all_results['emissions_pm10_smoldering']),
                    np.sum(all_results['emissions_pm10_residual'])],
        'NOx' : [0.0, 0.0, 0.0],
        'SO2' : [0.0, 0.0, 0.0],
        'NH3' : [0.0, 0.0, 0.0],
        'NMHC' : [np.sum(all_results['emissions_nmhc_flaming']), np.sum(all_results['emissions_nmhc_smoldering']),
                    np.sum(all_results['emissions_nmhc_residual'])],
    }
    '''

    # the commented out code above did not consider the percentage area, so FEPS would end up with extremely high
    # values when a burn unit contains multiple fuelbeds. The rates were just summed. Below, the rates are multiplied 
    # by the corresponding area, then divided by the total area, then summed. 
    # Example: Fuelbed 36 100 acres and Fuelbed 4 300 acres... suppose the emissions_pm25_flaming are [12, 24], then
    # the total pm25 flaming rate = (12 * 100)/400 + (24 * 300)/400 = 3 + 18 = 21. 21 is the rate for all 400 acres. 
    # In the old (wrong) code above the rate just added 12 and 24 to get a rate of 36. This would be the rate for 800 acres.   
    total_area = np.sum(all_results['parameters_area'])
    emissions = {
        'Phase' : ['Flame', 'Smold', 'Resid'],
        'CO2' : [np.sum(all_results['emissions_co2_flaming'] * all_results['parameters_area'] / total_area), 
                    np.sum(all_results['emissions_co2_smoldering'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_co2_residual'] * all_results['parameters_area'] / total_area)],
        'CO' : [np.sum(all_results['emissions_co_flaming'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_co_smoldering'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_co_residual'] * all_results['parameters_area'] / total_area)],
        'CH4' : [np.sum(all_results['emissions_ch4_flaming'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_ch4_smoldering'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_ch4_residual'] * all_results['parameters_area'] / total_area)],
        'PM25' : [np.sum(all_results['emissions_pm25_flaming'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_pm25_smoldering'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_pm25_residual'] * all_results['parameters_area'] / total_area)],
        'PM10' : [np.sum(all_results['emissions_pm10_flaming'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_pm10_smoldering'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_pm10_residual'] * all_results['parameters_area'] / total_area)],
        'NOx' : [0.0, 0.0, 0.0],
        'SO2' : [0.0, 0.0, 0.0],
        'NH3' : [0.0, 0.0, 0.0],
        'NMHC' : [np.sum(all_results['emissions_nmhc_flaming'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_nmhc_smoldering'] * all_results['parameters_area'] / total_area),
                    np.sum(all_results['emissions_nmhc_residual'] * all_results['parameters_area'] / total_area)],
    }
    df = pd.DataFrame(emissions)
    df = df[['Phase', 'CO2', 'CO', 'CH4', 'PM25', 'PM10', 'NOx', 'SO2', 'NH3', 'NMHC']]
    pollutants = ['CO2', 'CO', 'CH4', 'PM25', 'PM10', 'NOx', 'SO2', 'NH3', 'NMHC']
    for p in pollutants:
        df[p] /= LBS_PER_TON
    df.to_csv(feps_input_filename, index=False, float_format='%.3f')
    
def round_to(df):
    ''' Our packaged version of Pandas doesn't have round.
    Once we update the following is all that is required
    
    newdf = newdf.round(PRECISION)
    '''
    for col in df.columns:
        if 'fuelbeds' == col or 'filename' == col: continue
        df[col] = np.round(df.get(col), PRECISION)
    return df


def write_results(all_results, outfile, feps_input_filename, do_metric, col_cfg_file=None):
    # calculated results are in a hierarchical dictionary. Flatten the entire structure
    #  so that any chosen datum can be specified
    tmp = {}
    for k,v in flattenDict(all_results).items():
        colname = '_'.join(k)
        colname = colname.replace(' ', '_')
        tmp[colname] = v

    # always write the FEPS emissions input file
    write_feps_emissions_input(tmp, feps_input_filename)

    # Idea: output format will be done later so simply persist the calculated results.
    # I've retained this, but it is no longer the default action. We have a default
    # output formatting file specified in the command line parser.
    if pickle_output(col_cfg_file):
        pickle.dump(tmp, open(outfile, 'wb'))
    # this is for debugging or generating all the keys
    elif do_raw_output(col_cfg_file):
        for key in sorted(tmp.keys()):
            print('{}:   {}'.format(key, str(tmp[key])))
    # This is the common case
    else:
        # - pick conversion method
        converter = unit_convert.column_convert if do_metric else unit_convert.column_convert_none

        if col_cfg_file:
            columns_to_print = read_col_cfg_file(col_cfg_file)
            add_these = []
            for col in columns_to_print:
                key = col[0]
                new_key = col[1]
                if key in tmp.keys():
                    add_these.append((new_key, converter(key, tmp[key])))
            newdf = pd.DataFrame.from_dict(dict(add_these))
#           	 newdf = pd.DataFrame.from_items(add_these)
            newdf = round_to(newdf)

            newdf.to_csv(outfile, index=False)
        else:
            # The command line parser should preclude getting here.
            print("\nError: bad or missing column configuration file!\n")

def write_units(outfile, do_metric):
    cons_units = 'tons_ac'
    emis_units = 'lbs_ac'
    emis_reason = 'no metric flag'
    if do_metric:
        cons_units = 'tonnes_ha'
        emis_units = 'kg_ha'
        emis_reason = 'metric flag'
    d = {'column type': ["Consumption", "Emissions"],
         'Units': [cons_units, emis_units],
         'Reason': [emis_reason, emis_reason],
         'Options': ['tons_ac, tonnes_ha', 'lbs_ac, kg_ha']}
    df = pd.DataFrame(data=d)
    name, ext = os.path.splitext(outfile)
    outfile = name + '_units' + ext
    df.to_csv(outfile, index=False)
    print("\nSuccess!!! Description of units used \"{}\"".format(outfile))


def run(burn_type, csv_input, do_metric, msg_level, outfile, feps_input_filename, fuel_loadings=None, col_cfg=None, no_sera=False):
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
        if no_sera:
            emissions.no_sera = True
        else:
            emissions.no_sera = False

        results = emissions.results()

        write_results(results, outfile, feps_input_filename, do_metric, col_cfg_file=col_cfg)

        write_units(outfile, do_metric)

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
        if parser.no_sera == True:
            print("no_sera is True... run without SERA emissions values")
        
        run(parser.burn_type, parser.csv_file, parser.do_metric, parser.msg_level, parser.output_filename, parser.feps_input_filename,
            parser.fuel_loadings_file, parser.col_cfg_file, parser.no_sera)
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_tb(tb, limit=-5, file=sys.stdout)
        print(e)
        

if __name__ == '__main__':
    main()