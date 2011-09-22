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

activityZero = {
    'fuel_moisture_10hr_pct':15,
    'fuel_moisture_1000hr_pct':39,
    'fuelbed_area_acres':10,
    'lengthOfIgnition':5
    }

activityTwo = {
    'fuel_moisture_10hr_pct':15,
    'fuel_moisture_1000hr_pct':45,
    'fuelbed_area_acres':25,
    }

activityThree = {
    'fuel_moisture_10hr_pct':17,
    'fuel_moisture_1000hr_pct':50,
    'fuelbed_area_acres':100,
    }

activityFour = {
    'fuel_moisture_10hr_pct':25,
    'fuel_moisture_1000hr_pct':55,
    'fuelbed_area_acres':100,
    }

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

scenario_list = ['western', 'southern', 'boreal', 'activity']
for scene in scenario_list:
    consumer.fuelbed_ecoregion = scene if scene != 'activity' else 'western'
    consumer.burn_type = 'activity' if scene == 'activity' else 'natural'
    outfilename = "{}_out.csv".format(scene)
    with open(outfilename, 'w') as outfile:
        run_tests(consumer, fuelbed_list, outfile)
    reference_values = "{}_Expected.csv".format(scene)
    ref = compareCSV(reference_values, console=False)
    computed = compareCSV(outfilename, console=False)
    (failed, compared) = ref.Compare(computed)
    print("{}: failed = {} compared = {}".format(outfilename, failed, compared))







##class Driver(object):
##    """ Drive consume object for testing purposes
##    """
##    def __init__(self):
##        self._consumer = consume.FuelConsumption(
##            #fccs_file = "input_data/fccs_pyconsume_input.xml")
##            fccs_file = "input_data/input_without_1000fb.xml")
##
##
##    def _reset_activity_scenario(self):
##        self._consumer.fuel_moisture_10hr_pct = 15
##        self._consumer.fuel_moisture_1000hr_pct = 39
##        self._consumer.fuelbed_area_acres = 10
##        self._consumer.lengthOfIgnition = 5
##
##    def _reset_activity_scenario2(self):
##        self._consumer.fuel_moisture_10hr_pct = 15
##        self._consumer.fuel_moisture_1000hr_pct = 45
##        self._consumer.fuelbed_area_acres = 25
##
##    def _reset_activity_scenario3(self):
##        self._consumer.fuel_moisture_10hr_pct = 17
##        self._consumer.fuel_moisture_1000hr_pct = 50
##        self._consumer.fuelbed_area_acres = 100
##
##    def _reset_activity_scenario4(self):
##        self._consumer.fuel_moisture_10hr_pct = 25
##        self._consumer.fuel_moisture_1000hr_pct = 55
##        self._consumer.fuelbed_area_acres = 100
##
##
##    def write_header(self, results, catagory_list, stream):
##        out = "fuelbed"
##        for i in catagory_list:
##            ### - this needs to stay in sync with the way the data is printed
##            sorted_keys = sorted(results[i].keys())
##            for j in sorted_keys:
##                out += "," + j
##        out += '\n'
##        stream.write(out)
##
##    def write_header_alternate(self, catagory_list, stream):
##        out = "fuelbed"
##        for i in catagory_list:
##            out += "," + i
##        out += '\n'
##        stream.write(out)
##
##    def check_emissions(self):
##        ''' stub '''
##        #emissions = consume.Emissions(self._consumer)
##        #emissions.report(csv="00emiss.csv")
##        #results = emissions.results()
##        #print(results)
##
##    def write_csv(self, results, fuelbed_list, stream, header, debug):
##    	### - top-level catagory list
##        catagory_list = ['summary', 'canopy', 'ground fuels', 'litter-lichen-moss',
##            'nonwoody', 'shrub', 'woody fuels']
##        if debug:
##            catagory_list.append('debug')
##
##        if header:
##            self.write_header(results, catagory_list, stream)
##        for fb_index in xrange(0, len(fuelbed_list)):
##            out = fuelbed_list[fb_index]
##            for cat in catagory_list:
##                ### - this needs to stay in sync with the way the header is printed
##                sorted_keys = sorted(results[cat].keys())
##                for key in sorted_keys:
##                    out += "," + str(results[cat][key]['total'][fb_index])
##            out += '\n'
##            stream.write(out)
##
##    def write_csv_alternate(self, results, fuelbed_list, stream, header):
##        if header:
##            columns = ['flaming', 'residual', 'smoldering', 'total']
##            self.write_header_alternate(results, columns, stream)
##        for fb_index in xrange(0, len(fuelbed_list)):
##            out = fuelbed_list[fb_index]
##            sorted_keys = sorted(results['summary']['total'].keys())
##            for key in sorted_keys:
##                out += "," + str(results['summary']['total'][key][fb_index])
##            out += '\n'
##            stream.write(out)
##
##    def write_csv_alt3(self, results, fuelbed_list, stream, header):
##        # use all the emission keys except 'stratum'
##        emissions_keys = sorted(results['emissions'].keys())
##        emissions_keys = [key for key in emissions_keys if key != 'stratum']
##        cons_keys = sorted(results['consumption']['summary']['total'].keys())
##
##        # build up the column headers
##        columns = []
##        for key in cons_keys:
##            columns.append("{}_{}".format("cons", key))
##        for i in emissions_keys:
##            for j in cons_keys:
##                columns.append("{}_{}".format(i, j))
##
##        if header:
##            self.write_header_alternate(columns, stream)
##        for fb_index in xrange(0, len(fuelbed_list)):
##            out = fuelbed_list[fb_index]
##
##            # print the consumption column values
##            for key in cons_keys:
##                out += "," + str(results['consumption']['summary']['total'][key][fb_index])
##
##            # print the emission column values
##            for i in emissions_keys:
##                for j in cons_keys:
##                    out += "," + str(results['emissions'][i][j][fb_index])
##            out += '\n'
##            stream.write(out)
##

##def SetDefaults(consumer):
##    consumer.burn_type = 'natural'
##    consumer.fuelbed_area_acres = 100
##    consumer.fuel_moisture_1000hr_pct = 20
##    consumer.fuel_moisture_duff_pct = 20
##    consumer.canopy_consumption_pct = 20
##    consumer.shrub_blackened_pct = 50
##    consumer.output_units = 'tons_ac'
##    # - activity specific
##    consumer.days_since_rain = 20
##    consumer.fuel_moisture_10hr_pct = 10
##    consumer.fm_type = 'MEAS-Th'
##    consumer.lengthOfIgnition = 30
##    consumer.slope = 5
##    consumer.windspeed = 5












