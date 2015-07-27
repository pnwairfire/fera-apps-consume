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
import pandas as pd
import numpy as np
import pickle
from collections import defaultdict
import re

import argparse
import logging
import unit_convert

CONSUME_RESULTS = 'consume_results.csv'
FEPS_FILE = 'feps_input_from_consume.csv'

#-------------------------------------------------------------------------------
# Simple command line parser for post_process
#-------------------------------------------------------------------------------
def make_parser():
    ''' This is the parser for the post_process command line
    '''
    # - build the parser
    parser = argparse.ArgumentParser()

    # - specify a pickle file(s). If multiple, results are combined
    parser.add_argument('-r', action='store', nargs='*', dest='results_files', metavar='results files',
        help='Specify the name of the file(s) with results. More than one will be combined')

    # - specify metric conversion for all columns
    parser.add_argument('--metric', dest='do_metric', action='store_true',
        help='Indicate that columns should be converted to metric units.')

    # - specify an output filename
    parser.add_argument('-o', action='store', nargs=1, default=[CONSUME_RESULTS],
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
        self._results_files = None
        self._col_cfg_file = None
        self._output_file = None
        self._do_metric = False

    def do_parse(self, argv):
        parser = make_parser()
        argv = argv[1:] ### - remove the calling script name
        if 0 == len(argv):
            exit(1)
        else:
            args = parser.parse_args(argv)

            # check for valid input file
            if not args.results_files:
                raise(PostProcessException("\nError: A file with results is required."))
            for file in args.results_files:
                if not self.exists(file):
                    raise(PostProcessException("\nError: The file '{}' does not exist.".format(file)))
            self._results_files = [os.path.abspath(i) for i in args.results_files]

            if args.output_file:
                self._output_file = os.path.abspath(args.output_file[0])

            if args.do_metric:
                self._do_metric = True

    def exists(self, filename):
        return True if os.path.exists(filename) else False

    @property
    def results_files(self): return self._results_files
    @property
    def col_cfg_file(self): return self._col_cfg_file
    @property
    def output_file(self): return self._output_file
    @property
    def do_metric(self): return self._do_metric
#-------------------------------------------------------------------------------
# End command line parser for post_process
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Custom sorting strategy. Needs to stay in sync with FFT
#-------------------------------------------------------------------------------
def sort_fuelbeds(df):
    ''' Fuelbed number is actually a string and can be anything. However, to get nicer sorting
        we are using the following strategy:
            - try to break the string into an initial numeric component and a string remainder
            - sort on the components
        To sort the dataframe you need to add a column that ties the sorting strategy to an existing
        column. Then you sort by the ranking column (the one you added).
    '''
    def sort_chunkify(s):
        ''' Break into numeric and other '''
        m = re.match('^([0-9]+)(.*$)', s)
        retval = (sys.maxsize, s, s)
        if m:
            if 2 == m.lastindex:
                retval = (int(m.group(1)), m.group(2), s)
        return retval

    def sort_sort_and_flatten(results):
        ''' Incoming argument is a dictionary of lists:
            - the keys are the numeric component, sort them
            - if the value portion has more than one element sort that list
            - add single or sorted lists
        '''
        flattened = []
        for key in sorted(results.keys()):
            if 1 == len(results[key]):
                flattened.extend(results[key])
            else:
                flattened.extend(sorted(results[key], key=lambda tup: tup[1]))
        return flattened

    result = {}
    df[['Fuelbeds']] = df[['Fuelbeds']].astype(str)
    for item in df.Fuelbeds:
        chunked = sort_chunkify(str(item))
        if chunked[0] in result.keys():
            result[chunked[0]].append(chunked)
        else:
            result[chunked[0]] = [chunked]
    sorted_list = sort_sort_and_flatten(result)
    ranking_column = dict([(v[2], i) for i, v in enumerate(sorted_list)])
    df['Fb_Rank'] = df.Fuelbeds.map(ranking_column)
    df.sort(['Fb_Rank'], inplace = True)
    return df.drop('Fb_Rank', 1)

#-------------------------------------------------------------------------------
# Take a list of results, combine if necessary. You could have a list of results because FFT
#  runs activity and natural scenarios and then combines the results.
#-------------------------------------------------------------------------------
def get_combined_results(all_results):
    df = None
    if len(all_results) > 0:
        df = pd.read_csv(all_results[0])
        if 2 == len(all_results):
            df2 = pd.read_csv(all_results[1])
            df = pd.concat([df, df2])
        df = sort_fuelbeds(df)
    else:
        print("\nError: results file corrupted.\n")
    return df

def write_results_feps(results, directory):
    df = pd.DataFrame({
        'Fuelbeds': results.get('Fuelbeds'),
        'cons_flm': results.get('C_total_F'),
        'cons_sts': results.get('C_total_S'),
        'cons_lts': results.get('C_total_R'),
        'cons_duff_upper': results.get('C_upperduff'),
        'cons_duff_lower': results.get('C_lowerduff')
    })
    try:
        feps_file = os.path.join(directory, FEPS_FILE)
        df.to_csv(feps_file, index=False)
    except Exception as e:
        print('\nException in write_results_feps() : {}'.format(e))

def parse_column_line(line):
    retval = ()
    columns_to_sum = line[0]
    column_output_name = line[1].strip()
    retval = ([i.strip() for i in columns_to_sum], column_output_name)
    return retval

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    parser = PostProcessParser()
    parser.do_parse(sys.argv)
    results = get_combined_results(parser.results_files)
    write_results_feps(results, os.path.split(parser.results_files[0])[0])
    results.to_csv(parser.output_file, index=False)

if __name__ == '__main__':
    main()
