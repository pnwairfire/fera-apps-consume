#-------------------------------------------------------------------------------
# Name:        test_driver.py
# Author:      kjells
# Created:     9/22/2011
# Copyright:   (c) kjells 2011
# Purpose:     Use to generate results and run regression tests.
#-------------------------------------------------------------------------------

# - run via batch file that sets PYTHONPATH correctly
from __future__ import absolute_import
import sys
import os
import random

def pp():
    curdir = os.path.abspath(os.path.curdir)
    pardir = os.path.abspath(os.path.pardir)
    if pardir not in sys.path:
        sys.path.append(pardir)
    if curdir not in sys.path:
        sys.path.append(curdir)
    print(sys.path)

pp()
import consume
from . tester import DataObj as compareCSV

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

LOADINGS_FILES = [
    "test/loadings_numeric.csv",
    "test/loadings_alphanumeric.csv",
    "test/loadings_random.csv",
]
def get_input_file(infile):
    ''' Judge the location of the input file based on its relation to this file
    '''
    here = get_this_location()
    here = here[:-len('test')]
    return os.path.normpath(os.path.join(here, infile))

def wrap_input_display(inputs):
    ''' Print all the inputs with the exception of the fuelbed array
    '''
    if inputs:
        chunks = inputs.split('\n')
        print('')
        for line in chunks:
            if line and not line.startswith('FCCS'):
                print(line)
    else:
        print("\nError: missing input display")

def get_fuelbed_list(consumer):
    ''' The expected values against which we test go to the max below '''
    tmp = [i for i in consumer.FCCS.get_available_fuelbeds()]
    random.shuffle(tmp)
    return tmp

def get_consumption_object(burn_type, loadings_file=LOADINGS_FILES[0]):
    ''' Return a "ready to go" consumption object
    '''
    consumer = consume.FuelConsumption(fccs_file = get_input_file(loadings_file))
    set_defaults(consumer, {'burn_type' : burn_type})
    # run over the reference fuelbeds
    fb_list = get_fuelbed_list(consumer)
    consumer.fuelbed_fccs_ids = fb_list
    return (consumer, fb_list)

def write_columns(results, catagories, stream, first_element, index, header=False):
    out = str(first_element)
    for cat in catagories:
        sorted_keys = sorted(results[cat].keys())
        for key in sorted_keys:
            out += ","
            if not header:
                if cat != 'heat release':
                    out += str(results[cat][key]['total'][index])
                else:
                    out += str(results[cat][key][index])
            else:
                # 'primary live', 'seconday live' occur in multiple catagories,
                #   ensure unique column headings
                if ('primary' in key or 'secondary' in key) or (cat == 'heat release'):
                    key = cat + " " + key
                out += key
    out += '\n'
    stream.write(out)

def write_header(results, catagory_list, stream):
    write_columns(results, catagory_list, stream, 'fuelbed', None, True)

def write_header_emissions(catagory_list, stream):
    out = "fuelbed"
    for i in catagory_list:
        out += "," + i
    out += '\n'
    stream.write(out)

def coerce_if_possible(x):
    try:
        return int(x)
    except:
        return x

def write_csv(results, fb_list, stream):
	# - top-level catagory list
    catagory_list = ['summary', 'canopy', 'ground fuels',
        'litter-lichen-moss', 'nonwoody', 'shrub', 'woody fuels', 'heat release']
    cresults = results['consumption']
    cresults['heat release'] = results['heat release']
    write_header(cresults, catagory_list, stream)
    idx = 0
    for item in fb_list:
        write_columns(cresults, catagory_list, stream, coerce_if_possible(item), idx)
        idx += 1

def write_csv_emissions(results, fb_list, stream):
    # use all the emission keys except 'stratum'
    emissions_keys = sorted(results['emissions'].keys())
    emissions_keys = [key for key in emissions_keys if key != 'stratum']
    cons_keys = sorted(results['consumption']['summary']['total'].keys())
    hr_keys = sorted(results['heat release'].keys())

    # build up the column headers
    columns = []
    for key in cons_keys:
        columns.append("{}_{}".format("cons", key))
    for i in emissions_keys:
        for j in cons_keys:
            columns.append("{}_{}".format(i, j))
    for key in hr_keys:
        columns.append("heat release {}".format(key))

    write_header_emissions(columns, stream)
    idx = 0
    for item in fb_list:
        out = str(coerce_if_possible(item))

        # print the consumption column values
        for key in cons_keys:
            out += "," + str(results['consumption']['summary']['total'][key][idx])
        # print the emission column values
        for i in emissions_keys:
            for j in cons_keys:
                out += "," + str(results['emissions'][i][j][idx])
        # print the heat release column values
        for key in hr_keys:
            out += "," + str(results['heat release'][key][idx])

        out += '\n'
        stream.write(out)
        idx += 1

def run_tests(consumer, fb_list, outfile):
    ''' Run consumption-based tests
    '''
    results = consumer.results()
    write_csv(results, fb_list, outfile)

def set_defaults(consumer, map):
    ''' If a map is supplied, use the values from it (doesn't have to contain all values)
         Otherwise, use the defaults
    '''
    consumer.burn_type = map['burn_type'] if 'burn_type' in map else 'natural'
    consumer.fuelbed_area_acres = map['fuelbed_area_acres'] if 'fuelbed_area_acres' in map else 100
    consumer.fuel_moisture_1000hr_pct = map['fuel_moisture_1000hr_pct'] if 'fuel_moisture_1000hr_pct' in map else 20
    consumer.fuel_moisture_duff_pct = map['fuel_moisture_duff_pct'] if 'fuel_moisture_duff_pct' in map else 20
    consumer.canopy_consumption_pct = map['canopy_consumption_pct'] if 'canopy_consumption_pct' in map else 20
    consumer.shrub_blackened_pct = map['shrub_blackened_pct'] if 'shrub_blackened_pct' in map else 50
    consumer.pile_blackened_pct = map['pile_blackened_pct'] if 'pile_blackened_pct' in map else 90
    consumer.output_units = map['output_units'] if 'output_units' in map else 'tons_ac'
    consumer.fuelbed_ecoregion = map['fuelbed_ecoregion'] if 'fuelbed_ecoregion' in map else ['western']
    if 'activity' == consumer.burn_type:
        set_activity_defaults(consumer, map)

def set_activity_defaults(consumer, map):
    consumer.days_since_rain = map['days_since_rain'] if 'days_since_rain' in map else 20
    consumer.fuel_moisture_10hr_pct = map['fuel_moisture_10hr_pct'] if 'fuel_moisture_10hr_pct' in map else 10
    consumer.fm_type = map['fm_type'] if 'fm_type' in map else 'MEAS-Th'
    consumer.length_of_ignition = map['length_of_ignition'] if 'length_of_ignition' in map else 30
    consumer.slope = map['slope'] if 'slope' in map else 5
    consumer.windspeed = map['windspeed'] if 'windspeed' in map else 5

def run_basic_scenarios():
    ''' Run basic consumption scenarios
    '''
    scenario_list = [['western'], ['southern'], ['boreal'], ['activity']]
    for scene in scenario_list:
        burn_type = 'activity' if 'activity' in scene else 'natural'
        consumer, fb_list = get_consumption_object(burn_type)
        consumer.fuelbed_ecoregion = list(scene) if 'activity' not in scene else ['western']
        if 'activity' in scene:
            set_activity_defaults(consumer, {})
        else:
            consumer.burn_type = 'natural'
        outfilename = out_name("results", "{}_out.csv".format(scene[0]))
        reference_values = out_name("expected", "{}_expected.csv".format(scene[0]))
        run_and_test(consumer, fb_list, outfilename, reference_values)

def run_additional_activity_scenarios():
    activityTwo = {
        'burn_type': 'activity',
        'fuel_moisture_10hr_pct':15,
        'fuel_moisture_1000hr_pct':39,
        'fuelbed_area_acres':10,
        'length_of_ignition':5 }
    activityThree = {
        'burn_type': 'activity',
        'fuel_moisture_10hr_pct':15,
        'fuel_moisture_1000hr_pct':45,
        'fuelbed_area_acres':25 }
    activityFour = {
        'burn_type': 'activity',
        'fuel_moisture_10hr_pct':17,
        'fuel_moisture_1000hr_pct':50,
        'fuelbed_area_acres':100 }
    activityFive = {
        'burn_type': 'activity',
        'fuel_moisture_10hr_pct':25,
        'fuel_moisture_1000hr_pct':55,
        'fuelbed_area_acres':100 }

    scenario_list = [activityTwo, activityThree, activityFour, activityFive]
    counter = 2
    for scene in scenario_list:
        consumer, fb_list = get_consumption_object(scene['burn_type'])
        set_defaults(consumer, scene)
        consumer.fuelbed_ecoregion = ['western']
        outfilename = out_name("results", "{}_out.csv".format(counter))
        reference_values = out_name("expected", "scen{}_activity_expected.csv".format(counter))
        counter += 1
        run_and_test(consumer, consumer.fuelbed_fccs_ids, outfilename, reference_values)

#-------------------------------------------------------------------------------
# Use a new emissions object because switching units causes an internal state
#  problem for subsequent runs. todo ks
#-------------------------------------------------------------------------------
def run_emissions_western():
    consumer, fb_list = get_consumption_object('natural')
    em = consume.Emissions(consumer)
    outfilename ='western_emissions.csv'
    reference_file = "{}_expected.csv".format(outfilename.split('.')[0])
    run_and_test_emissions(em, fb_list, outfilename, reference_file)

def run_emissions_activity():
    consumer, fb_list = get_consumption_object('activity')
    em = consume.Emissions(consumer)
    outfilename ='activity_emissions.csv'
    reference_file = "{}_expected.csv".format(outfilename.split('.')[0])
    run_and_test_emissions(em, fb_list, outfilename, reference_file)

def run_emissions_activity_with_unit_conversion():
    consumer, fb_list = get_consumption_object('activity')
    consumer.fuelbed_ecoregion = ['western']
    em = consume.Emissions(consumer)
    em.output_units = 'kg_ha'
    outfilename ='activity_emissions_kgha.csv'
    reference_file = "{}_expected.csv".format(outfilename.split('.')[0])
    run_and_test_emissions(em, fb_list, outfilename, reference_file)

def run_emissions_activity_with_unit_conversion_and_permute_fuelbed_ids():
    for ffile in [(LOADINGS_FILES[1], 'activity_emissions_kgha_alpha.csv'),
                            (LOADINGS_FILES[2],'activity_emissions_kgha_random.csv')]:
        consumer, fb_list = get_consumption_object('activity', loadings_file=ffile[0])
        consumer.fuelbed_ecoregion = ['western']
        em = consume.Emissions(consumer)
        em.output_units = 'kg_ha'
        outfilename = ffile[1]
        reference_file = "{}_expected.csv".format(outfilename.split('.')[0])
        run_and_test_emissions(em, fb_list, outfilename, reference_file)

#-------------------------------------------------------------------------------
# Currently need consumption-specific and emissions-specific runners
#-------------------------------------------------------------------------------
VERBOSE = True
def run_and_test(consumer, fb_list, outfilename, reference_values):
    wrap_input_display(consumer.display_inputs(print_to_console=False))
    with open(outfilename, 'w') as outfile:
        run_tests(consumer, fb_list, outfile)
    ref = compareCSV(reference_values, console=VERBOSE)
    computed = compareCSV(outfilename, console=VERBOSE)
    (failed, compared) = ref.Compare(computed)
    print("{} = failed, {} compared:\t{}".format(failed, compared, outfilename))

def run_and_test_emissions(emissions, fb_list, outfilename, reference_values):
    wrap_input_display(emissions._cons_object.display_inputs(print_to_console=False))
    oname = out_name("results", outfilename)
    with open(oname, 'w') as outfile:
        results = emissions.results()
        write_csv_emissions(results, fb_list, outfile)
    rname = out_name("expected", reference_values)
    ref = compareCSV(rname, console=VERBOSE)
    computed = compareCSV(oname, console=VERBOSE)
    (failed, compared) = ref.Compare(computed)
    print("{} = failed, {} compared:\t{}".format(failed, compared, outfilename))

def exception_wrapper(func, *args):
    try:
        print("Running {}".format(func.__name__))
        func(*args)
        return 0
    except Exception as e:
        print('\nException running {}'.format(func.__name__))
        print(e)
        return 1

#-------------------------------------------------------------------------------
# Start
#-------------------------------------------------------------------------------
# The emissions database doesn't have data for the 1000, 1001 fuelbeds
#  and we don't have a database/input generator to create the file as yet. When
#  that occurs, we can use the larger file
NORMAL = True
#NORMAL = False

if NORMAL:
    exception_wrapper(run_basic_scenarios)
    exception_wrapper(run_additional_activity_scenarios)

    exception_wrapper(run_emissions_activity_with_unit_conversion)
    exception_wrapper(run_emissions_western)
    exception_wrapper(run_emissions_activity)
    exception_wrapper(run_emissions_activity_with_unit_conversion_and_permute_fuelbed_ids)
else:
    # - debugging
    fuelbed_list = [5]
    #fuelbed_list = get_fuelbed_list(consumer)
    consumer.fuelbed_fccs_ids = fuelbed_list
    run_basic_scenarios(consumer, fuelbed_list)

