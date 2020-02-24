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

TONS_PER_ACRE_TO_MG_PER_ACRE = 2.24170231  # tons/acre to Mg/ha
LBS_PER_ACRE_TO_KG_PER_HA = 1.12085116

unit_conversion_dict = {
'c_total': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_canopy': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_shrub': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_herb': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_llm': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_ground': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_total_f': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_canopy_f': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_shrub_f': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_herb_f': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_f': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_llm_f': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_ground_f': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_total_s': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_canopy_s': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_shrub_s': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_herb_s': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_s': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_llm_s': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_ground_s': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_total_r': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_canopy_r': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_r': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_llm_r': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_ground_r': TONS_PER_ACRE_TO_MG_PER_ACRE,
'ch4': LBS_PER_ACRE_TO_KG_PER_HA,
'co': LBS_PER_ACRE_TO_KG_PER_HA,
'co2': LBS_PER_ACRE_TO_KG_PER_HA,
'nh3': LBS_PER_ACRE_TO_KG_PER_HA,
'nmhc': LBS_PER_ACRE_TO_KG_PER_HA,
'nmoc': LBS_PER_ACRE_TO_KG_PER_HA,
'no': LBS_PER_ACRE_TO_KG_PER_HA,
'no2': LBS_PER_ACRE_TO_KG_PER_HA,
'nox': LBS_PER_ACRE_TO_KG_PER_HA,
'so2': LBS_PER_ACRE_TO_KG_PER_HA,
'pm': LBS_PER_ACRE_TO_KG_PER_HA,
'pm10': LBS_PER_ACRE_TO_KG_PER_HA,
'pm25': LBS_PER_ACRE_TO_KG_PER_HA,
'e_ch4_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_co_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_co2_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nh3_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nmhc_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nmoc_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_no_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_no2_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nox_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_so2_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_pm_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_pm10_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_pm25_f': LBS_PER_ACRE_TO_KG_PER_HA,
'e_ch4_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_co_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_co2_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nh3_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nmhc_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nmoc_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_no_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_no2_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nox_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_so2_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_pm_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_pm10_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_pm25_s': LBS_PER_ACRE_TO_KG_PER_HA,
'e_ch4_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_co_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_co2_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nh3_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nmhc_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nmoc_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_no_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_no2_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_nox_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_so2_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_pm_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_pm10_r': LBS_PER_ACRE_TO_KG_PER_HA,
'e_pm25_r': LBS_PER_ACRE_TO_KG_PER_HA,
'c_overstory_crown': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_midstory_crown': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_understory_crown': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_snagc1f_crown': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_snagc1f_wood': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_snagc1_wood': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_snagc2_wood': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_snagc3_wood': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_ladder': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_shrub_1live': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_shrub_2live': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_herb_1live': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_herb_2live': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_piles': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_1hr': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_10hr': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_100hr': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_s1000hr': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_r1000hr': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_s10khr': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_r10khr': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_s+10khr': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_wood_r+10khr': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_stump_sound': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_stump_rotten': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_stump_lightered': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_litter': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_lichen': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_moss': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_upperduff': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_lowerduff': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_basal': TONS_PER_ACRE_TO_MG_PER_ACRE,
'c_squirrel': TONS_PER_ACRE_TO_MG_PER_ACRE,
'ch4_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'ch4_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'ch4_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'ch4_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'ch4_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'ch4_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'co_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'co_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'co_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'co_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'co_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'co_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'co2_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'co2_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'co2_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'co2_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'co2_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'co2_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'nh3_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'nh3_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'nh3_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'nh3_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'nh3_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'nh3_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'nmhc_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'nmhc_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'nmhc_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'nmhc_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'nmhc_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'nmhc_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'nmoc_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'nmoc_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'nmoc_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'nmoc_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'nmoc_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'nmoc_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'no_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'no_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'no_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'no_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'no_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'no_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'no2_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'no2_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'no2_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'no2_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'no2_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'no2_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'nox_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'nox_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'nox_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'nox_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'nox_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'nox_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'so2_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'so2_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'so2_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'so2_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'so2_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'so2_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'pm_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'pm_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'pm_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'pm_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'pm_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'pm_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'pm10_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'pm10_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'pm10_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'pm10_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'pm10_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'pm10_ground': LBS_PER_ACRE_TO_KG_PER_HA,
'pm25_canopy': LBS_PER_ACRE_TO_KG_PER_HA,
'pm25_shrub': LBS_PER_ACRE_TO_KG_PER_HA,
'pm25_herb': LBS_PER_ACRE_TO_KG_PER_HA,
'pm25_wood': LBS_PER_ACRE_TO_KG_PER_HA,
'pm25_llm': LBS_PER_ACRE_TO_KG_PER_HA,
'pm25_ground': LBS_PER_ACRE_TO_KG_PER_HA
}




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
    df[['fuelbeds']] = df[['fuelbeds']].astype(str)
    for item in df.fuelbeds:
        chunked = sort_chunkify(str(item))
        if chunked[0] in result.keys():
            result[chunked[0]].append(chunked)
        else:
            result[chunked[0]] = [chunked]
    sorted_list = sort_sort_and_flatten(result)
    ranking_column = dict([(v[2], i) for i, v in enumerate(sorted_list)])
    df['Fb_Rank'] = df.fuelbeds.map(ranking_column)
    #df.sort(['Fb_Rank'], inplace = True)
    df.sort_values(by=['Fb_Rank'], inplace = True)
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
        'fuelbeds': results.get('fuelbeds'),
        'cons_flm': results.get('c_total_f'),
        'cons_sts': results.get('c_total_s'),
        'cons_lts': results.get('c_total_r'),
        'cons_duff_upper': results.get('c_upperduff'),
        'cons_duff_lower': results.get('c_lowerduff')
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

	
def convert_units(all_results, do_metric):
    if do_metric: 
        if len(all_results) > 0:
            for result in all_results:
#                print(result)
                if result in unit_conversion_dict:
#                    print("MATCH FOUND =================")
#                    print(all_results[result])
#                    print(unit_conversion_dict[result])
                    all_results[result] *= unit_conversion_dict[result]
#                    print(all_results[result])
            return all_results
        else:	
            print("\nError: results file corrupted.\n")
    else:
        return all_results

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    parser = PostProcessParser()
    parser.do_parse(sys.argv)
    results = get_combined_results(parser.results_files)
    results = convert_units(results, parser.do_metric)
    write_results_feps(results, os.path.split(parser.results_files[0])[0])
    results.to_csv(parser.output_file, index=False)

if __name__ == '__main__':
    main()
