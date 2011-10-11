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
import custom_col

def get_this_location():
    ''' Return the absolute directory path for this file
    '''
    return os.path.dirname(os.path.abspath(__file__))

def out_name(dir, filename):
    ''' Return the absolute directory path of this file
         with the supplied directory name and filename appended
    '''
    return os.path.join(
        os.path.join(get_this_location(), dir),
        filename)

def get_input_file():
    ''' Judge the location of the input file based on its relation to this file
    '''
    DATA_INPUT_FILE = "consume/input_data/input_without_1000fb.xml"
    here = get_this_location()
    return os.path.normpath(out_name(here, DATA_INPUT_FILE))

def add_FSRT_cols(parent_col, decider):
    FSRT_ALL = ['flaming', 'smoldering', 'residual', 'total']
    FSRT_TOTAL = ['total']
    choice = FSRT_ALL if 'all' == decider else FSRT_TOTAL
    out = []
    for i in choice:
        out.append("{}~{}".format(parent_col, i))
    return out

def get_simple_cols(results, prefix, include):
    if include:
        return ["{}~{}".format(prefix, i) for i in results.keys()]

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

    do_print(get_simple_cols(all_results['parameters'], 'parameters', cols.parameters_col))
    do_print(get_emissions_cols(all_results['emissions'], cols))
    do_print(get_simple_cols(all_results['heat release'], 'heat_release', cols.heat_release_col.include))
    do_print(get_consumption_cols(all_results['consumption'], cols))

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
    p = get_simple_cols(all_results['parameters'], 'parameters', cols.parameters_col)
    e = get_emissions_cols(all_results['emissions'], cols)
    h = get_simple_cols(all_results['heat release'], 'heat release', cols.heat_release_col.include)
    c = get_consumption_cols(all_results['consumption'], cols)
    keys = [p, e, h, c]
    columns = [subkey for key in keys for subkey in key]
    with open('batch_results.csv', 'w') as outfile:
        write_header(columns, outfile)
        write_computed_results(all_results, columns, fuelbed_list, outfile)

def run(csv_input):
    if os.path.exists(csv_input):
        consumer = consume.FuelConsumption(fccs_file=get_input_file())
        consumer.load_scenario(csv_input)
        emissions = consume.Emissions(consumer)
        results = emissions.results()
        cols = custom_col.CustomCol()
        #print_results(results, cols)
        fuelbed_list = consumer.fuelbed_fccs_ids.value
        write_results(results, cols, fuelbed_list)
    else:
        print("Error: Can't find input file {}".format(csv_input))

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("\nError - Please specify a .csv input file.")

if __name__ == '__main__':
    main()
