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
import pickle

import argparse
import logging

#-------------------------------------------------------------------------------
# Simple command line parser for post_process
#-------------------------------------------------------------------------------
def make_parser():
    ''' This is the parser for the post_process command line
    '''
    # - build the parser
    parser = argparse.ArgumentParser()

    # - specify a pickle file
    parser.add_argument('-p', action='store', nargs=1, dest='pickle_file', metavar='pickle file',
        help='Specify the name of the file with pickled results.')

    # - customize the output column configuration
    parser.add_argument('-x', action='store', nargs=1, dest='col_cfg_file', metavar='output columns',
        help='Specify the output column configuration file.')

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
        self._pickle_file = None
        self._col_cfg_file = None
        self._output_file = None

    def do_parse(self, argv):
        parser = make_parser()
        argv = argv[1:] ### - remove the calling script name
        if 0 == len(argv):
            exit(1)
        else:
            args = parser.parse_args(argv)

            # check for valid input file
            if not args.pickle_file:
                raise(PostProcessException("\nError: A file with pickle results is required."))
            if not self.exists(args.pickle_file[0]):
                raise(PostProcessException("\nError: The file '{}' does not exist.".format(args.pickle_file[0])))
            self._pickle_file = os.path.abspath(args.pickle_file[0])

            if args.col_cfg_file:
                if not self.exists(args.col_cfg_file[0]):
                    raise(PostProcessException("\nError: The column config file '{}' does not exist.".format(args.col_cfg_file[0])))
                self._col_cfg_file = os.path.abspath(args.col_cfg_file[0])

            if args.output_file:
                self._output_file = os.path.abspath(args.output_file[0])

    def exists(self, filename):
        return True if os.path.exists(filename) else False

    @property
    def pickle_file(self): return self._pickle_file
    @property
    def col_cfg_file(self): return self._col_cfg_file
    @property
    def output_file(self): return self._output_file
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
                    assert false, "Malformed line: {}".format(line)
    return retval

def write_results(all_results, outfile, col_cfg_file=None):
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

    if all_results:
        columns_to_print = default_cols
        if col_cfg_file:
            columns_to_print = read_col_cfg_file(col_cfg_file)

        tmp = all_results
        add_these = []
        for col in columns_to_print:
            key = col[0]
            new_key = col[1]
            if tmp.has_key(key):
                add_these.append((new_key, tmp[key]))
        newdf = pan.DataFrame.from_items(add_these)
        newdf.to_csv(outfile, index=False)
    else:
        print("\nError: results file corrupted.\n")

def get_pickled_results(pickle_file):
    results = None
    if os.path.exists(pickle_file):
        results = pickle.load(open(pickle_file, "rb"))
    else:
        print("\nError: results file not found.\n")

    return results

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    parser = PostProcessParser()
    parser.do_parse(sys.argv)
    try:
        write_results(get_pickled_results(parser.pickle_file),
            parser.output_file, col_cfg_file=parser.col_cfg_file)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
