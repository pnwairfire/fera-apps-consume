#-------------------------------------------------------------------------------
# Name:        post_process.py
# Purpose:     unpickle previously written results and output as directed
#
# Author:      kjells
#
# Created:     10/10/2011
# Copyright:   (c) kjells 2011
#-------------------------------------------------------------------------------
import os
import sys
import pandas as pan
import numpy as np
import pickle
from collections import defaultdict

import argparse
import logging
import unit_convert

FEPS_FILE = 'feps_input_from_consume.csv'

#-------------------------------------------------------------------------------
# Default columns to include in output file. Can be overridden by specifying
#  a column configuration file.
#-------------------------------------------------------------------------------
DEFAULT_COLS = [
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

FEPS_COLS = [
    (['consumption_summary_total_flaming'], 'cons_flm'),
    (['consumption_summary_total_smoldering'], 'cons_sts'),
    (['consumption_summary_total_residual'], 'cons_lts'),
    (['consumption_ground_fuels_duff_upper_total', 'consumption_ground_fuels_duff_lower_total'], 'cons_duff')
]

#-------------------------------------------------------------------------------
# Simple command line parser for post_process
#-------------------------------------------------------------------------------
def make_parser():
    ''' This is the parser for the post_process command line
    '''
    # - build the parser
    parser = argparse.ArgumentParser()

    # - specify a pickle file(s). If multiple, results are combined
    parser.add_argument('-p', action='store', nargs='*', dest='pickle_files', metavar='pickle files',
        help='Specify the name of the file(s) with pickled results. More than one will be combined')

    # - customize the output column configuration
    parser.add_argument('-x', action='store', nargs=1, dest='col_cfg_file', metavar='output columns',
        help='Specify the output column configuration file.')

    # - specify special processing for FEPS input file
    parser.add_argument('--feps', dest='do_feps', action='store_true',
        help='Indicate that a FEPS input file should be generated.')

    # - specify metric conversion for all columns
    parser.add_argument('--metric', dest='do_metric', action='store_true',
        help='Indicate that columns should be converted to metric units.')

    # - specify an output filename
    parser.add_argument('-o', action='store', nargs=1, default=['consume_results.csv'],
        dest='output_file', metavar='output file',
        help='Specify the name of the post_process output file.'
        )
    return parser

class PostProcessException(Exception):
    pass

class PostProcessParser(object):
    ''' Parse the post_process command line arguments
    '''
    def __init__(self):
        self._pickle_files = None
        self._col_cfg_file = None
        self._output_file = None
        self._do_feps = False
        self._do_metric = False

    def do_parse(self, argv):
        parser = make_parser()
        argv = argv[1:] ### - remove the calling script name
        if 0 == len(argv):
            exit(1)
        else:
            args = parser.parse_args(argv)

            # check for valid input file
            if not args.pickle_files:
                raise(PostProcessException("\nError: A file with pickle results is required."))
            for file in args.pickle_files:
                if not self.exists(file):
                    raise(PostProcessException("\nError: The file '{}' does not exist.".format(file)))
            self._pickle_files = [os.path.abspath(i) for i in args.pickle_files]

            if args.col_cfg_file:
                if not self.exists(args.col_cfg_file[0]):
                    raise(PostProcessException("\nError: The column config file '{}' does not exist.".format(args.col_cfg_file[0])))
                self._col_cfg_file = os.path.abspath(args.col_cfg_file[0])

            if args.output_file:
                self._output_file = os.path.abspath(args.output_file[0])

            if args.do_feps:
                self._do_feps = True

            if args.do_metric:
                self._do_metric = True

    def exists(self, filename):
        return True if os.path.exists(filename) else False

    @property
    def pickle_files(self): return self._pickle_files
    @property
    def col_cfg_file(self): return self._col_cfg_file
    @property
    def output_file(self): return self._output_file
    @property
    def do_feps(self): return self._do_feps
    @property
    def do_metric(self): return self._do_metric
#-------------------------------------------------------------------------------
# End command line parser for post_process
#-------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------
# Take a list of unpickled results, grab the correct columms, combine if necessary,
#  and write to output file. You could have a list of results because FFT
#  runs activity and natural scenarios and then combines the results.
#-------------------------------------------------------------------------------
def write_results(all_results, outfile, do_metric, col_cfg_file=None):
    if len(all_results) > 0:
        # pick conversion routine
        converter = unit_convert.column_convert if do_metric else unit_convert.column_convert_none

        # - set up column configuration
        columns_to_print = DEFAULT_COLS
        if col_cfg_file:
            columns_to_print = read_col_cfg_file(col_cfg_file)

        # - loop through the list of results. Use a list to preserve column order
        add_these = []
        for result in all_results:
            current = []
            for col in columns_to_print:
                key = col[0]
                new_key = col[1]
                if result.has_key(key):
                    current.append((new_key, converter(key, result[key])))
            add_these.append(current)

        # assume one result set, but check for a second
        combined = add_these[0]
        if len(add_these) > 1:
            combined = []
            for i, v in enumerate(add_these[0]):
                a = v[1]
                b = add_these[1][i][1]
                combined.append((v[0], np.concatenate((a, b))))

        newdf = pan.DataFrame.from_items(combined)
        newdf.to_csv(outfile, index=False)
    else:
        print("\nError: results file corrupted.\n")

def write_results_feps(all_results, outfile):
    if len(all_results) > 0:
        # - set up column configuration
        columns_to_print = [parse_column_line(i) for i in FEPS_COLS]

        # - loop through the list of results. Use a list to preserve column order
        totals = defaultdict(float)
        for result in all_results:
            print(' - result - ')
            for item in columns_to_print:
                columns_to_sum = item[0]
                summed_columns = 0.0
                for col in columns_to_sum:
                    print(col)
                    summed_columns += result[col]
                new_key = item[1]
                totals[new_key] += np.sum(summed_columns)

        with open(outfile, 'w+') as o:
            for key in totals.keys():
                o.write('{}={}\n'.format(key, totals[key]))
            o.write('moist_duff={}\n'.format(result['parameters_fm_duff'][0]))
    else:
        print("\nError: results file corrupted.\n")

def get_pickled_results(pickle_files):
    results = []
    for file in pickle_files:
        if os.path.exists(file):
            results.append(pickle.load(open(file, "rb")))
        else:
            print("\nError: results file not found.\n")
    return results

def parse_column_line(line):
    retval = ()
    columns_to_sum = line[0]
    column_output_name = line[1].strip()
    retval = ([i.strip() for i in columns_to_sum], column_output_name)
    return retval

def read_col_cfg_special(filename):
    retval = []
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.strip()
            if len(line) and not line.startswith('#'):
                retval.append(parse_column_line(line))
    return retval

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    parser = PostProcessParser()
    parser.do_parse(sys.argv)
    results = get_pickled_results(parser.pickle_files)
    if parser.do_feps:
        try:
            write_results_feps(results, FEPS_FILE)
        except Exception as e:
            print('\nException in write_results_feps() : {}'.format(e))
    try:
        write_results(results, parser.output_file, parser.do_metric, col_cfg_file=parser.col_cfg_file)
    except Exception as e:
        print('\nException in write_results() : {}'.format(e))

if __name__ == '__main__':
    main()
