"""
##### Working with the EMISSIONS Object #####

For emissions data, declare a Consume Emissions object by nesting in the
FuelConsumption object we were working on above as the only required argument.


>>> e_obj = consume.Emissions(fc_obj)


### SETTING INPUT PARAMETERS ###

Input parameters for emissions calculations are much easier to set than those
for FuelConsumption, as they are ALL ultimately automatically derived from the
parameters set within the nested FuelConsumption object.
The input parameters required for the emissions calculations are as follows:

     - FUEL CONSUMPTION (tons/ac) & the scenario of corresponding FCCS ID#s,
       AREAS, and ECOREGIONS, all of which is derived from the FuelConsumption
       object specified in the Emissions object declaration we just did

     - EMISSIONS FACTOR GROUP ('efg'), which specifies the appropriate set of
       emissions factors (lbs/tons consumed for each of 7 emissions species)
       to use for the scenario. This is automatically selected based on the
       FCCS fuelbeds in the consumption scenario, but the user can override
       the auto-select process if desired as described below.

To set alternate output units for the Emissions object, use the consume.list_valid_units() method
to view output unit options, and set using line below. 
Default output units for emissions are lbs/ac.

>>> e_obj.output_units = 'kg_ha'


### OUTPUTS ###

As with the FuelConsumption object, Emissions outputs can be accessed by
calling the .results() or .report() methods. Calling either methods will trigger
the calculation of emissions and output results in a variety of different
formats:

>>> e_obj.results()
                    ...generates a python DICTIONARY similar to the one created
                       by the FuelConsumption object, but with Emissions
                       results added (consumption data is also included).
                       See complete example below to see how specific
                       data categories can be accessed in this dictionary.

>>> e_obj.report()  ...prints a TABULAR REPORT of emissions results for all
                       pollutants and combustion stages (similar to the
                       "Emissions by Combustion Stage" report produced in
                       the official Consume 3.0 GUI program).  To export
                       a version of this report as a CSV FILE, use the
                       'csv' argument to specify a file name, e.g.:
                       >>> e_obj.report(csv = "emissions_report.csv")



### OTHER USEFUL METHODS ###

>>> e_obj.display_inputs()           ...displays a list of the input parameters.
                                        Useful for checking that scenario
                                        parameters were set correctly

>>> e_obj.efDB.browse()              ...displays a list of all emissions factor
                                        groups and their associated fuel types
                                        and references

>>> e_obj.efDB.info(#)               ...display detailed information about the
                                        specified emissions factor group ID#
                                        (use the .browse() method above to view
                                        ID#s). Includes the actual emissions
                                        factor values.

For further help on specific methods or properties,
type "help([CONSUME METHOD])" within a python shell, e.g.:

>>> help(fc_obj.FCCS.info)

"Out:

Help on method info in module consume_obj:

info(self, fccs_id, detail=False) method of consume_obj.FCCSDB instance
    Display an FCCS fuelbed description.

    Prints fuel loading information on the fuelbed with the specified
    FCCS ID. Requires one argument: an integer refering to a specific FCCS
    ID. For a list of valid FCCS IDs, use the .browse() method."

###################################################
           Complete Uninterrupted Example
###################################################

The following example sets up a 'natural' burn scenario in which 100 acres FCCS
fuelbed ID #1 ("Black cottonwood - Douglas fir - Quaking aspen riparian forest")
and 200 acres of FCCS fuelbed ID #47 ("Redwood - Tanoak forest") are consumed.
1000-hr and duff fuel moisture is set at 50% for fuelbed ID #1 and 40% for
fuelbed ID #47. Canopy consumption and shrub percent black is set at 25% for
both fuelbeds. See fuel_consumption.py for the consumption example.

>>> e_obj = consume.Emissions(fc_obj)
>>> e_obj.display_inputs()

Out:

CONSUMPTION

Current scenario parameters:

Parameter			        Value(s)
--------------------------------------------------------------
Burn type			        ['natural']
FCCS fuelbeds (ID#)		    [1, 47]
Fuelbed area (acres)		[ 100.  200.]
Fuelbed ecoregion		    ['western']
Fuel moisture (1000-hr, %)	[ 50.  40.]
Fuel moisture (duff, %)		[ 50.  40.]
Canopy consumption (%)		[ 25.]
Shrub blackened (%)		    [ 25.]
Output units			    ['kg_ha']

EMISSIONS

Current scenario parameters:

Parameter			Value(s)
--------------------------------------------------------------



>>> e_obj.report()

Out:

EMISSIONS
Units: lbs_ac

FCCS ID: 1
Area:	100 ac. (40.5 ha)
Emissions factor group: 2
SPECIES	Flaming		Smoldering	Residual	TOTAL
pm	    2.77e+02	3.73e+02	7.82e+02	1.43e+03
pm10	1.69e+02	2.54e+02	5.33e+02	9.56e+02
pm2.5	1.47e+02	2.30e+02	4.82e+02	8.58e+02
co	    1.11e+03	3.59e+03	7.53e+03	1.22e+04
co2	    4.09e+04	2.80e+04	5.87e+04	1.28e+05
ch4	    5.31e+01	1.92e+02	4.03e+02	6.49e+02
nmhc	6.27e+01	1.37e+02	2.88e+02	4.88e+02

FCCS ID: 47
Area:	200 ac. (80.9 ha)
Emissions factor group: 4
SPECIES	Flaming		Smoldering	Residual	TOTAL
pm	    4.60e+02	9.69e+02	1.45e+03	2.88e+03
pm10	2.45e+02	7.30e+02	1.09e+03	2.07e+03
pm2.5	2.01e+02	6.81e+02	1.02e+03	1.90e+03
co	    1.11e+03	7.87e+03	1.18e+04	2.08e+04
co2	    7.24e+04	8.72e+04	1.30e+05	2.90e+05
ch4	    6.28e+01	5.08e+02	7.60e+02	1.33e+03
nmhc	6.70e+01	3.81e+02	5.70e+02	1.02e+03

ALL FUELBEDS:
Units: lbs_ac
Total area: 300 ac. (121.4 ha)
pm	    3.99e+02	7.70e+02	1.23e+03	2.40e+03
pm10	9.45e+01	3.02e+01	2.14e+01	1.46e+02
pm2.5	2.96e+01	3.08e+00	0.00e+00	3.27e+01
co	    7.81e+00	6.37e-01	0.00e+00	8.45e+00
co2	    4.02e+01	6.65e+00	0.00e+00	4.68e+01
ch4	    2.65e+01	4.93e+02	9.07e+02	1.43e+03
nmhc	2.01e+02	2.37e+02	2.99e+02	7.36e+02



>>> e_obj.results()['emissions']['co2']

Out:
{'flaming': array([ 40877.14600611,  72354.16061005]),
 'residual': array([  58664.90328723,  130457.66209735]),
 'smoldering': array([ 27980.07467362,  87193.41115534]),
 'total': array([ 127522.12396695,  290005.23386274])}


#####################################################
        Navigating the .results() dictionaries
#####################################################

The table below depicts all categories included in the .results() dictionaries
that are produced from the FuelConsumption and Emissions objects. Note that the
FuelConsumption .results() dictionary does NOT include emissions data while the
Emissions .results() dictionary includes BOTH consumption and emissions data.

The FINAL index in the dictionary will be always be an integer that indicates
the fuelbed unit in the scenario. In the example above, a [0] would access
data for the first fuelbed (FCCS ID #1) and a [1] would access data for the
second fuelbed (FCCS ID #47). Use Python's built-in 'sum()' function to
calculate total consumption/emissions across ALL fuelbeds.


~~~Examples~~~
To access 'co2' emissions from all combustion stages:
e_obj.results()['emissions']['co2']

To access total 'co2' emissions for the given scenario across ALL fuelbeds*:
sum(e_obj.results()['emissions']['co2']['total'])

To view units that the emissions data are in:
e_obj.results()['parameters']['units_emissions']

*Note: if outputs units are per-area units (i.e. tons/acre or kg/ha), these
 sum' functions will not provide an accurate representation of the overall
 consumption rate for the scenario.


Index 1           Index 2              Index 3                     Index 4       Index 5
-----------------------------------------------------------------------------------------------------------------------------

'parameters'   'fuel moisture: 1000hr'
               'fuel moisture duff'
               'fuel moisture pct canopy consumed'
               'fuel moisture pct shrub blackened'
               'fuelbed area'
               'fuelbed ecoregion'
               'fuelbed fccs id'
               'units consumption'
               'units emissions'
-----------------------------------------------------------------------------------------------------------------------------

'emissions'    'ch4'                'flaming','smoldering','residual', or 'total'
               'co'                 'flaming','smoldering','residual', or 'total'
               'co2'                'flaming','smoldering','residual', or 'total'
               'nmhc'               'flaming','smoldering','residual', or 'total'
               'pm'                 'flaming','smoldering','residual', or 'total'
               'pm10'               'flaming','smoldering','residual', or 'total'
               'pm25'               'flaming','smoldering','residual', or 'total'

               'stratum'            'ch4'                       'canopy'             'flaming','smoldering','residual', or 'total
                                                                'ground fuels'       ''
                                                                'litter-lichen-moss' ''
                                                                'nonwoody'           ''
                                                                'shrub'              ''
                                                                'woody fuels'        ''
                                    'co'                        'canopy'             ''
                                                                'ground fuels'       ''
                                                                'litter-lichen-moss' ''
                                                                'nonwoody'           ''
                                                                'shrub'              ''
                                                                'woody fuels'        ''
                                    'co2'   .....etc.....


-----------------------------------------------------------------------------------------------------------------------------

'heat release' 'flaming'
               'smoldering'
               'residual'
               'total'

-----------------------------------------------------------------------------------------------------------------------------

'consumption'  'summary'            'total'                     'flaming','smoldering','residual', or 'total'
                                    'canopy'                    'flaming','smoldering','residual', or 'total'
                                    'ground fuels'              'flaming','smoldering','residual', or 'total'
                                    'litter-lichen-moss'        'flaming','smoldering','residual', or 'total'
                                    'nonwoody'                  'flaming','smoldering','residual', or 'total'
                                    'shrub'                     'flaming','smoldering','residual', or 'total'
                                    'woody fuels'               'flaming','smoldering','residual', or 'total

               'canopy'             'overstory'                 'flaming','smoldering','residual', or 'total'
                                    'midstory'                  'flaming','smoldering','residual', or 'total'
                                    'understory'                'flaming','smoldering','residual', or 'total'
                                    'ladder fuels'              'flaming','smoldering','residual', or 'total'
                                    'snags class 1 foliage'     'flaming','smoldering','residual', or 'total'
                                    'snags class 1 non foliage' 'flaming','smoldering','residual', or 'total'
                                    'snags class 1 wood'        'flaming','smoldering','residual', or 'total'
                                    'snags class 2'             'flaming','smoldering','residual', or 'total'
                                    'snags class 3'             'flaming','smoldering','residual', or 'total'

               'ground fuels'       'duff upper'                'flaming','smoldering','residual', or 'total'
                                    'duff lower'                'flaming','smoldering','residual', or 'total'
                                    'basal accumulations'       'flaming','smoldering','residual', or 'total'
                                    'squirrel middens'          'flaming','smoldering','residual', or 'total'

               'litter-lichen-moss' 'litter'                    'flaming','smoldering','residual', or 'total'
                                    'lichen'                    'flaming','smoldering','residual', or 'total'
                                    'moss'                      'flaming','smoldering','residual', or 'total'
               'nonwoody'           'primary dead'              'flaming','smoldering','residual', or 'total'
                                    'primary live'              'flaming','smoldering','residual', or 'total'
                                    'secondary dead'            'flaming','smoldering','residual', or 'total'
                                    'secondary live'            'flaming','smoldering','residual', or 'total'

               'shrub'              'primary dead'              'flaming','smoldering','residual', or 'total'
                                    'primary live'              'flaming','smoldering','residual', or 'total'
                                    'secondary dead'            'flaming','smoldering','residual', or 'total'
                                    'secondary live'            'flaming','smoldering','residual', or 'total'
               'woody fuels'        '1-hr fuels'                'flaming','smoldering','residual', or 'total'
                                    '10-hr fuels'               'flaming','smoldering','residual', or 'total'
                                    '100-hr fuels'              'flaming','smoldering','residual', or 'total'
                                    '1000-hr fuels sound'       'flaming','smoldering','residual', or 'total'
                                    '1000-hr fuels rotten'      'flaming','smoldering','residual', or 'total'
                                    '10000-hr fuels sound'      'flaming','smoldering','residual', or 'total'
                                    '10000-hr fuels rotten'     'flaming','smoldering','residual', or 'total'
                                    '10k+-hr fuels sound'       'flaming','smoldering','residual', or 'total'
                                    '10k+-hr fuels rotten'      'flaming','smoldering','residual', or 'total'
                                    'stumps sound'              'flaming','smoldering','residual', or 'total'
                                    'stumps rotten'             'flaming','smoldering','residual', or 'total'
                                    'stumps lightered'          'flaming','smoldering','residual', or 'total'
-----------------------------------------------------------------------------------------------------------------------------

"""
import numpy as np
from eflookup.fccs2ef import Fccs2SeraEf
from eflookup.fccs2ef import CoverType2SeraEf

from . emissions_db import EmissionsFactorDB as edb
from . import data_desc as dd
from . import util_consume as util


#class Emissions(object):
class Emissions(util.FrozenClass):
    """A class that estimates emissions from fire.

    This class implements the CONSUME model equations for estimating emissions
    due to fire based on fuel consumption data.

    """
    @property
    def no_sera(self): return self._no_sera
    @no_sera.setter
    def no_sera(self, value):
        self._no_sera = value

    @property
    def output_units(self): return self._output_units
    @output_units.setter
    def output_units(self, value):
        tmp = value.lower()
        if tmp in dd.list_valid_units():
            self._output_units = tmp
        else:
            print("Error: the only permitted values for units are:")
            for i in dd.list_valid_units():
                print("\t{}".format(i))

    def __init__(self, fuel_consumption_object = None, emissions_xml = ""):
        """Emissions class constuctor.

        Upon initialization of the Emissions object, all input
        variables are declared.

        Optional arguments:

        _cons_object           : a FuelConsumption object. Emissions objects have a
                          FuelConsumption object nested within them from which
                          fuel consumption outputs are used to derive emissions
                          data. If a specific FuelConsumption object is not
                          specified, an empty one will be created.

        emissions_xml   : directory location of the emissions factor database
                          XML. Leave blank to load the default database.

        """
        if fuel_consumption_object is not None:
            self._cons_object = fuel_consumption_object
            self._emission_factor_db = edb(emissions_xml, fuel_consumption_object)
            self._have_cons_data = 0
            self._internal_units = "lbs_ac"
            self._output_units = "lbs_ac"
            self._emissions_factor_groups = None

            ### - output variables
            self._emis_data = None
            self._emis_summ = None
            self._no_sera = False
            self._freeze()

    def results(self):
        """Returns a python DICTIONARY of emissions estimates.

        Returns a python dictionary variable comprised of input and output data.

        See "Navigating the .results()" dictionaries in the README at the
        top of this file for detailed information on the structure of
        the dictionary and examples on how to extract information from the
        dictionary.
        """
                
        self._calculate()
        self._convert_units()

        ins = self._cons_object._settings.package(self._cons_object.FCCS.loadings_data_)
        ins['emissions_fac_group'] = self._emissions_factor_groups
        # - single-value settings must be converted to a list so that results can be treated the same way
        ins['units_emissions'] = list([self._output_units] * len(self._cons_object._settings.get('fuelbeds')))
        return util.make_dictionary_of_lists(cons_data = self._cons_object._cons_data,
                                        heat_data = self._cons_object._heat_data,
                                        emis_data = self._emis_data, inputs = ins)

    def report(self, csv = ""):
        """Displays a report of emissions estimates.

        Displays (in shell) emissions data in tabular format, similar to
        how the official GUI CONSUME reports emissions by combustion stage.

        -Optional arguments-

            csv :   Valid values: any valid file location
                    Default value: ""
                    Value functionality:
                        will export a comma-separated-file of the report to the
                        specified location

        """

        if self._calculate():
            self._convert_units()
            categories = ["pm", "pm10", "pm2.5", "co", "co2", "ch4", "nmhc"]
            area = self._cons_object._settings.get('area')
            units = self._cons_object._settings.units
            ecoregion =  self._cons_object._settings.get('ecoregion')
            fccs_ids = self._cons_object._settings.get('fuelbeds')
            efgs = self._emissions_factor_groups
            str_au = units

            if units in dd.perarea() and sum(area) > 0:
                str_au = "/".join(units.split("_"))

            if len(area) == 1:
                area = np.array([1] * len(fccs_ids), dtype=float) * area

            if len(ecoregion) == 1:
                ecoregion = ecoregion * len(fccs_ids)

            csv_lines = ('fuelbeds,ecoregion,area,efg,units'
                         + ",species,flaming,smoldering,residual,total\n")


            print("\n\nEMISSIONS\nUnits: {}".format(self._output_units))
            for i in range(0, len(fccs_ids)):
                ha = area[i] * 0.404685642
                print ("\nFCCS ID: " + str(fccs_ids[i])
                        + "\nArea:\t%.0f" % area[i] + " ac. (%.1f" % ha
                        + " ha)\nEmissions factor group: "
                        + str(self._emissions_factor_groups[i])
                        + "\nSPECIES\tFlaming\t\tSmoldering\tResidual\tTOTAL")


                csv_header = (str(fccs_ids[i]) + ',' + ecoregion[i] + ',' +
                              str(area[i]) + ',' + str(efgs[i]) + ',' + str_au +
                              ',')

                for j in range(0, 7):
                    dat = self._emis_data[j][0]  # <<<
                    print (categories[j] + "\t%.2e" % dat[0][i]
                            + "\t%.2e" % dat[1][i]
                            + "\t%.2e" % dat[2][i] + "\t%.2e"
                            % dat[3][i])

                    csv_lines += (csv_header + categories[j] + ',' +
                            str(dat[0][i]) + ',' + str(dat[1][i]) + ',' +
                            str(dat[2][i]) + ',' + str(dat[3][i]) + '\n')

            print ("\nALL FUELBEDS:\nUnits: " + self._output_units
                   + "\nTotal area: %.0f" % sum(area)
                   + " ac. (%.1f" % (sum(area) * 0.404685642) + " ha)")

            all_hed =  'ALL,ALL,' + str(sum(area)) + ',ALL,' + str_au + ','


            if self._internal_units in dd.perarea() and sum(area) > 0:
                em_sum = self._emis_summ[0]
                for j in range(0, 7):
                    print (categories[j] + "\t%.2e" % em_sum[j][0]
                            + "\t%.2e" % em_sum[j][1]
                            + "\t%.2e" % em_sum[j][2] + "\t%.2e"
                            % em_sum[j][3])

                    csv_lines += (all_hed + categories[j] + ',' +
                                  str(em_sum[j][0]) + ',' + str(em_sum[j][1]) +
                                  ',' + str(em_sum[j][2]) + ',' +
                                  str(em_sum[j][3]) + '\n')

            else:
                for j in range(0, 7):
                    dat = self._emis_data[j][0]
                    print (categories[j] + "\t%.2e" % sum(dat[0])
                            + "\t%.2e" % sum(dat[1]) + "\t%.2e" % sum(dat[2])
                            + "\t%.2e" % sum(dat[3]))

                    csv_lines += (all_hed + categories[j] + ',' +
                                  str(sum(dat[0])) + ',' + str(sum(dat[1])) +
                                  ',' + str(sum(dat[2])) + ',' +
                                  str(sum(dat[3])) + '\n')

            if csv != "":
                text = open(csv, 'w')
                text.write(csv_lines)
                text.close()


    def display_inputs(self):
        """Lists the input parameters for the emissions scenario.

        Displays the input parameters for the consumption and emissions
        scenario in the shell. Useful as a quick way to check that the
        scenario parameters have been correctly set.

        """
        out_consumption = self._cons_object._settings.display_settings()
        return out_consumption

    def _calculate(self):
        """Calculates emissions estimates.

        Runs all the functions necessary to derive emissions from the
        consumption data, which is set upon object initialization.

        """
        if self._have_cons_data == 0:
            self._cons_object._calculate() # to generate consumption values
            if not None is self._cons_object._cons_data:
                self._have_cons_data = len(self._cons_object._cons_data[0][0])

        if self._have_cons_data:
            self._emissions_factor_groups = self._emission_factor_db.get_efgs(self._cons_object._settings.get('fuelbeds'))
            self._emissions_calc(efg = self._emissions_factor_groups)
            return (not None is self._emis_data) and (not None is self._emis_summ)
        else:
            return False

    def _convert_units(self):
        """Converts units of consumption and emissions data"""
        area = self._cons_object._settings.get('area')
        # if Emissions internal/output units differ, update emissions data
        if self._internal_units != self._output_units:
            orig_units = self._internal_units

            [self._internal_units, self._emis_data] = util.unit_conversion(self._emis_data,
                                                   area,
                                                   self._internal_units,
                                                   self._output_units)

            [self._internal_units, self._emis_summ] = util.unit_conversion(self._emis_summ,
                                                   sum(area),
                                                   orig_units,
                                                   self._output_units)
            ### - pass on to fuel consumption object
            self._cons_object._convert_units(explicit_units=self._output_units)

    def _emissions_calc_pm_piles(self, all_loadings, pile_loadings, pile_black_pct):
        # helper functions
        def get_clean_dirty_vdirty_ratio(loadings, pile_loading_total):
            # - ensure float for divisior
            plt_as_float = pile_loading_total.copy(float)
            plt_as_float[:] = pile_loading_total
            clean_ratio =  np.where(pile_loading_total, loadings['pile_clean_loading']  / plt_as_float, 0.0)
            dirty_ratio =  np.where(pile_loading_total, loadings['pile_dirty_loading']  / plt_as_float, 0.0)
            vdirty_ratio = np.where(pile_loading_total, loadings['pile_vdirty_loading'] / plt_as_float, 0.0)
            pile_loading_ratios = np.array([clean_ratio] + [dirty_ratio] + [vdirty_ratio])
            return pile_loading_ratios.transpose()

        def calc_pm(pile_loadings, cdv_ratios, pm_type, pile_black_pct):
            # - emission factor * clean/dirty/vdirty ratio
            adjusted_pm_value = pm_type * cdv_ratios

            # get consumed mass
            total_consumed = (pile_loadings * pile_black_pct).values

            cdv_results = np.zeros(len(total_consumed))
            for i in range(0, len(total_consumed)):
                summ = 0.0
                for adj_value in adjusted_pm_value[i]:
                    summ += total_consumed[i] * adj_value
                cdv_results[i] = summ

            return util.csdist(cdv_results, [0.70, 0.15, 0.15])

        # Start -----------
        pile_ratios = get_clean_dirty_vdirty_ratio(all_loadings, pile_loadings)
        pm_piles = calc_pm(pile_loadings, pile_ratios, util.pile_particulatematter_emission_factors['PM'], pile_black_pct)
        pm10_piles = calc_pm(pile_loadings, pile_ratios, util.pile_particulatematter_emission_factors['PM10'], pile_black_pct)
        pm25_piles = calc_pm(pile_loadings, pile_ratios, util.pile_particulatematter_emission_factors['PM25'], pile_black_pct)
        return (pm_piles, pm10_piles, pm25_piles)

    def _emissions_calc_pollutants_piles(self, pile_loadings, pile_black_pct):
        # helper function
        def calc_pollutant(pile_loadings, pollutant_type, pile_black_pct):
            # get consumed mass
            total_consumed = pile_loadings * pile_black_pct
            phase_consumed = util.csdist(total_consumed.values, [0.70, 0.15, 0.15])

            results = np.zeros_like(phase_consumed)
            for i in range(0, len(pile_loadings)):
                tmp = phase_consumed[:,i] * pollutant_type
                results[:,i] = np.array([tmp[0]] + [tmp[1]] + [tmp[2]] + [sum(tmp)])
            return results

        # Start -----------
        pile_co = calc_pollutant(pile_loadings, util.pile_pollutant_emission_factors['CO'], pile_black_pct)
        pile_co2 = calc_pollutant(pile_loadings, util.pile_pollutant_emission_factors['CO2'], pile_black_pct)
        pile_ch4= calc_pollutant(pile_loadings, util.pile_pollutant_emission_factors['CH4'], pile_black_pct)
        pile_nmhc = calc_pollutant(pile_loadings, util.pile_pollutant_emission_factors['NMHC'], pile_black_pct)
        pile_nmoc = calc_pollutant(pile_loadings, util.pile_pollutant_emission_factors['NMOC'], pile_black_pct)
        pile_nh3 = calc_pollutant(pile_loadings, util.pile_pollutant_emission_factors['NH3'], pile_black_pct)
        pile_no = calc_pollutant(pile_loadings, util.pile_pollutant_emission_factors['NO'], pile_black_pct)
        pile_no2 = calc_pollutant(pile_loadings, util.pile_pollutant_emission_factors['NO2'], pile_black_pct)
        pile_nox = calc_pollutant(pile_loadings, util.pile_pollutant_emission_factors['NOx'], pile_black_pct)
        pile_so2 = calc_pollutant(pile_loadings, util.pile_pollutant_emission_factors['SO2'], pile_black_pct)

        return (pile_co, pile_co2, pile_ch4, pile_nmhc, pile_nmoc, pile_nh3, pile_no, pile_no2, pile_nox, pile_so2)

    def _emissions_calc(self, efg):
        """Calculates emissions estimates.

        Calculates emissions of pm, pm10, pm25, co, co2, ch4, and nmhc as
        lbs/ton consumed based on consumption data and emissions factors for
        each emissions species.

        """
        def calc_species(cons_data, ef):
            """ Gets summed data """
            temp = cons_data * ef
            for i in range(0, len(temp)):
                summ = sum(temp[i])
                temp[i][3] = summ
            return temp

        def get_emis_summ(p):
            """ Sums emissions data by area for each species/fccs id """
            alls = []
            base = self._emis_data[p]
            for i in range(0, len(self._cons_object._cons_data)):
                base2 = area * np.array(base[i])
                alls.append(np.sum(base2, axis=1))
            return alls / tot_area

        def arrayize(d):
            """ Converts list to numpy array """
            return np.array(d)

        def pile_info(cons_obj):
            """ Get commonly used pile information """
            loadings = \
                cons_obj._get_loadings_for_specified_files(cons_obj._settings.get('fuelbeds'))
            pile_black_pct = (cons_obj._settings.get('pile_black_pct') * 0.01)
            pile_loading_total = loadings['pile_clean_loading'] \
                                + loadings['pile_dirty_loading'] \
                                + loadings['pile_vdirty_loading']
            return (loadings, pile_loading_total, pile_black_pct)

        self._emis_data = None
        self._emis_summ = None

        # - subtract out pile loading -- restore it at the end of routine
        all_fsrt = self._cons_object._cons_data
        all_fsrt[0] = all_fsrt[0] - self._cons_object._cons_data_piles
        all_fsrt[6] = all_fsrt[6] - self._cons_object._cons_data_piles

        # Load default emissions factors (average of all factors...)
        t = self._emission_factor_db.data[0]
        num_fuelbeds = int(self._have_cons_data)# <<< ucons
        
        if self._no_sera:
            ef_flamg_pm = np.array([t['PM_flaming']] * num_fuelbeds, dtype = float)
            ef_flamg_pm10 = np.array([t['PM10b_flaming']] * num_fuelbeds, dtype = float)
            ef_flamg_pm25 = np.array([t['PM25_flaming']] * num_fuelbeds, dtype = float)
            ef_flamg_co = np.array([t['CO_flaming']] * num_fuelbeds, dtype = float)
            ef_flamg_co2 = np.array([t['CO2_flaming']] * num_fuelbeds, dtype = float)
            ef_flamg_ch4 = np.array([t['CH4_flaming']] * num_fuelbeds, dtype = float)
            ef_flamg_nmhc = np.array([t['NMHC_flaming']] * num_fuelbeds, dtype = float)
            # these are in SERA lookup, but not Consume
            ef_flamg_nmoc = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_nh3 = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_no = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_no2 = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_nox = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_so2 = np.array([0] * num_fuelbeds, dtype = float)

            ef_smres_pm = np.array([t['PM_smold_resid']] * num_fuelbeds, dtype = float)
            ef_smres_pm10 = np.array([t['PM10b_smold_resid']] * num_fuelbeds, dtype = float)
            ef_smres_pm25 = np.array([t['PM25_smold_resid']] * num_fuelbeds, dtype = float)
            ef_smres_co = np.array([t['CO_smold_resid']] * num_fuelbeds, dtype = float)
            ef_smres_co2 = np.array([t['CO2_smold_resid']] * num_fuelbeds, dtype = float)
            ef_smres_ch4 = np.array([t['CH4_smold_resid']] * num_fuelbeds, dtype = float)
            ef_smres_nmhc = np.array([t['NMHC_smold_resid']] * num_fuelbeds, dtype = float)
            # these are in SERA lookup, but not Consume
            ef_smres_nmoc = np.array([0] * num_fuelbeds, dtype = float)
            ef_smres_nh3 = np.array([0] * num_fuelbeds, dtype = float)
            ef_smres_no = np.array([0] * num_fuelbeds, dtype = float)
            ef_smres_no2 = np.array([0] * num_fuelbeds, dtype = float)
            ef_smres_nox = np.array([0] * num_fuelbeds, dtype = float)
            ef_smres_so2 = np.array([0] * num_fuelbeds, dtype = float)

            # And go fetch factors from the chosen emissions factor groups
            for i in range(0, num_fuelbeds):
                data = self._emission_factor_db.data[int(efg[i])]
                ef_flamg_pm25[i] = data['PM25_flaming']; ef_smres_pm25[i] = data['PM25_smold_resid']
                ef_flamg_co[i] = data['CO_flaming']; ef_smres_co[i] = data['CO_smold_resid']
                ef_flamg_co2[i] = data['CO2_flaming']; ef_smres_co2[i] = data['CO2_smold_resid']
                ef_flamg_ch4[i] = data['CH4_flaming']; ef_smres_ch4[i] = data['CH4_smold_resid']
                ef_flamg_nmhc[i] = data['NMHC_flaming']; ef_smres_nmhc[i] = data['NMHC_smold_resid']
                ef_flamg_pm[i] = data['PM_flaming']; ef_smres_pm[i] = data['PM_smold_resid']
                ef_flamg_pm10[i] = data['PM10b_flaming']; ef_smres_pm10[i] = data['PM10b_smold_resid']

            fill = [np.array([0] * num_fuelbeds, dtype=float)]
            
            ef_pm = np.array([ef_flamg_pm] + [ef_smres_pm] + [ef_smres_pm] + fill)
            ef_pm10 = np.array([ef_flamg_pm10] + [ef_smres_pm10] + [ef_smres_pm10] + fill)
            ef_pm25 = np.array([ef_flamg_pm25] + [ef_smres_pm25] + [ef_smres_pm25] + fill)
            ef_co = np.array([ef_flamg_co] + [ef_smres_co] + [ef_smres_co] + fill)
            ef_co2 = np.array([ef_flamg_co2] + [ef_smres_co2] + [ef_smres_co2] + fill)
            ef_ch4 = np.array([ef_flamg_ch4] + [ef_smres_ch4] + [ef_smres_ch4] + fill)
            ef_nmhc = np.array([ef_flamg_nmhc] + [ef_smres_nmhc] + [ef_smres_nmhc] + fill)
            # these will all be zeros
            ef_nmoc = np.array([ef_flamg_nmoc] + [ef_smres_nmoc] + [ef_smres_nmoc] + fill)
            ef_nh3 = np.array([ef_flamg_nh3] + [ef_smres_nh3] + [ef_smres_nh3] + fill)
            ef_no = np.array([ef_flamg_no] + [ef_smres_no] + [ef_smres_no] + fill)
            ef_no2 = np.array([ef_flamg_no2] + [ef_smres_no2] + [ef_smres_no2] + fill)
            ef_nox = np.array([ef_flamg_nox] + [ef_smres_nox] + [ef_smres_nox] + fill)
            ef_so2 = np.array([ef_flamg_so2] + [ef_smres_so2] + [ef_smres_so2] + fill)

        else:
            # using SERA numbers
            # set up some arrays
            ef_flamg_pm = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_pm10 = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_pm25 = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_co = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_co2 = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_ch4 = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_nh3 = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_nmhc = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_nmoc = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_no = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_no2 = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_nox = np.array([0] * num_fuelbeds, dtype = float)
            ef_flamg_so2 = np.array([0] * num_fuelbeds, dtype = float)

            ef_smold_pm = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_pm10 = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_pm25 = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_co = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_co2 = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_ch4 = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_nh3 = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_nmhc = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_nmoc = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_no = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_no2 = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_nox = np.array([0] * num_fuelbeds, dtype = float)
            ef_smold_so2 = np.array([0] * num_fuelbeds, dtype = float)

            ef_resid_pm = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_pm10 = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_pm25 = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_co = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_co2 = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_ch4 = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_nh3 = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_nmhc = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_nmoc = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_no = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_no2 = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_nox = np.array([0] * num_fuelbeds, dtype = float)
            ef_resid_so2 = np.array([0] * num_fuelbeds, dtype = float)

            fuelbeds = self._cons_object._settings.get('fuelbeds')

            for i in range(0, num_fuelbeds):
                fuelbedNum = fuelbeds[i]

                ## get the cover_type, then use it to do lu = CoverType2SeraEf(cover_type)

                indexForFCCSObject = self._cons_object.FCCS.loadings_data_.fccs_id==fuelbedNum
                cover_type = self._cons_object.FCCS.loadings_data_[indexForFCCSObject].cover_type.values[0]

                lu = CoverType2SeraEf(cover_type)
                
                ef_flamg_pm25[i] = 2 * lu.get(phase="flaming",fuel_category="canopy",fuel_sub_category="overstory",species="PM2.5")
                ef_smold_pm25[i] = 2 * lu.get(phase="smoldering",fuel_category="canopy",fuel_sub_category="overstory",species="PM2.5")
                ef_resid_pm25[i] = ef_smold_pm25[i]
                
                ef_flamg_pm10[i] = ef_flamg_pm25[i] * 1.111
                ef_smold_pm10[i] = ef_smold_pm25[i] * 1.111
                ef_resid_pm10[i] = ef_smold_pm10[i]

                ef_flamg_co[i] = 2 * lu.get(phase="flaming",fuel_category="canopy",fuel_sub_category="overstory",species="CO")
                ef_smold_co[i] = 2 * lu.get(phase="smoldering",fuel_category="canopy",fuel_sub_category="overstory",species="CO")
                ef_resid_co[i] = ef_smold_co[i]

                ef_flamg_co2[i] = 2 * lu.get(phase="flaming",fuel_category="canopy",fuel_sub_category="overstory",species="CO2")
                ef_smold_co2[i] = 2 * lu.get(phase="smoldering",fuel_category="canopy",fuel_sub_category="overstory",species="CO2")
                ef_resid_co2[i] = ef_smold_co2[i]

                ef_flamg_ch4[i] = 2 * lu.get(phase="flaming",fuel_category="canopy",fuel_sub_category="overstory",species="CH4")
                ef_smold_ch4[i] = 2 * lu.get(phase="smoldering",fuel_category="canopy",fuel_sub_category="overstory",species="CH4")
                ef_resid_ch4[i] = ef_smold_ch4[i]

                # NMHC ? PM ? instead of showing old values, leave these set to zero. 
                # In other words, NHMC and PM are unsupported. Instead of NMHC, we return NMOC 
                
                ef_flamg_nmoc[i] = 2 * lu.get(phase="flaming",fuel_category="canopy",fuel_sub_category="overstory",species="NMOC")
                ef_smold_nmoc[i] = 2 * lu.get(phase="smoldering",fuel_category="canopy",fuel_sub_category="overstory",species="NMOC")
                ef_resid_nmoc[i] = ef_smold_nmoc[i]

                # new pollutants follow: NH3, NO, NO2, NOx, SO2
                ef_flamg_nh3[i] = 2 * lu.get(phase="flaming",fuel_category="canopy",fuel_sub_category="overstory",species="NH3")
                ef_smold_nh3[i] = 2 * lu.get(phase="smoldering",fuel_category="canopy",fuel_sub_category="overstory",species="NH3")
                ef_resid_nh3[i] = ef_smold_nh3[i]

                ef_flamg_no[i] = 2 * lu.get(phase="flaming",fuel_category="canopy",fuel_sub_category="overstory",species="NO")
                ef_smold_no[i] = 2 * lu.get(phase="smoldering",fuel_category="canopy",fuel_sub_category="overstory",species="NO")
                ef_resid_no[i] = ef_smold_no[i]

                ef_flamg_no2[i] = 2 * lu.get(phase="flaming",fuel_category="canopy",fuel_sub_category="overstory",species="NO2")
                ef_smold_no2[i] = 2 * lu.get(phase="smoldering",fuel_category="canopy",fuel_sub_category="overstory",species="NO2")
                ef_resid_no2[i] = ef_smold_no2[i]

                ef_flamg_nox[i] = 2 * lu.get(phase="flaming",fuel_category="canopy",fuel_sub_category="overstory",species="NOx")
                ef_smold_nox[i] = 2 * lu.get(phase="smoldering",fuel_category="canopy",fuel_sub_category="overstory",species="NOx")
                ef_resid_nox[i] = ef_smold_nox[i]

                ef_flamg_so2[i] = 2 * lu.get(phase="flaming",fuel_category="canopy",fuel_sub_category="overstory",species="SO2")
                ef_smold_so2[i] = 2 * lu.get(phase="smoldering",fuel_category="canopy",fuel_sub_category="overstory",species="SO2")
                ef_resid_so2[i] = ef_smold_so2[i]
         
            fill = [np.array([0] * num_fuelbeds, dtype=float)]
            ef_pm = np.array([ef_flamg_pm] + [ef_smold_pm] + [ef_resid_pm] + fill)
            ef_pm10 = np.array([ef_flamg_pm10] + [ef_smold_pm10] + [ef_resid_pm10] + fill)
            ef_pm25 = np.array([ef_flamg_pm25] + [ef_smold_pm25] + [ef_resid_pm25] + fill)
            ef_co = np.array([ef_flamg_co] + [ef_smold_co] + [ef_resid_co] + fill)
            ef_co2 = np.array([ef_flamg_co2] + [ef_smold_co2] + [ef_resid_co2] + fill)
            ef_ch4 = np.array([ef_flamg_ch4] + [ef_smold_ch4] + [ef_resid_ch4] + fill)
            ef_nmhc = np.array([ef_flamg_nmhc] + [ef_smold_nmhc] + [ef_resid_nmhc] + fill)
            ef_nmoc = np.array([ef_flamg_nmoc] + [ef_smold_nmoc] + [ef_resid_nmoc] + fill)
            ef_nh3 = np.array([ef_flamg_nh3] + [ef_smold_nh3] + [ef_resid_nh3] + fill)
            ef_no = np.array([ef_flamg_no] + [ef_smold_no] + [ef_resid_no] + fill)
            ef_no2 = np.array([ef_flamg_no2] + [ef_smold_no2] + [ef_resid_no2] + fill)
            ef_nox = np.array([ef_flamg_nox] + [ef_smold_nox] + [ef_resid_nox] + fill)
            ef_so2 = np.array([ef_flamg_so2] + [ef_smold_so2] + [ef_resid_so2] + fill)
            


###---------------------------------------------------

       
        # Emissions calculations:
       # consumption (tons/acre) * emissions factor (lb/ton) = lbs/ac emissions
       # Emissions for all fuels combined
        emis_pm_fsrt = calc_species(all_fsrt, ef_pm)
        emis_pm10_fsrt = calc_species(all_fsrt, ef_pm10)
        emis_pm25_fsrt = calc_species(all_fsrt, ef_pm25)
        emis_co_fsrt = calc_species(all_fsrt, ef_co)
        emis_co2_fsrt = calc_species(all_fsrt, ef_co2)
        emis_ch4_fsrt = calc_species(all_fsrt, ef_ch4)
        emis_nmhc_fsrt = calc_species(all_fsrt, ef_nmhc)
        emis_nmoc_fsrt = calc_species(all_fsrt, ef_nmoc)
        emis_nh3_fsrt = calc_species(all_fsrt, ef_nh3)
        emis_no_fsrt = calc_species(all_fsrt, ef_no)
        emis_no2_fsrt = calc_species(all_fsrt, ef_no2)
        emis_nox_fsrt = calc_species(all_fsrt, ef_nox)
        emis_so2_fsrt = calc_species(all_fsrt, ef_so2)
        
        # --- Separate pile calculations ---
        (all_loadings, pile_loadings, pile_black_pct) = pile_info(self._cons_object)
        (pile_pm, pile_pm10, pile_pm25) = \
            self._emissions_calc_pm_piles(all_loadings, pile_loadings, pile_black_pct)

        # Add pile PM contribution in. Add to the totals (index 0) and the woody stratum (index 6)
        if self._no_sera:
            emis_pm_fsrt[0] = emis_pm_fsrt[0] + pile_pm
            emis_pm_fsrt[6] = emis_pm_fsrt[6] + pile_pm
        emis_pm10_fsrt[0] = emis_pm10_fsrt[0] + pile_pm10
        emis_pm10_fsrt[6] = emis_pm10_fsrt[6] + pile_pm10
        emis_pm25_fsrt[0] = emis_pm25_fsrt[0] + pile_pm25
        emis_pm25_fsrt[6] = emis_pm25_fsrt[6] + pile_pm25

        (pile_co, pile_co2, pile_ch4, pile_nmhc, pile_nmoc, pile_nh3, pile_no, pile_no2, pile_nox, pile_so2) = \
            self._emissions_calc_pollutants_piles(pile_loadings, pile_black_pct)
        emis_co_fsrt[0] = emis_co_fsrt[0] + pile_co
        emis_co_fsrt[6] = emis_co_fsrt[6] + pile_co
        emis_co2_fsrt[0] = emis_co2_fsrt[0] + pile_co2
        emis_co2_fsrt[6] = emis_co2_fsrt[6] + pile_co2
        emis_ch4_fsrt[0] = emis_ch4_fsrt[0] + pile_ch4
        emis_ch4_fsrt[6] = emis_ch4_fsrt[6] + pile_ch4
        if self._no_sera:
            emis_nmhc_fsrt[0] = emis_nmhc_fsrt[0] + pile_nmhc
            emis_nmhc_fsrt[6] = emis_nmhc_fsrt[6] + pile_nmhc
        emis_nmoc_fsrt[0] = emis_nmoc_fsrt[0] + pile_nmoc
        emis_nmoc_fsrt[6] = emis_nmoc_fsrt[6] + pile_nmoc
        # new pollutants from SERA
        emis_nh3_fsrt[0] = emis_nh3_fsrt[0] + pile_nh3
        emis_nh3_fsrt[6] = emis_nh3_fsrt[6] + pile_nh3
        emis_no_fsrt[0] = emis_no_fsrt[0] + pile_no
        emis_no_fsrt[6] = emis_no_fsrt[6] + pile_no
        emis_no2_fsrt[0] = emis_no2_fsrt[0] + pile_no2
        emis_no2_fsrt[6] = emis_no2_fsrt[6] + pile_no2
        emis_nox_fsrt[0] = emis_nox_fsrt[0] + pile_nox
        emis_nox_fsrt[6] = emis_nox_fsrt[6] + pile_nox
        emis_so2_fsrt[0] = emis_so2_fsrt[0] + pile_so2
        emis_so2_fsrt[6] = emis_so2_fsrt[6] + pile_so2
        # ^^^ Separate pile calculations ^^^

        #print "UNPACKING"
        self._emis_data = arrayize([emis_pm_fsrt, emis_pm10_fsrt, emis_pm25_fsrt,
                   emis_co_fsrt, emis_co2_fsrt, emis_ch4_fsrt, emis_nmhc_fsrt, emis_nmoc_fsrt, 
                   emis_nh3_fsrt, emis_no_fsrt, emis_no2_fsrt, emis_nox_fsrt, emis_so2_fsrt])

        #print "ADDING PER AREA STUFF"
        # And emissions per-unit-area summaries:
        area = self._cons_object._settings.get('area')
        if len(area) == 1:
            area = np.array(np.array([1] * num_fuelbeds), dtype=float) * area
        tot_area = sum(area)

        pm_all = get_emis_summ(0)
        pm10_all = get_emis_summ(1)
        pm25_all = get_emis_summ(2)
        co_all = get_emis_summ(3)
        co2_all = get_emis_summ(4)
        ch4_all = get_emis_summ(5)
        nmhc_all = get_emis_summ(6)
        nmoc_all = get_emis_summ(7)
        nh3_all = get_emis_summ(8)
        no_all = get_emis_summ(9)
        no2_all = get_emis_summ(10)
        nox_all = get_emis_summ(11)
        so2_all = get_emis_summ(12)

        # ks todo - what does this do?
        self._emis_summ = np.array([pm_all, pm10_all, pm25_all, co_all, co2_all, ch4_all, nmhc_all, nmoc_all, nh3_all, no_all, no2_all, nox_all, so2_all])
        # the only problem this line causes is if unit conversion is involved
        # self._emis_summ = np.array([0, 0, 0, 0, 0, 0, 0])

        # - restore pile consumption
        all_fsrt[0] = all_fsrt[0] + self._cons_object._cons_data_piles
        all_fsrt[6] = all_fsrt[6] + self._cons_object._cons_data_piles


