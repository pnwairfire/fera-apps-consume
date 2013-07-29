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

PICKLE_OUTPUT = 'consume_pickle.p'
CONSUME_RESULTS = 'consume_results.csv'

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

def get_pickled_results():
    results = None
    if os.path.exists(PICKLE_OUTPUT):
        results = pickle.load(open(PICKLE_OUTPUT, "rb"))
    else:
        print("\nError: results file not found.\n")

    return results

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    col_cfg_file = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        write_results(get_pickled_results(), CONSUME_RESULTS, col_cfg_file=col_cfg_file)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
