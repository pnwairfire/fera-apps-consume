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
import module_locator

RESULTS_FILE = 'batch_results.csv'

def can_run():
    mod_location = module_locator.module_path()
    cwd = os.getcwd()
    return True if mod_location == cwd else False

def get_input_file():
    ''' Judge the location of the input file based on its relation to this file
    '''
    DATA_INPUT_FILE = "./consume/input_data/input_without_1000fb.xml"
    #return os.path.normpath(DATA_INPUT_FILE)
    return DATA_INPUT_FILE

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

def print_results(all_results, cols):
    def do_print(out):
            if out:
                for i, n in enumerate(out):
                    print("{} - {}".format(i, n))

    p = get_parameter_cols(all_results['parameters'], 'parameters', cols.parameters_col)
    e = get_emissions_cols(all_results['emissions'], cols)
    h = get_heatrelease_cols(all_results['heat release'], 'heat release', cols.heat_release_col)
    c = get_consumption_cols(all_results['consumption'], cols)
    out = []
    if p: out.extend(p)
    if e: out.extend(e)
    if h: out.extend(h)
    if c: out.extend(c)
    do_print(out)

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
        line += fuelbed
        for column in columns:
            line += ','
            line += str(get_column_data(results, column, number))
        line += '\n'
    outfile.write(line)

def write_results(all_results, cols, fuelbed_list):
    p = get_parameter_cols(all_results['parameters'], 'parameters', cols.parameters_col)
    e = get_emissions_cols(all_results['emissions'], cols)
    h = get_heatrelease_cols(all_results['heat release'], 'heat release', cols.heat_release_col)
    c = get_consumption_cols(all_results['consumption'], cols)
    tmp = [p, e, h, c]
    keys = [i for i in tmp if i]    # - only include columns that exist
    columns = [subkey for key in keys for subkey in key] # - flatten into single list
    with open(RESULTS_FILE, 'w') as outfile:
        write_header(columns, outfile)
        write_computed_results(all_results, columns, fuelbed_list, outfile)

def run(csv_input, col_cfg=None):
    consumer = consume.FuelConsumption(fccs_file=get_input_file())
    consumer.load_scenario(csv_input, display=False)
    emissions = consume.Emissions(consumer)
    results = emissions.results()
    cols = CustomCol() if not col_cfg else CustomCol.from_file(col_cfg)
    fuelbed_list = consumer.fuelbed_fccs_ids.value
    write_results(results, cols, fuelbed_list)
    print("\nSuccess!!! Results are in \"{}\"".format(RESULTS_FILE))
    #print_results(results, cols)

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
import cmdline
def main():
    if can_run():
        parser = cmdline.ConsumeParser(sys.argv)
        run(parser.csv_file, parser.col_cfg_file)
    else:
        print("Error: this program must be run from the location of the exe/script.")

if __name__ == '__main__':
    main()
