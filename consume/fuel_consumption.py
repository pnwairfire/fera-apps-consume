"""
### GETTING STARTED with the FUEL CONSUMPTION OBJECT ###

Open a Python shell program (e.g. IDLE, ipython, etc.).
Import the module:

>>> import consume

Declare a Consume FuelConsumption object:

>>> fc_obj = consume.FuelConsumption()

--Note: if the .xml fuel loading database is located somewhere other than
    the default location, user can specify this using the 'fccs_file' argument,
    e.g.:
    fc_obj = consume.FuelConsumption(fccs_file="C:/Documents/FCCSLoadings.xml")



### SETTING INPUT PARAMETERS ###

There are a number of alternative options for setting input values:

    1. Start a program that will prompt the user for inputs:
        >>> fc_obj.prompt_for_inputs()


    2. Load inputs from a pre-formatted csv file (see example file:
        "consume_inputs_example.csv" for correct formatting):

        >>> fc_obj.load_scenario("myscenario.csv")

        --OR to load, calculate outputs, and store outputs at once, use the
          batch_process method:

        >>> fc_obj.batch_process("myscenario.csv", "myoutputs.csv")


    3. Individually set/change input values manually:
        >>> fc_obj.burn_type = <'natural' or 'activity'>
        >>> fc_obj.fuelbed_fccs_ids = [FCCSID#1,FCCSID#2,...]
        >>> fc_obj.fuelbed_area_acres = [AREA#1,AREA#2,...]
        >>> fc_obj.fuelbed_ecoregion = [ECOREGION#1, ECOREGION#2,...]
        >>> fc_obj.fuel_moisture_1000hr_pct = [1000hrFM#1, 1000hrFM#2,...]
        >>> fc_obj.fuel_moisture_duff_pct = [DuffFM#1, DuffFM#2, ...]
        >>> fc_obj.canopy_consumption_pct = [PctCan#1, PctCan#2,...]
        >>> fc_obj.shrub_blackened_pct = [PercentShrub#1, PercentShrub#2,...]

        ---inputs specific to 'activity' burns:
        >>> fc_obj.fuel_moisture_10hr_pct = [10HourFM#1, 10HourFM#2, ...]
        >>> fc_obj.slope = [Slope#1, Slope#2, ...]
        >>> fc_obj.windspeed = [Windspeed#1, Windspeed#2, ...]
        >>> fc_obj.fm_type = <'MEAS-Th', 'ADJ-Th', or 'NFDRS-Th'>
        >>> fc_obj.days_since_rain = [Days#1, Days#2, ...]
        >>> fc_obj.length_of_ignition = [Length#1, Length#2, ...]


        --Note: When setting input values, the user can also select a SINGLE
            value (instead of a list) for any environment variable that will
            apply to the entire scenario.
            These environment variables include the following:
            ecoregion, fuel_moisture_1000hr_pct,  fuel_moisture_duff_pct,
            canopy_consumption_pct, shrub_blackened_pct, slope, windpseed,
            fm_type, days_since_rain, length_of_ignition


     Description of the input parameters:

        burn_type
                : Use this variable to select 'natural' burn equations or
                  'activity' (i.e. prescribed) burn equations. Note that
                  'activity' burns require 6 additional input parameters:
                  10hr fuel moisture, slope, windpseed, fuel moisture type,
                  days since significant rainfall, and length of ignition.

        fuelbed_fccs_ids
                : a list of Fuel Characteristic Classification System (FCCS)
                  (http://www.fs.fed.us/pnw/fera/fccs/index.shtml) fuelbed ID
                  numbers (1-291).  Use the .FCCS.browse() method to load a list
                  of all FCCS ID#'s and their associated site names. Use
                  .FCCS.info(id#) to get a site description of the
                  specified FCCD ID number. To get a complete listing of fuel
                  loadings for an FCCS fuelbed, use:
                  .FCCS.info(id#, detail=True)

        fuelbed_area_acres
                : a list (or single number to be used for all fuelbeds) of
                  numbers in acres that represents area for the corresponding
                  FCCS fuelbed ID listed in the 'fuelbeds_fccs_ids' variable.

        fuelbed_ecoregion
                : a list (or single region to be used for all fuelbeds) of
                  ecoregions ('western', 'southern', or 'boreal') that
                  represent the ecoregion for the corresponding FCCS fuelbed ID
                  listed in the 'fuelbeds_fccs_ids' variable. Regions within the
                  US that correspond to each broad regional description can be
                  found in the official Consume 3.0 User's Guide, p. 60. Further
                  info on Bailey's ecoregions can be found here:
                www.eoearth.org/article/Ecoregions_of_the_United_States_(Bailey)
                  Default is 'western'

        fuel_moisture_1000hr_pct
                : 1000-hr fuel moisture in the form of a number or list of
                  numbers ranging from 0-100 representing a percentage.
                  Default is 50%

        fuel_moisture_10hr_pct
                : <specific to 'activity' burns>
                  10-hr fuel moisture in the form of a number or list of
                  numbers ranging from 0-100 representing a percentage.
                  Default is 50%

        fuel_moisture_duff_pct
                : Duff fuel moisture. A number or list of numbers ranging from
                  0-100 representing a percentage.
                  Default is 50%.

        canopy_consumption_pct
                : Percent canopy consumed. A number or list of numbers ranging
                  from 0-100 representing a percentage. Set to '-1' to
                  use an FCCS-fuelbed dependent precalculated canopy consumption
                  percentage based on crown fire initiation potential, crown to
                  crown transmissivity, and crown fire spreading potential.
                  (note: auto-calc is not available for FCCS ID's 401-456)
                  Default is -1

        shrub_blackened_pct
                : Percent of shrub that has been blackened. A number or list
                  of numbers ranging from 0-100 representing a percentage.
                  Default is 50%

        slope
                : <specific to 'activity' burns>
                  Percent slope of a fuelbed unit. Used in predicting 100-hr
                  (1-3" diameter) fuel consumption in 'activity' fuelbeds.
                  Valid values: a number or list of numbers ranging from 0-100
                  representing a percentage.
                  Default is 5%

        windspeed
                : <specific to 'activity' burns>
                  Mid-flame wind speed (mph) during the burn. Maximum is 35 mph.
                  Used in predicting 100-hr (1-3" diameter) fuel consumption in
                  'activity' fuelbeds.
                  Default is 5 mph

        fm_type
                : <specific to 'activity' burns>
                  Source of 1000-hr fuel moisture data.
                    "Meas-Th" (default) : measured directly
                    "NFDRS-Th" : calculated from NFDRS
                    "ADJ-Th" : adjusted for PNW conifer types
                  Note: 1000-hr fuel moisture is NOT calculated by Consume,
                  i.e. user must derive 1000-hr fuel moisture & simply select
                  the method used.

        days_since_rain
                : <specific to 'activity' burns>
                  Number of days since significant rainfall. According to the
                  Consume 3.0 User's Guide, "Significant rainfall is one-quarter
                  inch in a 48-hour period." Used to predict duff consumption
                  in 'activity' fuelbeds.

        length_of_ignition
                : <specific to 'activity' burns>
                  The amount of time (minutes) it will take to ignite the area
                  to be burned. Used to determine if a fire will be of high
                  intensity, which affects diameter reduction of large woody
                  fuels in 'activity' fuelbeds.

The user can also optionally set alternate output units. Use the
list_valid_units() method to view output unit options.
Default fuel consumption units are tons/acre ('tons_ac').

>>> consume.list_valid_units()
Out:
['lbs',
 'lbs_ac',
 'tons',
 'tons_ac',
 'kg',
 'kg_m^2',
 'kg_ha',
 'kg_km^2'
 'tonnes',
 'tonnes_ha',
 'tonnes_km^2']


>>> fc_obj.output_units = 'lbs'


### CUSTOMIZING FUEL LOADINGS ###

Fuel loadings are automatically imported from the FCCS database based on the
FCCS fuelbed ID#s selected by the user. If desired, the user can also
customize FCCS fuel loadings by setting the '.customized_fuel_loadings' variable
to a list of 3 value lists in this format:
[fuelbed index number {interger}, fuel stratum {string}, loading value {number}]

e.g.:
>>> fc_obj.customized_fuel_loadings = [[1, 'overstory', 4.5],[2, 'shrub_prim', 5]]

The above command will change the canopy 'overstory' loading in the first ('1')
fuelbed to 4.5 (tons/acre) and will change the 'shrub_prim' (primary shrub
loading) in the second ('2') fuelbed to 5 tons/acre. To view all valid stratum
names and units, use the fc_obj.FCCS.list_fuel_loading_names() method.


### OUTPUTS ###

Consumption outputs can be accessed by calling the .results(), .report(), or
.batch_process() methods. Calling any of these methods will trigger the
calculation of all fuel consumption equation and will return the results in
a variety of different formats:


>>> fc_obj.results()
                    ...generates & prints a python DICTIONARY of consumption
                       results by fuel category (major and minor categories)
                       See complete example below to see how individual
                       data categories can be accessed from this dictionary.

>>> fc_obj.report(csv="")
                    ...prints a TABULAR REPORT of consumption results for
                       the major fuel categories (similar to the "Fuel
                       Consumption by Combustion Stage" report produced by the
                       official Consume 3.0 GUI program).  To export a version
                       of this report as a CSV FILE, use the 'csv' argument to
                       specify a file name, e.g.:
                       >>> fc_obj.report(csv = "consumption_report.csv")

>>> fc_obj.batch_process(csvin="", csvout="")
                    ...similar to the .report() method, although requires an
                       input csv file and will export results to the specified
                       CSV output.



### OTHER USEFUL METHODS ###

>>> consume.list_valid_units()        ...displays a list of valid output unit
                                         options

>>> consume.list_valid_consumption_strata()
                                      ...displays a list of valid consumption
                                         strata group names

>>> fc_obj.list_variable_names()      ...displays a list of the variable names
                                         used for each input parameter

>>> fc_obj.FCCS.browse()              ...loads a list of all FCCS fuelbed ID
                                         numbers and their site names

>>> fc_obj.FCCS.info(#)               ...provides site description of the FCCS
                                         fuelbed with the specified ID number.
                                         Set detail=True to print out detailed
                                         fuel loading information

>>> fc_obj.FCCS.get_canopy_pct(#)     ...displays estimated canopy consumption
                                         percent as calculated by MTRI for the
                                         specified FCCS ID number. This is the
                                         value that will be used if
                                         canopy_consumption_pct is set to -1.

>>> fc_obj.load_example()             ...loads an example scenario with 2
                                         fuelbeds

>>> fc_obj.reset_inputs_and_outputs() ...clears input and output parameters

>>> fc_obj.display_inputs()           ...displays a list of the input parameters.
                                         Useful for checking that scenario
                                         parameters were set correctly

###################################################
           Complete Uninterrupted Example
###################################################

The following example sets up a 'natural' burn scenario in which 100 acres FCCS
fuelbed ID #1 ("Black cottonwood - Douglas fir - Quaking aspen riparian forest")
and 200 acres of FCCS fuelbed ID #47 ("Redwood - Tanoak forest") are consumed.
1000-hr and duff fuel moisture is set at 50% for fuelbed ID #1 and 40% for
fuelbed ID #47. Canopy consumption and shrub percent black is set at 25% for
both fuelbeds.


>>> import consume
>>> fc_obj = consume.FuelConsumption()
>>> fc_obj.fuelbed_fccs_ids = [1, 47]
>>> fc_obj.fuelbed_area_acres = [100, 200]
>>> fc_obj.fuelbed_ecoregion = 'western'
>>> fc_obj.fuel_moisture_1000hr_pct = [50, 40]
>>> fc_obj.fuel_moisture_duff_pct = [50, 40]
>>> fc_obj.canopy_consumption_pct = 25
>>> fc_obj.shrub_blackened_pct = 25
>>> fc_obj.output_units = 'kg_ha'
>>> fc_obj.display_inputs()

Out:

Current scenario parameters:

Parameter			        Value(s)
--------------------------------------------------------------
Burn type			        natural
FCCS fuelbeds (ID#)		    [1, 47]
Fuelbed area (acres)	    [100, 200]
Fuelbed ecoregion		    western
Fuel moisture (1000-hr, %)	[50, 40]
Fuel moisture (duff, %)		[50, 40]
Canopy consumption (%)		25
Shrub blackened (%)		    25
Output units			    kg_ha


>>> fc_obj.report()

Out:

FUEL CONSUMPTION
Consumption units: kg/ha
Heat release units: btu/ha
Total area: 300 acres


FCCS ID: 1
Area:	100
Ecoregion: western
CATEGORY	    Flaming		Smoldering	Residual	TOTAL
canopy		    1.25e+04	9.58e+02	1.51e+02	1.36e+04
shrub		    1.26e+03	6.97e+01	0.00e+00	1.33e+03
nonwoody	    3.95e+02	2.08e+01	0.00e+00	4.16e+02
llm		        2.32e+03	2.20e+02	0.00e+00	2.54e+03
ground fuels	8.97e+02	1.51e+04	3.72e+04	5.32e+04
woody fuels	    9.71e+03	5.61e+03	8.81e+03	2.41e+04
TOTAL:		    2.70e+04	2.20e+04	4.61e+04	9.52e+04

Heat release:	1.19e+08	9.70e+07	2.03e+08	4.20e+08


FCCS ID: 47
Area:	200
Ecoregion: western
CATEGORY	    Flaming		Smoldering	Residual	TOTAL
canopy		    7.93e+03	2.48e+03	2.05e+03	1.25e+04
shrub		    3.87e+03	2.69e+02	0.00e+00	4.13e+03
nonwoody	    9.88e+02	5.20e+01	0.00e+00	1.04e+03
llm		        4.93e+03	5.41e+02	0.00e+00	5.47e+03
ground fuels	3.59e+03	4.08e+04	6.98e+04	1.14e+05
woody fuels	    2.56e+04	2.06e+04	2.49e+04	7.11e+04
TOTAL:		    4.69e+04	6.47e+04	9.67e+04	2.08e+05

Heat release:	2.07e+08	2.85e+08	4.27e+08	9.18e+08


ALL FUELBEDS:

Consumption:	4.03e+04	5.04e+04	7.99e+04	1.71e+05
Heat release:	3.26e+08	3.82e+08	6.30e+08	1.34e+09



>>> fc_obj.results()['consumption']['ground fuels']

Out:
{'basal accumulations': {'flaming': array([-0.,  0.]),
                         'residual': array([-0.,  0.]),
                         'smoldering': array([-0.,  0.]),
                         'total': array([-0.,  0.])},
 'duff, lower': {'flaming': array([ 0.,  0.]),
                 'residual': array([ 35377.20573062,  62608.52081126]),
                 'smoldering': array([  8844.30143266,  15652.13020281]),
                 'total': array([ 44221.50716328,  78260.65101407])},
 'duff, upper': {'flaming': array([  896.68092549,  3586.72370195]),
                 'residual': array([ 1793.36185097,  7173.4474039 ]),
                 'smoldering': array([  6276.76647841,  25107.06591365]),
                 'total': array([  8966.80925487,  35867.23701949])},
 'squirrel middens': {'flaming': array([ 0.,  0.]),
                      'residual': array([ 0.,  0.]),
                      'smoldering': array([ 0.,  0.]),
                      'total': array([ 0.,  0.])}}

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

To access TOTAL consumption for the given scenario for each fuelbed unit:
fc_obj.results()['consumption']['summary']['total']['total']

To access TOTAL consumption for only the first fuelbed unit in the scenario:
fc_obj.results()['consumption']['summary']['total']['total'][0]

To access TOTAL consumption for the given scenario across ALL fuelbeds*:
sum(fc_obj.results()['consumption']['summary']['total']['total'])

To access consumption data for all canopy strata:
fc_obj.results()['consumption']['canopy']

To access TOTAL canopy consumption:
fc_obj.results()['consumption']['summary']['canopy']['total']

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
import math
import numpy as np
import fccs_db as fccs
import data_desc as dd
import util_consume as util
import con_calc_natural as ccn
import con_calc_activity as cca
import input_settings as settings
import logging
import pandas as pan

msg = logging.getLogger(__name__)
msg.addHandler(logging.StreamHandler())

### - uncomment to enable basic file tracing of just the consume calls
#import os
#import sys
#import sysconfig
#sys.settrace(util.trace_calls)


# Variables that need to be defined for these equations
#snow_free_days = 30 # need for curing eval, if still valid


#class FuelConsumption(object):
class FuelConsumption(util.FrozenClass):
    """A class that estimates fuel consumption due to fire.

    This class implements the CONSUME model equations for estimating fuel
    consumption due to fire.

    There are no required arguments for declaring a FuelConsumption class
    object. The user can optionally set the 'fccs_file' argument to the directory
    location of the FCCS fuel loadings xml file if it does not reside in the
    default location.

    Input parameters to the FuelConsumption object are described below.
    Values can be input in one of several ways:
        -manually (e.g. "fc_obj.fuelbed_fccs_ids = [1,5]", etc.)
        -via the .prompt_for_inputs() method
        -by loading a preformatted csv (see 'consume_batch_inputs_example.csv'
         file) using the .load_scenario(csv=INPUTCSV) or using the
         .batch_process(csv_in=INPUTCSV, csv_out=OUTPUTCSV) method

    Description of the input parameters:

        burn_type
                : Use this variable to select 'natural' burn equations or
                  'activity' (i.e. prescribed) burn equations. Note that
                  'activity' burns require 6 additional input parameters:
                  10hr fuel moisture, slope, windpseed, fuel moisture type,
                  days since significant rainfall, and length of ignition.

        fuelbed_fccs_ids
                : a list of Fuel Characteristic Classification System (FCCS)
                  (http://www.fs.fed.us/pnw/fera/fccs/index.shtml) fuelbed ID
                  numbers (1-291).  Use the .FCCS.browse() method to load a list
                  of all FCCS ID#'s and their associated site names. Use
                  .FCCS.info(id#) to get a site description of the
                  specified FCCD ID number. To get a complete listing of fuel
                  loadings for an FCCS fuelbed, use:
                  .FCCS.info(id#, detail=True)

        fuelbed_area_acres
                : a list (or single number to be used for all fuelbeds) of
                  numbers in acres that represents area for the corresponding
                  FCCS fuelbed ID listed in the 'fuelbeds_fccs_ids' variable.

        fuelbed_ecoregion
                : a list (or single region to be used for all fuelbeds) of
                  ecoregions ('western', 'southern', or 'boreal') that
                  represent the ecoregion for the corresponding FCCS fuelbed ID
                  listed in the 'fuelbeds_fccs_ids' variable. Regions within the
                  US that correspond to each broad regional description can be
                  found in the official Consume 3.0 User's Guide, p. 60. Further
                  info on Bailey's ecoregions can be found here:
                www.eoearth.org/article/Ecoregions_of_the_United_States_(Bailey)
                  Default is 'western'

        fuel_moisture_1000hr_pct
                : 1000-hr fuel moisture in the form of a number or list of
                  numbers ranging from 0-100 representing a percentage.
                  Default is 50%

        fuel_moisture_10hr_pct
                : <specific to 'activity' burns>
                  10-hr fuel moisture in the form of a number or list of
                  numbers ranging from 0-100 representing a percentage.
                  Default is 50%

        fuel_moisture_duff_pct
                : Duff fuel moisture. A number or list of numbers ranging from
                  0-100 representing a percentage.
                  Default is 50%.

        canopy_consumption_pct
                : Percent canopy consumed. A number or list of numbers ranging
                  from 0-100 representing a percentage. Set to '-1' to
                  use an FCCS-fuelbed dependent precalculated canopy consumption
                  percentage based on crown fire initiation potential, crown to
                  crown transmissivity, and crown fire spreading potential.
                  (note: auto-calc is not available for FCCS ID's 401-456)
                  Default is -1

        shrub_blackened_pct
                : Percent of shrub that has been blackened. A number or list
                  of numbers ranging from 0-100 representing a percentage.
                  Default is 50%

        slope
                : <specific to 'activity' burns>
                  Percent slope of a fuelbed unit. Used in predicting 100-hr
                  (1-3" diameter) fuel consumption in 'activity' fuelbeds.
                  Valid values: a number or list of numbers ranging from 0-100
                  representing a percentage.
                  Default is 5%

        windspeed
                : <specific to 'activity' burns>
                  Mid-flame wind speed (mph) during the burn. Maximum is 35 mph.
                  Used in predicting 100-hr (1-3" diameter) fuel consumption in
                  'activity' fuelbeds.
                  Default is 5 mph

        fm_type
                : <specific to 'activity' burns>
                  Source of 1000-hr fuel moisture data.
                    "Meas-Th" (default) : measured directly
                    "NFDRS-Th" : calculated from NFDRS
                    "ADJ-Th" : adjusted for PNW conifer types
                  Note: 1000-hr fuel moisture is NOT calculated by Consume,
                  i.e. user must derive 1000-hr fuel moisture & simply select
                  the method used.

        days_since_rain
                : <specific to 'activity' burns>
                  Number of days since significant rainfall. According to the
                  Consume 3.0 User's Guide, "Significant rainfall is one-quarter
                  inch in a 48-hour period." Used to predict duff consumption
                  in 'activity' fuelbeds.

        length_of_ignition
                : <specific to 'activity' burns>
                  The amount of time (minutes) it will take to ignite the area
                  to be burned. Used to determine if a fire will be of high
                  intensity, which affects diameter reduction of large woody
                  fuels in 'activity' fuelbeds.

    Classes:
        .FCCS   : an FCCSDB object stored in the FuelConsumption object from
                  which FCCS fuel loading information is derived. Use
                  help(consume.FCCSDB) to view available methods.

    """
    @property
    def fm_type(self): return self._settings.fm_type
    @fm_type.setter
    def fm_type(self, value):
        self._settings.fm_type = value
    @property
    def burn_type(self): return self._settings.burn_type
    @burn_type.setter
    def burn_type(self, value):
        self._settings.burn_type = value
    @property
    def output_units(self): return self._settings.units
    @output_units.setter
    def output_units(self, value):
        self._settings.units =  value

    @property
    def fuelbed_fccs_ids(self): return self._settings.get('fuelbeds')
    @fuelbed_fccs_ids.setter
    def fuelbed_fccs_ids(self, value):
        self._settings.set('fuelbeds', value)
    @property
    def fuelbed_area_acres(self): return self._settings.get('area')
    @fuelbed_area_acres.setter
    def fuelbed_area_acres(self, value):
        self._settings.set('area', value)
    @property
    def fuelbed_ecoregion(self): return self._settings.get('ecoregion')
    @fuelbed_ecoregion.setter
    def fuelbed_ecoregion(self, value):
        self._settings.set('ecoregion', value)
    @property
    def fuel_moisture_1000hr_pct(self): return self._settings.get('fm_1000hr')
    @fuel_moisture_1000hr_pct.setter
    def fuel_moisture_1000hr_pct(self, value):
        self._settings.set('fm_1000hr', value)
    @property
    def fuel_moisture_duff_pct(self): return self._settings.get('fm_duff')
    @fuel_moisture_duff_pct.setter
    def fuel_moisture_duff_pct(self, value):
        self._settings.set('fm_duff', value)
    @property
    def fuel_moisture_10hr_pct(self): return self._settings.get('fm_10hr')
    @fuel_moisture_10hr_pct.setter
    def fuel_moisture_10hr_pct(self, value):
        self._settings.set('fm_10hr', value)
    @property
    def canopy_consumption_pct(self): return self._settings.get('can_con_pct')
    @canopy_consumption_pct.setter
    def canopy_consumption_pct(self, value):
        self._settings.set('can_con_pct', value)
    @property
    def shrub_blackened_pct(self): return self._settings.get('shrub_black_pct')
    @shrub_blackened_pct.setter
    def shrub_blackened_pct(self, value):
        self._settings.set('shrub_black_pct', value)
    @property
    def pile_blackened_pct(self): return self._settings.get('pile_black_pct')
    @pile_blackened_pct.setter
    def pile_blackened_pct(self, value):
        self._settings.set('pile_black_pct', value)
    @property
    def slope(self): return self._settings.get('slope')
    @slope.setter
    def slope(self, value):
        self._settings.set('slope', value)
    @property
    def windspeed(self): return self._settings.get('windspeed')
    @windspeed.setter
    def windspeed(self, value):
        self._settings.set('windspeed', value)
    @property
    def days_since_rain(self): return self._settings.get('days_since_rain')
    @days_since_rain.setter
    def days_since_rain(self, value):
        self._settings.set('days_since_rain', value)
    @property
    def length_of_ignition(self): return self._settings.get('length_of_ignition')
    @length_of_ignition.setter
    def length_of_ignition(self, value):
        self._settings.set('length_of_ignition', value)

    @property
    def msg_level(self): return self._msg_level
    @msg_level.setter
    def msg_level(self, value):
        assert 0 <= value and value <= 50
        self._msg_level = value


    def __init__(self, fccs_file = "", msg_level=logging.ERROR):
        """FuelConsumption class constructor

        Upon initialization of the FuelConsumption object, all input
        variables are declared and FCCS data is loaded as an FCCSDB object that
        is stored as self.FCCS(loading FCCS information may take a few seconds).

        User can optionally specify the directory location of the default xml
        FCCS database that is used to derive fuel loading information:

        Optional argument:

        fccs_file   : Location of the .xml file that contains all FCCS fuel
                      loading information. The default location is:
                      "[python-consume dir.]/input_data/fccs_loadings_1_458.xml.xml"

        """
        self.msg_level = msg_level
        msg.setLevel(self.msg_level)
        # msg.debug("debug message")
        # msg.info("info message")
        # msg.warning("warning message")
        # msg.error("error message")

        self.FCCS = fccs.FCCSDB(fccs_file)
        self._settings = settings.ConsumeInputSettings()

        ### - reset outputs
        self.customized_fuel_loadings = []
        self._fccs_loadings = []
        self._cons_data = np.array([])
        self._cons_debug_data = np.array([])
        self._emis_data = np.array([])
        self._calc_success = False
        self._conv_success = False
        self._unique_check = False

        self._msg_level = logging.ERROR
        self._calc_success = False
        self._unq_inputs = []
        self._runlnk = []
        self._internal_units = 'tons_ac'
        self.output_units = self._internal_units
        self._conv_success = False
        self._ucons_data = None
        self._heat_data = None
        self._cons_data = None

        self._freeze()

    def _reset_outputs(self):
        self.customized_fuel_loadings = []
        self._fccs_loadings = []
        self._cons_data = np.array([])
        self._cons_debug_data = np.array([])
        self._emis_data = np.array([])
        self._calc_success = False
        self._conv_success = False
        self._unique_check = False

        self._msg_level = logging.ERROR
        self._calc_success = False
        self._unq_inputs = []
        self._runlnk = []
        self._internal_units = 'tons_ac'
        self.output_units = self._internal_units
        self._conv_success = False
        self._ucons_data = None
        self._heat_data = None
        self._cons_data = None

    def results(self):
        """Output fuel consumption results as a python DICTIONARY object

        Returns a python dictionary comprised of input and output data.
        Calling this method will only return output data if the input data is
        already set.

        See "Navigating the .results()" dictionaries in the README at the top
        of this file for detailed information on the structure of the dictionary
        and examples of how to extract information from the dictionary.

        """
        self._calculate()
        if self._calc_success:
            self._convert_units()
            self._conv_success = True
            if self._conv_success:
                return util.make_dictionary_of_lists(cons_data = self._cons_data,
                                          cons_debug_data = self._cons_debug_data,
                                          heat_data = self._heat_data,
                                          emis_data = [],
                                          inputs = self._settings.package(self.FCCS.loadings_data_))

    def report(self, csv = "", stratum = "all", ret=False, incl_heat=False):
        """Output fuel consumption results as a TABULAR REPORT and/or CSV FILE

        Displays (in shell) consumption data in tabular format, similar to
        how the official GUI CONSUME reports consumption by combustion stage.

        Optional arguments:

        csv         : Location of a CSV FILE in which to export consumption
                      data. No file will be exported if left blank.

        stratum     : Filters exported data by the specified fuel strata.
                      Default is 'total'. Valid values: 'all', 'total',
                      'canopy', 'woody fuels', 'shrub', 'nonwoody',
                      'ground fuels', 'litter-lichen-moss'

        """

        self._calculate()
        if self._calc_success:
            self._convert_units()
            if self._conv_success:
                if not ret:
                    self._display_report(csv, stratum, incl_heat = incl_heat, ret=ret)
                else:
                    return self._display_report(csv, stratum, incl_heat = incl_heat, ret=ret)



    def batch_process(self, csv_in, csv_out, stratum = 'total',
                      incl_heat = False):

        """Processes an csv file of consume inputs and outputs to csv

            See 'consume_batch_input_example.csv' for formatting guidance.
            Column headings in an input batch file MUST conform to those in the
            example file.

            Required arguments:

            csv_in  : directory location of the CSV file containing the input
                      data e.g. "/home/username/my_consume_inputs.csv". See
                      'consume_batch_input_example.csv' in the python-consume
                      download directory for formatting guidance.

            csv_out : directory location of the CSV file that will be written as
                      an output e.g. "C:/consume/outputs/my_consume_outputs.csv"


            Optional arguments:

            stratum   : Filters exported data by the specified fuel strata.
                        Default is 'total'. Valid values: 'all', 'total',
                        'canopy', 'woody fuels', 'shrub', 'nonwoody',
                        'ground fuels', 'litter-lichen-moss'

            incl_heat : Specifies whether or not to include heat release data
                        in the output csv file. Default is 'False'.
        """
        self.report(csv = csv_out, stratum = stratum)
        print "\nFile saved to: " + csv_out


    def display_inputs(self, print_to_console=True):
        """Lists the input parameters for the consumption scenario.

        Displays the input parameters for the consumption in the shell. Useful
        as a quick way to check that the scenario parameters have been
        correctly set.

        """
        return self._settings.display_settings()

    def load_scenario(self, load_file='', display=True):
        """Loads scenario input parameters from a CSV file

        Required argument:

        load_file  : directory location of the CSV file from which the scenario
                     will be loaded. See 'consume_batch_input_example.csv' for
                     formatting guidance.

        """
        return self._settings.load_from_file(load_file)

    def _display_report(self, csv, stratum = 'all', incl_heat = False, ret=False):
        """Displays an in-shell report on consumption values"""

        categories = ["canopy\t", "shrub\t", "nonwoody", "llm  \t",
                      "ground fuels", "woody fuels"]

        units = self._settings.units
        fccs_ids = self._settings.get('fuelbeds')
        area = self._settings.get('area')
        ecoregion = self._settings.get('ecoregion')
        fm_1000hr = self._settings.get('fm_1000hr')
        fm_duff = self._settings.get('fm_duff')
        fm_can = self._settings.get('can_con_pct')
        fm_shb = self._settings.get('shrub_black_pct')
        hr_au = "btu"
        str_au = units

        cons_data = self._cons_data
        heat_data = self._heat_data

        if units in dd.perarea() and sum(area) > 0:
            str_au = "/".join(units.split("_"))
            hr_au = "btu/" + units.split("_")[1]


        if len(area) == 1:
            area = np.array([1] * len(fccs_ids), dtype=float) * area

        if len(ecoregion) == 1:
            ecoregion = ecoregion * len(fccs_ids)

        if len(fm_1000hr) == 1:
            fm_1000hr = np.array([1] * len(fccs_ids), dtype=float) * fm_1000hr

        if len(fm_duff) == 1:
            fm_duff = np.array([1] * len(fccs_ids), dtype=float) * fm_duff

        if len(fm_can) == 1:
            fm_can = np.array([1] * len(fccs_ids), dtype=float) * fm_can

        if len(fm_shb) == 1:
            fm_shb = np.array([1] * len(fccs_ids), dtype=float) * fm_shb


        if stratum == "all":
            catrange = range(1, 7)
        elif stratum == "total":
            catrange = range(0, 0)
        elif stratum in [s.rstrip("\t") for s in categories]:
            strat = stratum
            strat += "\t" if strat in ["canopy", "shrub", "llm"] else ""
            catrange = range(categories.index(strat) + 1, categories.index(strat) + 2)
        else:
            print ('ERROR: Invalid consumption strata. Please choose among:\n' +
                   ','.join(dd.list_valid_consumption_strata()) + ', all, or total')


        txt = ""
        txt += ("\n\nFUEL CONSUMPTION\nConsumption units: " + str_au +
            "\nHeat release units: " + hr_au +
            "\nTotal area: %.0f" % sum(np.array(area)) + " acres")

        csv_lines = ("unitID,fccsID,ecoregion,area,1000hr_fm,duff_fm,"
                     + "canopy_consumed_pct,shrub_blackened_pct,units,"
                     + "category,flaming,smoldering,residual,total\n")

        def fix(dat):
            tmp = "\t%.2e" % dat
            if dat < 1 and dat > 0:
                tmp += " "
            return tmp

        for i in range(0, len(fccs_ids)):

            txt += ("\n\nFCCS ID: " + str(fccs_ids[i])
            + "\nArea:\t%.0f" % area[i] + "\nEcoregion: " + ecoregion[i]
            + "\nCATEGORY\tFlaming\t\tSmoldering\tResidual\tTOTAL")

            fm_hdr = (str(fm_1000hr[i]) + ',' + str(fm_duff[i]) +
                      ',' + str(fm_can[i]) + ',' + str(fm_shb[i]) + ',')

            unitID = i + 1
            csv_header = (','.join([str(unitID), str(fccs_ids[i]), ecoregion[i],
                                   str(area[i]), fm_hdr]) )


            for j in range(1, 7):
                txt += ('\n' + categories[j - 1] +
                        ''.join([fix(cons_data[j][p][i]) for p in [0,1,2,3]]))

            for j in catrange:
                csv_lines += (csv_header + str_au + ',' +
                              categories[j - 1].rstrip('\t') + ',' +
                              str(cons_data[j][0][i]) + ',' +
                              str(cons_data[j][1][i]) + ',' +
                              str(cons_data[j][2][i]) + ',' +
                              str(cons_data[j][3][i]) + "\n")

            txt += ("\nTOTAL:\t" +
                    ''.join([fix(cons_data[0][p][i]) for p in [0,1,2,3]]))

            if stratum in ['all', 'total']:
                csv_lines += (csv_header + str_au + ',total consumption,' +
                              str(cons_data[0][0][i]) + ',' +
                              str(cons_data[0][1][i]) + ',' +
                              str(cons_data[0][2][i]) + ',' +
                              str(cons_data[0][3][i]) + '\n')

            txt += ("\n\nHeat release:\t%.2e" % heat_data[0][0][i]
                    + "\t%.2e" % heat_data[0][1][i]
                    + "\t%.2e" % heat_data[0][2][i]
                    + "\t%.2e" % heat_data[0][3][i])

            if incl_heat:
                csv_lines += (csv_header + hr_au + ",total heat release," +
                              str(heat_data[0][0][i]) + ',' +
                              str(heat_data[0][1][i]) + ',' +
                              str(heat_data[0][2][i]) + ',' +
                              str(heat_data[0][3][i]) + '\n')

        tot_area = sum(area)

        if units in dd.perarea() and sum(area) > 0:

            tot_flam = sum(np.array(area) * np.array(cons_data[0][0]))
            tot_smld = sum(np.array(area) * np.array(cons_data[0][1]))
            tot_resd = sum(np.array(area) * np.array(cons_data[0][2]))
            tot_cons = sum(np.array(area) * np.array(cons_data[0][3]))
            pa_flam = tot_flam / tot_area
            pa_smld = tot_smld / tot_area
            pa_resd = tot_resd / tot_area
            pa_cons = tot_cons / tot_area

            pa_flam_hr = sum(np.array(heat_data[0][0]))
            pa_smld_hr = sum(np.array(heat_data[0][1]))
            pa_resd_hr = sum(np.array(heat_data[0][2]))
            pa_cons_hr = sum(np.array(heat_data[0][3]))

            txt += ("\n\nALL FUELBEDS:\n\nConsumption:\t%.2e" % pa_flam + "\t%.2e"
                % pa_smld + "\t%.2e" % pa_resd + "\t%.2e" % pa_cons)
            txt += ("\nHeat release:\t%.2e" % pa_flam_hr + "\t%.2e"
                % pa_smld_hr + "\t%.2e" % pa_resd_hr + "\t%.2e" % pa_cons_hr)

            csv_lines += ('ALL,ALL,' + str(tot_area) + ',ALL,ALL,ALL,ALL,' +
                  str_au + ',consumption,' +  str(pa_flam) + ',' + str(pa_smld) +
                          ',' + str(pa_resd) + ',' + str(pa_cons) + '\n')
            if incl_heat:
                csv_lines += ('ALL,ALL,' + str(tot_area) + ',ALL,ALL,ALL,ALL,' +
                 hr_au + ',heat release,' + str(pa_flam_hr) + ',' + str(pa_smld_hr)
                          + ',' + str(pa_resd_hr) + ',' + str(pa_cons_hr) + '\n')

        else:
            txt += ("\n\nALL FUELBEDS:\n\nConsumption:\t%.2e" %
                    sum(cons_data[0][0]) + "\t%.2e" % sum(cons_data[0][1])
                    + "\t%.2e" % sum(cons_data[0][2])
                    + "\t%.2e" % sum(cons_data[0][3]))
            txt += ("\nHeat release:\t%.2e" % sum(heat_data[0][0]) + "\t%.2e" %
                    sum(heat_data[0][1]) + "\t%.2e" %
                    sum(heat_data[0][2]) + "\t%.2e" %
                    sum(heat_data[0][3]))

            csv_lines += ('ALL,ALL,' + str(tot_area) +
                       ',ALL,ALL,ALL,ALL,consumption,' +
                       str(sum(cons_data[0][0])) + ',' + str(sum(cons_data[0][1]))
                       + ',' + str(sum(cons_data[0][2])) + ',' +
                       str(sum(cons_data[0][3])) + '\n')
            if incl_heat:
                csv_lines += ('ALL,ALL,' + str(tot_area)
                       + ',ALL,ALL,ALL,ALL,heat release,' +
                       str(sum(heat_data[0][0])) + ',' +
                       str(sum(heat_data[0][1])) + ',' + str(sum(heat_data[0][2]))
                       + ',' + str(sum(heat_data[0][3])))

        if csv != "":
            text = open(csv,'w')
            text.write(csv_lines)
            text.close()
        if not ret:
            print txt
        else: return txt

    def _calculate(self):
        """ Validates input parameters before executing Consume 3.0 equations

        Validates and modifies all input parameters and calls the function that
        runs all the Consume 3.0 consumption equations.

        """
        # reset calculated variables
        self._reset_outputs()

        if self._settings.settings_are_complete():
            self._consumption_calc()
            self._heat_release_calc()
            self._calc_success = True
            return True
        else:
            return False


    def _convert_units(self, explicit_units=None):
        """ Checks units and runs the unit conversion method for output data """
        # Convert to the desired output units
        self._conv_success = False

        if explicit_units:
            self._settings.units = str(explicit_units)

        if self._calc_success:
            if self._internal_units != self._settings.units:
                print("Converting units: {} -> {}".format(self._internal_units, self._settings.units))
                new_units = None
                [new_units, self._cons_data] = util.unit_conversion(
                                                    self._cons_data,
                                                    self._settings.get('area'),
                                                    self._internal_units,
                                                    self._settings.units)
                self._settings.units = new_units
                self._heat_release_calc()
                self._conv_success = True
            else:
                pass
                #print("Not converting units...")


    def _heat_release_calc(self):
        """ Calculates heat release from consumption data """

        btu_dict = {'tons' : 16000000.0,
                    'tonnes' : 18607977.8,
                    'kg' : 18607.9778,         ### - 8000 * 1.05505585 * 2.20462
                    'lbs' : 8000.0}
        key = self._settings.units.split('_')[0]
        assert key in btu_dict.keys()
        BTU_PER_UNIT = btu_dict[key]
        self._heat_data = (self._cons_data * BTU_PER_UNIT)

    '''
    This is an efficient way to get the specified fuelbeds. However, if the user has
    specified the same fuelbed number multiple times (likely with different equation
    sets) this returns just one copy of the data. Unfortunately, it is impossible to
    correctly broadcast this structure when doing calculations. Keep for explanatory
    value or reimplementation.
    def _get_loadings_for_specified_files(self, ids):
        # gets the specified fuelbeds from the dataframe. The return from nonzero is a
        #  tuple, hence the weird array reference
        selector_mask = [np.nonzero(self.FCCS.loadings_data_.fccs_id == i)[0][0] \
            for i in self.FCCS.loadings_data_.fccs_id if i in ids]
        return self.FCCS.loadings_data_.ix[selector_mask]
    '''

    def _get_loadings_for_specified_files(self, ids):
        ''' gets the specified fuelbeds from the dataframe.
        '''
        results = []
        for id in ids:
            try:
                tmp =  self.FCCS.loadings_data_[self.FCCS.loadings_data_.fccs_id==id].index[0]
                results.append(tmp)
            except:
                assert False, "Error: Invalid fuelbed specified"
        return self.FCCS.loadings_data_.iloc[results]

    def calc_ff_redux_proportion(self, LD):
        duff_depth = LD['duff_upper_depth'] + LD['duff_lower_depth']
        # total forest floor depth (inches)
        ff_depth = (duff_depth + LD['lit_depth'] + LD['lch_depth'] + LD['moss_depth'])

        # - this works correctly but still generates a warning, use the
        #   context manager to swallow the benign warning
        with np.errstate(divide='ignore', invalid='ignore'):
            nonzero_depth = np.not_equal(ff_depth, 0.0)
            # divide reduction by total ff depth to get proportion
            ff_redux_proportion = np.where(nonzero_depth, (LD['ff_reduction'] / ff_depth), 0.0)

        return ff_redux_proportion

    def _consumption_calc(self):
        """Calculates fuel consumption estimates.

        Input parameters must be set prior to running this method.

        Calculates fuel consumption for each of 36 sub-categories and 7 major
        categories of fuel types from the given inputs using the equations
        found in the Consume 3.0 User's Manual.

        Input parameters include fuel loadings (from FCCS data), ecoregion,
        and fuel moisture indicators (1000 hour fuel moisture, duff moisture,
        percent canopy consumed, and percent blackened shrub). See CONSUME 3.0
        manual for more information.

        Page numbers documented in the code correspond to the manual pages from
        which the equations were derived. Line numbers (ln ####) refer to
        corresponding lines in the original source code.


        """
        LD = self._get_loadings_for_specified_files(self._settings.get('fuelbeds'))

        # Setup ecoregion masks for equations that vary by ecoregion
        ecodict = {"maskb": {"boreal":1, "western":0, "southern":0},
                     "masks": {"boreal":0, "western":0, "southern":1},
                     "maskw": {"boreal":0, "western":1, "southern":0}}
        ecoregion = self._settings.get('ecoregion')
        ecob_mask = [ecodict["maskb"][e] for e in ecoregion]
        ecos_mask = [ecodict["masks"][e] for e in ecoregion]
        ecow_mask = [ecodict["maskw"][e] for e in ecoregion]
        ecoregion_masks = {'boreal':ecob_mask, 'southern':ecos_mask , 'western':ecow_mask}

           ########################################################
        ############ Fuel Consumption Calculation Execution ##########
           ########################################################

        [can_over_fsrt, can_mid_fsrt, can_under_fsrt, can_snag1f_fsrt,
         can_snag1w_fsrt, can_snag1nf_fsrt, can_snag2_fsrt, can_snag3_fsrt,
         can_ladder_fsrt] = ccn.ccon_canopy(self._settings.get('can_con_pct'), LD)

        [shb_prim_live_fsrt, shb_prim_dead_fsrt,
         shb_seco_live_fsrt, shb_seco_dead_fsrt] = ccn.ccon_shrub(self._settings.get('shrub_black_pct'), LD)

        [nw_prim_live_fsrt, nw_prim_dead_fsrt,
         nw_seco_live_fsrt, nw_seco_dead_fsrt] = ccn.ccon_nw(LD)

        [stump_snd_fsrt, stump_rot_fsrt, stump_ltr_fsrt] = ccn.ccon_stumps(LD)

        pile_fsrt = ccn.ccon_piles(self._settings.get('pile_black_pct'), LD)

        fm_1000hr = self._settings.get('fm_1000hr')
        fm_duff =  self._settings.get('fm_duff')
        if self._settings.burn_type in ['natural', ['natural']]:

            one_hr_fsrt = ccn.ccon_one_nat(LD)
            ten_hr_fsrt = ccn.ccon_ten_nat(LD)
            hun_hr_fsrt = ccn.ccon_hun_nat(ecos_mask, LD)
            oneK_hr_snd_fsrt = ccn.ccon_oneK_snd_nat(fm_duff, fm_1000hr, ecos_mask, LD)
            tenK_hr_snd_fsrt = ccn.ccon_tenK_snd_nat(fm_1000hr, LD)
            tnkp_hr_snd_fsrt = ccn.ccon_tnkp_snd_nat(fm_1000hr, LD)
            oneK_hr_rot_fsrt = ccn.ccon_oneK_rot_nat(fm_1000hr, ecos_mask, LD)
            tenK_hr_rot_fsrt = ccn.ccon_tenK_rot_nat(fm_1000hr, LD)
            tnkp_hr_rot_fsrt = ccn.ccon_tnkp_rot_nat(fm_1000hr, LD)
            [LD['ff_reduction'], y_b, duff_depth] = ccn.ccon_ffr(fm_duff, ecoregion_masks, LD)
            LD['ff_reduction_successive'] = LD['ff_reduction']
        else:
            fm_type = self._settings.fm_type
            windspeed =  self._settings.get('windspeed')
            slope =  self._settings.get('slope')
            area =  self._settings.get('area')
            days_since_rain =  self._settings.get('days_since_rain')
            fm_10hr =  self._settings.get('fm_10hr')
            length_of_ignition =  self._settings.get('length_of_ignition')

            [one_hr_fsrt, ten_hr_fsrt, hun_hr_fsrt,
            [oneK_hr_snd_fsrt, oneK_hr_rot_fsrt],
            [tenK_hr_snd_fsrt, tenK_hr_rot_fsrt],
            [tnkp_hr_snd_fsrt, tnkp_hr_rot_fsrt],
            LD['ff_reduction']] = cca.ccon_activity(fm_1000hr, fm_type,
                windspeed, slope, area, days_since_rain, fm_10hr, length_of_ignition, LD)
            LD['ff_reduction_successive'] = LD['ff_reduction']

        lch_fsrt = ccn.ccon_forest_floor(LD, 'lch_depth', 'lichen_loading', [0.95, 0.05, 0.00])
        moss_fsrt = ccn.ccon_forest_floor(LD, 'moss_depth', 'moss_loading', [0.95, 0.05, 0.00])
        lit_fsrt = ccn.ccon_forest_floor(LD, 'lit_depth', 'litter_loading', [0.90, 0.10, 0.00])
        duff_upper_fsrt = ccn.ccon_forest_floor(LD, 'duff_upper_depth', 'duff_upper_loading', [0.10, 0.70, 0.20])
        duff_lower_fsrt = ccn.ccon_forest_floor(LD, 'duff_lower_depth', 'duff_lower_loading', [0.00, 0.20, 0.80])

        ff_redux_proportion = self.calc_ff_redux_proportion(LD)
        bas_fsrt = ccn.ccon_bas(LD['bas_loading'], ff_redux_proportion)
        sqm_fsrt = ccn.ccon_sqm(LD['sqm_loading'], ff_redux_proportion)


        # Category summations
        can_fsrt = sum([can_over_fsrt, can_mid_fsrt, can_under_fsrt,
                        can_snag1f_fsrt, can_snag1w_fsrt, can_snag1nf_fsrt,
                        can_snag2_fsrt, can_snag3_fsrt, can_ladder_fsrt])
        shb_fsrt = sum([shb_prim_live_fsrt, shb_prim_dead_fsrt,
                        shb_seco_live_fsrt, shb_seco_dead_fsrt])
        nw_fsrt = sum([nw_prim_live_fsrt, nw_prim_dead_fsrt,
                       nw_seco_live_fsrt, nw_seco_dead_fsrt])
        llm_fsrt = sum([lch_fsrt, moss_fsrt, lit_fsrt])
        gf_fsrt = sum([duff_upper_fsrt, duff_lower_fsrt, bas_fsrt, sqm_fsrt])
        woody_fsrt = sum([pile_fsrt, stump_snd_fsrt, stump_rot_fsrt, stump_ltr_fsrt,
                    one_hr_fsrt, ten_hr_fsrt, hun_hr_fsrt, oneK_hr_snd_fsrt,
                    oneK_hr_rot_fsrt, tenK_hr_snd_fsrt, tenK_hr_rot_fsrt,
                    tnkp_hr_snd_fsrt, tnkp_hr_rot_fsrt])

        all_fsrt = sum([can_fsrt, shb_fsrt, nw_fsrt,
                        llm_fsrt, gf_fsrt, woody_fsrt])

        #######################
        #### OUTPUT EXPORT ####
        #######################

        self._ucons_data = np.array(
            [all_fsrt,
            can_fsrt,
            shb_fsrt,
            nw_fsrt,
            llm_fsrt,
            gf_fsrt,
            woody_fsrt,
            can_over_fsrt,
            can_mid_fsrt,
            can_under_fsrt,
            can_snag1f_fsrt,
            can_snag1w_fsrt,
            can_snag1nf_fsrt,
            can_snag2_fsrt,
            can_snag3_fsrt,
            can_ladder_fsrt,
            shb_prim_live_fsrt,
            shb_prim_dead_fsrt,
            shb_seco_live_fsrt,
            shb_seco_dead_fsrt,
            nw_prim_live_fsrt,
            nw_prim_dead_fsrt,
            nw_seco_live_fsrt,
            nw_seco_dead_fsrt,
            lit_fsrt,
            lch_fsrt,
            moss_fsrt,
            duff_upper_fsrt,
            duff_lower_fsrt,
            bas_fsrt,
            sqm_fsrt,
            pile_fsrt,
            stump_snd_fsrt,
            stump_rot_fsrt,
            stump_ltr_fsrt,
            one_hr_fsrt,
            ten_hr_fsrt,
            hun_hr_fsrt,
            oneK_hr_snd_fsrt,
            oneK_hr_rot_fsrt,
            tenK_hr_snd_fsrt,
            tenK_hr_rot_fsrt,
            tnkp_hr_snd_fsrt,
            tnkp_hr_rot_fsrt]
            )

        self._cons_debug_data = np.array([LD['ff_reduction']])

        # delete extraneous memory hogging variables
        del (all_fsrt, can_fsrt, shb_fsrt, nw_fsrt, llm_fsrt,
                gf_fsrt,woody_fsrt, can_over_fsrt, can_mid_fsrt, can_under_fsrt,
                can_snag1f_fsrt, can_snag1w_fsrt, can_snag1nf_fsrt,
                can_snag2_fsrt, can_snag3_fsrt, can_ladder_fsrt,
                shb_prim_live_fsrt, shb_prim_dead_fsrt, shb_seco_live_fsrt,
                shb_seco_dead_fsrt, nw_prim_live_fsrt, nw_prim_dead_fsrt,
                nw_seco_live_fsrt, nw_seco_dead_fsrt, lit_fsrt, lch_fsrt,
                moss_fsrt, duff_upper_fsrt, duff_lower_fsrt, bas_fsrt,
                sqm_fsrt, pile_fsrt, stump_snd_fsrt, stump_rot_fsrt, stump_ltr_fsrt,
                one_hr_fsrt, ten_hr_fsrt, hun_hr_fsrt, oneK_hr_snd_fsrt,
                oneK_hr_rot_fsrt, tenK_hr_snd_fsrt, tenK_hr_rot_fsrt,
                tnkp_hr_snd_fsrt, tnkp_hr_rot_fsrt)

        if self._unique_check:
            self._cons_data = _unpack(self._ucons_data, self._runlnk)
        else:
            self._cons_data = self._ucons_data

