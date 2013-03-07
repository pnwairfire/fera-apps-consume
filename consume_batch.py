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


RESULTS_FILE = 'batch_results.csv'

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

def add_FSRT_cols(parent_col, decider):
    FSRT_ALL = ['flaming', 'smoldering', 'residual', 'total']
    FSRT_TOTAL = ['total']
    choice = FSRT_ALL if 'all' == decider else FSRT_TOTAL
    out = []
    for i in choice:
        out.append("{}~{}".format(parent_col, i))
    return out

def get_parameter_cols(results, prefix, include):
    if include:
        return ["{}~{}".format(prefix, i) for i in results.keys()]

def get_heatrelease_cols(results, prefix, cols):
    if cols.include:
        return add_FSRT_cols(prefix, cols.detail)

def get_stratum_cols(results, decider):
    out = []
    for i in results.keys():
        for j in results[i].keys():
            subcol = add_FSRT_cols(j, decider)
            for s_col in subcol:
                out.append("stratum~{}~{}".format(i, s_col))
    return out

def get_emissions_cols(results, cols):
    if cols.emissions_col.include:
        parents = [i for i in results.keys()]
        parents.remove('stratum')
        out = []
        for i in parents:
            tmp = ["emissions~{}".format(i) for i in add_FSRT_cols(i, cols.emissions_col.detail)]
            out.extend(tmp)
        if cols.emissions_stratum_col.include:
            tmp = ["emissions~{}".format(i) for i in
                get_stratum_cols(results['stratum'], cols.emissions_stratum_col.detail)]
            out.extend(tmp)
        return out

def get_consumption_cols(results, cols):
    if cols.consumption_col.include:
        parents = [i for i in results.keys()]
        parents.remove('debug')
        out = []
        for i in parents:
            for j in results[i].keys():
                subcol = add_FSRT_cols(j, cols.consumption_col.detail)
                for s_col in subcol:
                    out.append("consumption~{}~{}".format(i, s_col))
        return out


def rename_columns(cols):
    ''' The number of possible output columns is unwieldy and long column names exacerbate
        the problem. Shorten the column names.
    '''
    def ren_parameters_col(col_in):
        col_out = col_in.replace('parameters', "P", 1)
        return col_out.replace("~", "_")

    def ren_emissions_col(col_in):
        col_out = col_in.replace('emissions', "E", 1)
        col_out = col_out.replace('nonwoody', 'nonwood', 1)
        col_out = col_out.replace('woody fuels', 'wood', 1)
        col_out = col_out.replace('litter-lichen-moss', 'llm', 1)
        col_out = col_out.replace('ground fuels', 'ground', 1)
        col_out = col_out.replace('stratum', 'st', 1)
        return col_out.replace("~", "_")

    def ren_consumption_col(col_in):
        col_out = col_in.replace('consumption', "C", 1)
        ##    col_out = col_out.replace('canopy', 'canopy', 1)
        ##    col_out = col_out.replace('shrub', 'shrub', 1)
        col_out = col_out.replace('nonwoody', 'nonwood', 1)
        col_out = col_out.replace('woody fuels', 'wood', 1)
        col_out = col_out.replace('litter-lichen-moss', 'llm', 1)
        col_out = col_out.replace('ground fuels', 'ground', 1)
        col_out = col_out.replace('summary', 'sum', 1)
        return col_out.replace("~", "_")

    def ren_heatrelease_col(col_in):
        col_out = col_in.replace('heat release', "HR", 1)
        return col_out.replace("~", "_")
    #-------------------------------------------------------------------------------
    new_cols = []
    for col in cols:
        new_col = ""
        if col.startswith("p"): new_col = ren_parameters_col(col)
        if col.startswith("c"): new_col = ren_consumption_col(col)
        if col.startswith("e"): new_col = ren_emissions_col(col)
        if col.startswith("h"): new_col = ren_heatrelease_col(col)
        new_cols.append(new_col)
    return new_cols

def order_consumption_cols(cols):
    stratum = ['canopy', 'shrub', 'nonwoody',
        'woody fuels', 'litter-lichen-moss', 'ground fuels', 'summary']
    strata_out = []
    for strata in stratum:
        marker = "consumption~{}".format(strata)
        for col in cols:
            if marker in col:
                strata_out.append(col)
    assert len(strata_out) == len(cols)
    return strata_out

def get_results_list(all_results, cols):
    p = get_parameter_cols(all_results['parameters'], 'parameters', cols.parameters_col)
    c = get_consumption_cols(all_results['consumption'], cols)
    e = get_emissions_cols(all_results['emissions'], cols)
    h = get_heatrelease_cols(all_results['heat release'], 'heat release', cols.heat_release_col)
    if c:
        c = order_consumption_cols(c)
    tmp = [p, c, e, h]
    keys = [i for i in tmp if i]    # - only include columns that exist
    columns = [subkey for key in keys for subkey in key] # - flatten into single list
    return columns

def print_results(all_results, cols):
    def do_print(out):
            if out:
                for i, n in enumerate(out):
                    print("{} - {}".format(i, n))
    columns = get_results_list(all_results, cols)
    do_print(rename_columns(columns))

def write_header(columns, outfile):
    header = 'fuelbed,'
    header += ",".join(columns)
    header += '\n'
    outfile.write(header)

def get_column_data(results, key_string, index):
    keys = key_string.split('~')
    keys = tuple(keys)
    format_str = ""
    for i in keys:
        format_str += "['{}']"
    deref = format_str.format(*keys)
    code = 'results{}[{}]'.format(deref, index)
    try:
        return eval(code)
    except ValueError:
        print "ValueError.", code
    except IndexError:
        code = 'results{}[{}]'.format(deref, 0)
        return eval(code)
    except TypeError:
        print "TypeError.", code
    except:
        print "Unexpected error:", code

def write_computed_results(results, columns, fuelbed_list, outfile):
    line = ""
    for number, fuelbed in enumerate(fuelbed_list):
        line += str(fuelbed)
        for column in columns:
            line += ','
            line += str(get_column_data(results, column, number))
        line += '\n'
    outfile.write(line)

def write_results(all_results, cols, fuelbed_list):
    columns = get_results_list(all_results, cols)
    with open(RESULTS_FILE, 'w') as outfile:
        write_header(rename_columns(columns), outfile)
        write_computed_results(all_results, columns, fuelbed_list, outfile)

def write_results2(all_results, col_cfg_file=None):
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
        ('parameters_units', 'Units')
    ]
    tmp = {}
    for k,v in flattenDict(all_results).iteritems():
        colname = '_'.join(k)
        colname = colname.replace(' ', '_')
        tmp[colname] = v
    add_these = []
    for col in default_cols:
        key = col[0]
        new_key = col[1]
        if tmp.has_key(key):
            add_these.append((new_key, tmp[key]))
    newdf = pan.DataFrame.from_items(add_these)
    newdf.to_csv(RESULTS_FILE, index=False)


def run(burn_type, csv_input, msg_level, fuel_loadings=None, col_cfg=None):
    #consumer = consume.FuelConsumption(fccs_file=get_input_file(fuel_loadings), msg_level=msg_level) \
    consumer = consume.FuelConsumption(fccs_file=fuel_loadings, msg_level=msg_level) \
        if fuel_loadings else consume.FuelConsumption(msg_level=msg_level)
    consumer.burn_type = burn_type
    if consumer.load_scenario(csv_input, display=False):
        emissions = consume.Emissions(consumer)
        results = emissions.results()
        cols = CustomCol() if not col_cfg else CustomCol.from_file(col_cfg)
        fuelbed_list = consumer.fuelbed_fccs_ids
        #write_results(results, cols, fuelbed_list)
        write_results2(results)
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
