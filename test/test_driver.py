#-------------------------------------------------------------------------------
# Name:        test_driver.py
# Author:      kjells
# Created:     9/22/2011
# Copyright:   (c) kjells 2011
# Purpose:     Use to generate results for regression tests.
#-------------------------------------------------------------------------------

# - run via batch file that sets PYTHONPATH correctly
import consume
import sys
from tester import DataObj as compareCSV

def write_columns(results, catagories, stream, first_element, index, header=False):
    out = first_element
    for cat in catagories:
        sorted_keys = sorted(results[cat].keys())
        for key in sorted_keys:
            out += ","
            out += str(results[cat][key]['total'][index]) if not header else key
    out += '\n'
    stream.write(out)

def write_header(results, catagory_list, stream):
    write_columns(results, catagory_list, stream, 'fuelbed', None, True)

def write_csv(results, fuelbed_list, stream):
	# - top-level catagory list
    catagory_list = ['summary', 'canopy', 'ground fuels',
        'litter-lichen-moss', 'nonwoody', 'shrub', 'woody fuels']
    write_header(results, catagory_list, stream)
    for fb_index in xrange(0, len(fuelbed_list)):
        write_columns(results, catagory_list, stream, fuelbed_list[fb_index], fb_index)

def run_tests(consumer, fuelbed_list, outfile):
    results = consumer.results()
    write_csv(results['consumption'], fuelbed_list, outfile)

def SetDefaults(consumer, map):
    consumer.burn_type = map['burn_type'] if 'burn_type' in map else 'natural'
    consumer.fuelbed_area_acres = map['fuelbed_area_acres'] if 'fuelbed_area_acres' in map else 100
    consumer.fuel_moisture_1000hr_pct = map['fuel_moisture_1000hr_pct'] if 'fuel_moisture_1000hr_pct' in map else 20
    consumer.fuel_moisture_duff_pct = map['fuel_moisture_duff_pct'] if 'fuel_moisture_duff_pct' in map else 20
    consumer.canopy_consumption_pct = map['canopy_consumption_pct'] if 'canopy_consumption_pct' in map else 20
    consumer.shrub_blackened_pct = map['shrub_blackened_pct'] if 'shrub_blackened_pct' in map else 50
    consumer.output_units = map['output_units'] if 'output_units' in map else 'tons_ac'
    # - activity specific
    consumer.days_since_rain = map['days_since_rain'] if 'days_since_rain' in map else 20
    consumer.fuel_moisture_10hr_pct = map['fuel_moisture_10hr_pct'] if 'fuel_moisture_10hr_pct' in map else 10
    consumer.fm_type = map['fm_type'] if 'fm_type' in map else 'MEAS-Th'
    consumer.lengthOfIgnition = map['lengthOfIgnition'] if 'lengthOfIgnition' in map else 30
    consumer.slope = map['slope'] if 'slope' in map else 5
    consumer.windspeed = map['windspeed'] if 'windspeed' in map else 5

def run_additional_activity_scenarios(consumer, fuelbed_list):
    activityTwo = {
        'fuel_moisture_10hr_pct':15,
        'fuel_moisture_1000hr_pct':39,
        'fuelbed_area_acres':10,
        'lengthOfIgnition':5 }
    activityThree = {
        'fuel_moisture_10hr_pct':15,
        'fuel_moisture_1000hr_pct':45,
        'fuelbed_area_acres':25 }
    activityFour = {
        'fuel_moisture_10hr_pct':17,
        'fuel_moisture_1000hr_pct':50,
        'fuelbed_area_acres':100 }
    activityFive = {
        'fuel_moisture_10hr_pct':25,
        'fuel_moisture_1000hr_pct':55,
        'fuelbed_area_acres':100 }

    scenario_list = ['activityTwo', 'activityThree', 'activityFour', 'activityFive']
    counter = 2
    for scene in scenario_list:
        SetDefaults(consumer, scene)
        consumer.fuelbed_ecoregion = 'western'
        consumer.burn_type = 'activity'
        outfilename = "activity{}_out.csv".format(counter)
        counter += 1
        reference_values = "activity{}_expected.csv".format(counter)
        run_and_test(consumer, fuelbed_list, outfilename, reference_values)

def run_basic_scenarios(consumer, fuelbed_list):
    scenario_list = ['western', 'southern', 'boreal', 'activity']
    for scene in scenario_list:
        consumer.fuelbed_ecoregion = scene if scene != 'activity' else 'western'
        consumer.burn_type = 'activity' if scene == 'activity' else 'natural'
        outfilename = "{}_out.csv".format(scene)
        reference_values = "{}_Expected.csv".format(scene)
        run_and_test(consumer, fuelbed_list, outfilename, reference_values)

def run_and_test(consumer, fuelbed_list, outfilename, reference_values):
    with open(outfilename, 'w') as outfile:
        run_tests(consumer, fuelbed_list, outfile)
    ref = compareCSV(reference_values, console=False)
    computed = compareCSV(outfilename, console=False)
    (failed, compared) = ref.Compare(computed)
    print("{} = failed, {} compared:\t{}".format(failed, compared, outfilename))



#-------------------------------------------------------------------------------
# Start
#-------------------------------------------------------------------------------
# Current the emissions database doesn't have data for the 1000, 1001 fuelbeds
#  and we don't have a database/input generator to create the file as yet. When
#  that occurs, we can use the larger file
consumer = consume.FuelConsumption(
            #fccs_file = "input_data/fccs_pyconsume_input.xml")
            fccs_file = "../input_data/input_without_1000fb.xml")
SetDefaults(consumer, {})

# run over all the fuelbeds
fuelbed_list = [str(i[0]) for i in consumer.FCCS.data]
consumer.fuelbed_fccs_ids = fuelbed_list

run_basic_scenarios(consumer, fuelbed_list)
run_additional_activity_scenarios(consumer, fuelbed_list)