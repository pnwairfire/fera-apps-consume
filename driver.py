#-------------------------------------------------------------------------------
# Name:        driver.py
# Author:      kjells
# Created:     23/05/2011
# Copyright:   (c) kjells 2011
# Purpose:     Use to generate results for regression tests.
#-------------------------------------------------------------------------------
import consume
import sys

class Driver(object):
    """ Drive consume object for testing purposes
    """
    def __init__(self):
        self._consumer = consume.FuelConsumption(
            #fccs_file = "input_data/fccs_pyconsume_input.xml")
            fccs_file = "input_data/input_without_1000fb.xml")

    def _reset_consumer(self):
        self._consumer.burn_type = 'natural'
        self._consumer.fuelbed_area_acres = 100
        self._consumer.fuel_moisture_1000hr_pct = 20
        self._consumer.fuel_moisture_duff_pct = 20
        self._consumer.fuel_moisture_10hr_pct = 10
        self._consumer.canopy_consumption_pct = 20
        self._consumer.shrub_blackened_pct = 50
        self._consumer.output_units = 'tons_ac'
        self._consumer.slope = 5
        self._consumer.lengthOfIgnition = 30
        self._consumer.days_since_rain = 20
        self._consumer.windspeed = 5
        self._consumer.fm_type = 'MEAS-Th'

    def _reset_activity_scenario(self):
        self._consumer.fuel_moisture_10hr_pct = 15
        self._consumer.fuel_moisture_1000hr_pct = 39
        self._consumer.fuelbed_area_acres = 10
        self._consumer.lengthOfIgnition = 5

    def _reset_activity_scenario2(self):
        self._consumer.fuel_moisture_10hr_pct = 15
        self._consumer.fuel_moisture_1000hr_pct = 45
        self._consumer.fuelbed_area_acres = 25

    def _reset_activity_scenario3(self):
        self._consumer.fuel_moisture_10hr_pct = 17
        self._consumer.fuel_moisture_1000hr_pct = 50
        self._consumer.fuelbed_area_acres = 100

    def _reset_activity_scenario4(self):
        self._consumer.fuel_moisture_10hr_pct = 25
        self._consumer.fuel_moisture_1000hr_pct = 55
        self._consumer.fuelbed_area_acres = 100


    def write_header(self, results, catagory_list, stream):
        out = "fuelbed"
        for i in catagory_list:
            ### - this needs to stay in sync with the way the data is printed
            sorted_keys = sorted(results[i].keys())
            for j in sorted_keys:
                out += "," + j
        out += '\n'
        stream.write(out)

    def write_header_alternate(self, catagory_list, stream):
        out = "fuelbed"
        for i in catagory_list:
            out += "," + i
        out += '\n'
        stream.write(out)

    def check_emissions(self):
        ''' stub '''
        #emissions = consume.Emissions(self._consumer)
        #emissions.report(csv="00emiss.csv")
        #results = emissions.results()
        #print(results)

    def write_csv(self, results, fuelbed_list, stream, header, debug):
    	### - top-level catagory list
        catagory_list = ['summary', 'canopy', 'ground fuels', 'litter-lichen-moss',
            'nonwoody', 'shrub', 'woody fuels']
        if debug:
            catagory_list.append('debug')

        if header:
            self.write_header(results, catagory_list, stream)
        for fb_index in xrange(0, len(fuelbed_list)):
            out = fuelbed_list[fb_index]
            for cat in catagory_list:
                ### - this needs to stay in sync with the way the header is printed
                sorted_keys = sorted(results[cat].keys())
                for key in sorted_keys:
                    out += "," + str(results[cat][key]['total'][fb_index])
            out += '\n'
            stream.write(out)

    def write_csv_alternate(self, results, fuelbed_list, stream, header):
        if header:
            columns = ['flaming', 'residual', 'smoldering', 'total']
            self.write_header_alternate(results, columns, stream)
        for fb_index in xrange(0, len(fuelbed_list)):
            out = fuelbed_list[fb_index]
            sorted_keys = sorted(results['summary']['total'].keys())
            for key in sorted_keys:
                out += "," + str(results['summary']['total'][key][fb_index])
            out += '\n'
            stream.write(out)

    def write_csv_alt3(self, results, fuelbed_list, stream, header):
        # use all the emission keys except 'stratum'
        emissions_keys = sorted(results['emissions'].keys())
        emissions_keys = [key for key in emissions_keys if key != 'stratum']
        cons_keys = sorted(results['consumption']['summary']['total'].keys())

        # build up the column headers
        columns = []
        for key in cons_keys:
            columns.append("{}_{}".format("cons", key))
        for i in emissions_keys:
            for j in cons_keys:
                columns.append("{}_{}".format(i, j))

        if header:
            self.write_header_alternate(columns, stream)
        for fb_index in xrange(0, len(fuelbed_list)):
            out = fuelbed_list[fb_index]

            # print the consumption column values
            for key in cons_keys:
                out += "," + str(results['consumption']['summary']['total'][key][fb_index])

            # print the emission column values
            for i in emissions_keys:
                for j in cons_keys:
                    out += "," + str(results['emissions'][i][j][fb_index])
            out += '\n'
            stream.write(out)

    def run_tests(self, fuelbed_list=[], scenario_list=[], outfile=None, debug=False):
        self._reset_consumer()
        #outfilename = 'output_consume.csv'
        outfilename = 'output_consume_alternate.csv'

        #self._reset_activity_scenario()
        #self._reset_activity_scenario2()
        #outfilename = 'output_scenario2.csv'
        #self._reset_activity_scenario3()
        #outfilename = 'output_scenario3.csv'
        #self._reset_activity_scenario4()
        #outfilename = 'output_scenario4.csv'

        if not len(fuelbed_list):
            fuelbed_list = [str(i[0]) for i in self._consumer.FCCS.data]
        self._consumer.fuelbed_fccs_ids = fuelbed_list

        if not len(scenario_list):
            scenario_list = ['western', 'southern', 'boreal', 'activity']

        close_file = False
        if not outfile:
            outfile = open(outfilename, 'w')
            close_file = True

        write_header = True
        for scene in scenario_list:
            if 'activity' == scene:
                self._consumer.burn_type = scene
                self._consumer.fuelbed_ecoregion = 'western'
            else:
                print scene
                self._consumer.fuelbed_ecoregion = scene
            emissions = consume.Emissions(self._consumer)
            results = emissions.results()
            #self.write_csv(results['consumption'], fuelbed_list, outfile, write_header, debug)
            #self.write_csv_alternate(results['consumption'], fuelbed_list, outfile, write_header)
            self.write_csv_alt3(results, fuelbed_list, outfile, write_header)
            write_header = False

        if close_file:
            outfile.close()

#-------------------------------------------------------------------------------
# Start
#-------------------------------------------------------------------------------
driver = Driver()
if len(sys.argv) > 1:
    # - use the supplied scenario
    #driver.run_tests(fuelbed_list=['7'], scenario_list=['{}'.format(sys.argv[1])])
    driver.run_tests(scenario_list=['{}'.format(sys.argv[1])])
else:
    #driver.run_tests(scenario_list=['activity'])
    #driver.run_tests(fuelbed_list=['1'], scenario_list=['activity'])
    driver.run_tests(fuelbed_list=['5'], scenario_list=['activity'])
    #driver.run_tests(scenario_list=['western'])

"""
### - runs over all fuelbeds using 'western', 'southern', 'boreal', 'activity'
driver.run_tests()

### - run over the specfied fuelbeds, all scenarios
driver.run_tests(fuelbed_list=['1', '3', '1001'])

### - limit the scenarios
driver.run_tests(scenario_list=['western', 'southern', 'boreal'])
driver.run_tests(scenario_list=['western'])
driver.run_tests(scenario_list=['southern'])
driver.run_tests(scenario_list=['boreal'])

### - add the debug columns, far right of the output
driver.run_tests(debug=True)
"""
