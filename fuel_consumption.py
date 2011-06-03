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
        >>> fc_obj.lengthOfIgnition = [Length#1, Length#2, ...]


        --Note: When setting input values, the user can also select a SINGLE
            value (instead of a list) for any environment variable that will
            apply to the entire scenario.
            These environment variables include the following:
            ecoregion, fuel_moisture_1000hr_pct,  fuel_moisture_duff_pct,
            canopy_consumption_pct, shrub_blackened_pct, slope, windpseed,
            fm_type, days_since_rain, lengthOfIgnition


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

        lengthOfIgnition
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
import input_variables as iv
import util_consume as util


class FuelConsumption:
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

        lengthOfIgnition
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

    def __init__(self, fccs_file = ""):
        """FuelConsumption class constructor

        Upon initialization of the FuelConsumption object, all input
        variables are declared and FCCS data is loaded as an FCCSDB object that
        is stored as self.FCCS(loading FCCS information may take a few seconds).

        User can optionally specify the directory location of the default xml
        FCCS database that is used to derive fuel loading information:

        Optional argument:

        fccs_file   : Location of the .xml file that contains all FCCS fuel
                      loading information. The default location is:
                      "[python-consume dir.]/input_data/FCCS_loadings.xml"

        """

        self.FCCS = fccs.FCCSDB(fccs_file)
        iv.InputVarParameters[0][3] = self._val_fccs = self.FCCS.valids
        self._fccs_canopy_consumption_pct = self.FCCS.fccs_canopy_consumption_pct
        self.reset_inputs_and_outputs()

    def reset_inputs_and_outputs(self):
        """Resets all the input parameters and all output data."""

        self._params = None
        self.fuelbed_fccs_ids = iv.InputVar('fuelbeds')
        self.fuelbed_area_acres = iv.InputVar('area')
        self.fuelbed_ecoregion = iv.InputVar('ecoregion')
        self.fuel_moisture_1000hr_pct = iv.InputVar('fm_1000hr')
        self.fuel_moisture_duff_pct = iv.InputVar('fm_duff')
        self.fuel_moisture_10hr_pct = iv.InputVar('fm_10hr')
        self.canopy_consumption_pct = iv.InputVar('can_con_pct')
        self.shrub_blackened_pct = iv.InputVar('shrub_black_pct')
        self.burn_type = iv.InputVar('burn_type')
        self.output_units = iv.InputVar('units')
        self.slope = iv.InputVar('slope')
        self.windspeed = iv.InputVar('windspeed')
        self.fm_type = iv.InputVar('fm_type')
        self.days_since_rain = iv.InputVar('days_since_rain')
        self.lengthOfIgnition = iv.InputVar('lengthOfIgnition')
        #self.display_inputs()

        self.customized_fuel_loadings = []
        self._fccs_loadings = []
        self.units = "tons_ac"
        self._build_input_set()
        self._cons_data = np.array([])
        self._cons_debug_data = np.array([])
        self._emis_data = np.array([])
        self._calc_success = False
        self._conv_success = False
        self._unique_check = False


    def load_example(self):
        """Load example scenario data.

        Loads an example 'natural' burn scenario (mostly for testing), setting
        input parameters (fuelbeds, area, ecoregion, 1000-hr fuel moisture,
        duff fuel moisture, percent canopy consumed, and percent blackened
        shrub).

        """

        self.burn_type = 'natural'
        self.fuelbed_fccs_ids.value = [27, 18]
        self.fuelbed_area_acres.value = [100.0, 100.0]
        self.fuelbed_ecoregion.value = 'western'
        self.fuel_moisture_1000hr_pct.value = 20.0
        self.fuel_moisture_duff_pct.value = 20.0
        self.canopy_consumption_pct.value = 20.0
        self.shrub_blackened_pct.value = 0.0

        self.display_inputs()

    def prompt_for_inputs(self):
        """Load scenario inputs from the user.

        Prompts user for the input parameters via the shell in somewhat
        user-friendly manner.

        """
        self.InSet.prompt_for_inputs()


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
            if self._conv_success:
                return util.make_dictionary_of_lists(cons_data = self._cons_data,
                                          cons_debug_data = self._cons_debug_data,
                                          heat_data = self._heat_data,
                                          emis_data = [],
                                          inputs = self.InSet.validated_inputs)

    def report(self, csv = "", stratum = "all", ret=False, tsize=8):
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
                    self._display_report(csv, stratum, incl_heat = False, ret=ret, tsize=tsize)
                else:
                    return self._display_report(csv, stratum, incl_heat = False, ret=ret, tsize=tsize)



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

        self.InSet.load(csv_in)
        self.report(csv = csv_out, stratum = stratum)
        print "\nFile saved to: " + csv_out


    def display_inputs(self):
        """Lists the input parameters for the consumption scenario.

        Displays the input parameters for the consumption in the shell. Useful
        as a quick way to check that the scenario parameters have been
        correctly set.

        """
        self._build_input_set()
        self.InSet.display_input_values()


    def list_variable_names(self):
        """Lists variable names of each of the input parameters for reference"""
        self.InSet.display_variable_names()


    def save_scenario(self, save_file=''):
        """Saves the scenario input parameters to a CSV file

        Required argument:

        save_file  : directory location of the CSV file to which the scenario
                     will be saved

        """
        self.InSet.save(save_file)


    def load_scenario(self, load_file=''):
        """Loads scenario input parameters from a CSV file

        Required argument:

        load_file  : directory location of the CSV file from which the scenario
                     will be loaded. See 'consume_batch_input_example.csv' for
                     formatting guidance.

        """
        self.InSet.load(load_file)

    def _display_report(self, csv, stratum = 'all', incl_heat = False, ret=False, tsize=8):
        """Displays an in-shell report on consumption values"""

        categories = ["canopy\t", "shrub\t", "nonwoody", "llm  \t",
                      "ground fuels", "woody fuels"]

        units = self.InSet.validated_inputs['units']
        fccs_ids = self.InSet.validated_inputs['fuelbeds']
        area = self.InSet.validated_inputs['area']
        ecoregion = self.InSet.validated_inputs['ecoregion']
        fm_1000hr = self.InSet.validated_inputs['fm_1000hr']
        fm_duff = self.InSet.validated_inputs['fm_duff']
        fm_can = self.InSet.validated_inputs['can_con_pct']
        fm_shb = self.InSet.validated_inputs['shrub_black_pct']
        hr_au = "btu"
        str_au = units

        cons_data = self._cons_data
        heat_data = self._heat_data

        if units in perarea() and sum(area) > 0:
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

        if units in perarea() and sum(area) > 0:

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

        self._csvlines = csv_lines
        if csv != "":
            text = open(csv,'w')
            text.write(csv_lines)
            text.close()
        if not ret:
            print txt
        else: return txt


    def _wfeis_return(self, fuelbed_fccs_ids = [1],
                          fuelbed_area_km2 = [0],
                          fuelbed_ecoregion = 'western',
                          fuel_moisture_1000hr_pct = 50,
                          fuel_moisture_duff_pct = 50,
                          canopy_consumption_pct = 50,
                          shrub_blackened_pct = 50,
                          customized_fuel_loadings = [],
                          output_units = 'kg',
                          combustion_stage = 'all',
                          stratum = 'all',
                          verbose = False):

        """Directly returns consumption values for given inputs

        This is a customized function designed for work with MTRI's Wildland
        Fire Emissions Information System (WFEIS, wfeis.mtri.org).

        Arguments:

        fuelbed_fccs_ids
                : a list of FCCS fuelbed ID numbers

        fuelbed_area_km2
                : a list (or single number to be used for all fuelbeds) of
                  numbers in square km that correspond w/ the appropriate FCCS
                  fuelbed ID listed in the 'fuelbeds' variable.

        fuelbed_ecoregion
                : a list (or single region to be used for all fuelbeds) of
                  ecoregions ('western', 'southern', or 'boreal') that
                  correspond w/ the appropriate FCCS fuelbed ID listed in the
                  'fuelbeds' variable.

        fuel_moisture_1000hr_pct
                : 1000-hr fuel moisture in the form of a number or list of
                  numbers ranging from 0-140 representing a percentage.

        fuel_moisture_duff_pct
                : Duff fuel moisture. A number or list of numbers ranging from
                  0-400 representing a percentage.

        canopy_consumption_pct
                : Percent canopy consumed. A number or list of numbers ranging
                  from 0-100 representing a percentage. -1 for auto-calc.

        shrub_blackened_pct
                : Percent of shrub that has been blackened. A number or list
                  of numbers ranging from 0-100 representing a percentage.

        customized_fuel_loadings
                : A list of 3 value lists in this format:
                  [fuelbed index number {interger},
                   fuel stratum {string},
                   loading value {number}]
                  To view all valid stratum names and units, use the
                  FuelConsumption.FCCS.list_fuel_loading_names() method.

        output_units
                : 'lbs', 'lbs_ac', 'tons', 'tons_ac', 'kg', 'kg_m^2', 'kg_ha',
                  'tonnes', 'tonnes_ha', 'tonnes_km^2'

        combustion_stage
                : 'flaming', 'residual', 'smoldering', or 'total'

        stratum
                : 'total', 'canopy', 'shrub', 'ground fuels', 'nonwoody',
                  'litter-lichen-moss', or 'woody fuels'


        """

        self.fuelbed_fccs_ids.value = fuelbed_fccs_ids
        self.fuelbed_area_acres.value = [a * 247.105381 for a in fuelbed_area_km2]
        self.fuelbed_ecoregion.value = fuelbed_ecoregion
        self.fuel_moisture_1000hr_pct.value = fuel_moisture_1000hr_pct
        self.fuel_moisture_duff_pct.value = fuel_moisture_duff_pct
        self.canopy_consumption_pct.value = canopy_consumption_pct
        self.shrub_blackened_pct.value = shrub_blackened_pct
        self.output_units.value = output_units
        self.customized_fuel_loadings = customized_fuel_loadings

        baseDict = self.results()
        baseDat = baseDict['consumption']['summary']

        if stratum == 'all':
            out = baseDat

        elif combustion_stage == 'all':
            out = baseDat[stratum]

        else:
            if type(combustion_stage) is list:
                csdict = {'T' : 'total', 'F' : 'flaming',
                          'R' : 'residual', 'S' : 'smoldering',
                          'total' : 'total', 'flaming' : 'flaming',
                          'residual' : 'residual', 'smoldering' : 'smoldering'}
                out = []
                for s, stage in enumerate(combustion_stage):
                    if stage == 'R':
                        tmp = (baseDat[stratum]['residual'][s] +
                               baseDat[stratum]['smoldering'][s])
                        out.append(tmp)
                    else:
                        out.append(baseDat[stratum][csdict[stage]][s])

            else:
                out = baseDat[stratum][combustion_stage]

        self.reset_inputs_and_outputs()

        if verbose: return out, baseDict
        else: return out


    def _build_input_set(self):
        """Builds the InputVarSet object from the individual input parameters"""

        if self._params == None:
            params = {'fuelbeds': self.fuelbed_fccs_ids,
                      'area': self.fuelbed_area_acres,
                      'ecoregion': self.fuelbed_ecoregion,
                      'fm_1000hr': self.fuel_moisture_1000hr_pct,
                      'fm_10hr': self.fuel_moisture_10hr_pct,
                      'fm_duff': self.fuel_moisture_duff_pct,
                      'can_con_pct': self.canopy_consumption_pct,
                      'shrub_black_pct': self.shrub_blackened_pct,
                      'burn_type': self.burn_type,
                      'units': self.output_units,
                      'slope': self.slope,
                      'windspeed': self.windspeed,
                      'fm_type': self.fm_type,
                      'days_since_rain': self.days_since_rain,
                      'lengthOfIgnition': self.lengthOfIgnition}

        else: params = self._params

        for p in params:
            if type(params[p]) in (int, str, list, float, np.array, tuple):
                tmp = iv.InputVar(p)
                tmp.value = params[p]
                params[p] = tmp

        self.InSet = iv.InputVarSet(params)
        self.fuelbed_fccs_ids = params['fuelbeds']
        self.fuelbed_area_acres = params['area']
        self.fuelbed_ecoregion = params['ecoregion']
        self.fuel_moisture_1000hr_pct = params['fm_1000hr']
        self.fuel_moisture_10hr_pct = params['fm_10hr']
        self.fuel_moisture_duff_pct = params['fm_duff']
        self.canopy_consumption_pct = params['can_con_pct']
        self.shrub_blackened_pct = params['shrub_black_pct']
        self.burn_type = params['burn_type']
        self.output_units = params['units']
        self.slope = params['slope']
        self.windspeed = params['windspeed']
        self.fm_type = params['fm_type']
        self.days_since_rain = params['days_since_rain']
        self.lengthOfIgnition = params['lengthOfIgnition']


    def _calculate(self):
        """ Validates input parameters before executing Consume 3.0 equations

        Validates and modifies all input parameters and calls the function that
        runs all the Consume 3.0 consumption equations.

        """

        def validate_customized_fuel_loadings():
            """ Validate customized fuel loading inputs """
            cfl_format_check = True
            cfl_index_check = True
            cfl_name_check = True
            cfl_value_check = True
            cfl_name_bads = []
            cfl_value_bads = []

            cfl = self.customized_fuel_loadings
            if len(cfl) != 0:
                if type(cfl[0]) is not list and len(cfl) == 3:
                    self.customized_fuel_loadings = [cfl]

            for cfl in self.customized_fuel_loadings:
                if type(cfl) is list and len(cfl) == 3:
                    if cfl[0] < 0 or cfl[0] > self.InSet.set_length:
                        cfl_index_check = False

                    if cfl[1] not in zip(*dd.LoadDefs)[1]:
                        cfl_name_check = False
                        cfl_name_bads.append(cfl[1])

                    try:
                        t = float(cfl[2])
                        if t < 0:
                            cfl_value_check = False
                            cfl_value_bads.append(cfl[2])
                    except:
                        cfl_value_check = False
                        cfl_value_bads.append(cfl[2])
                else:
                    cfl_format_check = False

            if not cfl_index_check:
                print ("ERROR: invalid customized fuel loading input:\n" +
                       "Fuelbed index must be between 1 and " + str(p))
                return False

            elif not cfl_name_check:
                print ("ERROR: invalid customized fuel loading input:\n" +
                       "The following strata name(s) are invalid: ")
                print cfl_name_bads
                print ("To view a list of valid strata names, use the" +
                       ".FCCS.list_fuel_loading_names() method.")
                return False

            elif not cfl_value_check:
                print ("ERROR: invalid customized fuel loading input:\n" +
                       "The following value(s) is either less than zero or " +
                       "cannot be converted to a number:")
                print cfl_value_bads
                return False

            elif not cfl_format_check:
                print ("ERROR: invalid customized fuel loading input:\n" +
                       "The .customized_fuel_loadings variable must be formatted as"
                      + " a list of 3 value lists, e.g.:\n[[1, 'overstory',4.5]," +
                        " [1, 'shrub_prim', 3.0],...]")
                return False
            else:
                return True

        # reset calculated variables
        self._calc_success = False
        self._unq_inputs = []
        self._runlnk = []
        self._build_input_set()

        if self.InSet.validate() and validate_customized_fuel_loadings():
            # Build canopy consumption input if auto-calc (-1) is selected
            can = self.InSet.validated_inputs['can_con_pct']
            if len(can) == 1 and -1 in can:
                cans = []
                for f in self.InSet.validated_inputs['fuelbeds']:
                    cans.append(float(self._fccs_canopy_consumption_pct[int(f)]))
                self.InSet.validated_inputs['can_con_pct'] = np.array(cans)

            else:
                for j, jval in enumerate(can):
                    if jval == -1:
                        self.InSet.validated_inputs['can_con_pct'][j] = (
                                float(self._fccs_canopy_consumption_pct[int(
                                self.InSet.validated_inputs['fuelbeds'][j])]))

            self.canopy_consumption_pct.value = self.InSet.validated_inputs['can_con_pct']

            self.units = 'tons_ac'
            [self._unq_inputs, self._runlnk] = self.InSet.getuniques(self._unique_check)
            self._consumption_calc(**self._unq_inputs)
            self._calc_success = True


    def _convert_units(self):
        """ Checks units and runs the unit conversion method for output data """
        # Convert to the desired output units
        self._conv_sucess = False

        if type(self.output_units) in (int, str, list, float, np.array, tuple):
            tmp = iv.InputVar('units')
            tmp.value = self.output_units
            self.output_units = self.InSet.params['units'] = tmp

        if self._calc_success and self.output_units.validate():
            [self.units, self._cons_data] = util.unit_conversion(
                                                self._cons_data,
                                                self.fuelbed_area_acres.value,
                                                self.units,
                                                self.output_units.value[0])

            self.InSet.params['units'].value = self.units
            self.InSet.validated_inputs['units'] = self.units
            self._heat_release_calc()
            self._conv_success = True


    def _heat_release_calc(self):
        """ Calculates heat release from consumption data """

        # conversion factors- according to source code (2000 btu/lb.)
        btu_dict = {'tons' : 4000000.0,
                    'tonnes' : 4409245.24,
                    'kg' : 4409.24524,
                    'lbs' : 2000.0}

        BTU_PER_UNIT = btu_dict[self.units.split('_')[0]]

        self._heat_data = (self._cons_data * BTU_PER_UNIT)



    def _consumption_calc(self, fuelbeds, ecoregion = 'western', fm_1000hr=50.0,
                          fm_duff=50.0, burn_type = 'natural', can_con_pct=50.0,
                          shrub_black_pct = 50.0, fm_10hr = 50.0,
                          slope = 30.0, windspeed = 20.0, fm_type = "MEAS-Th",
                          days_since_rain = 2, lengthOfIgnition = 1, area=1,
                          units = ""):

        """Calculates fuel consumption estimates.

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

        Arguments:

        burn_type
                : Use this variable to select ['natural'] burn equations or
                  ['activity'] (i.e. prescribed) burn equations. Note that
                  'activity' burns require 6 additional input parameters:
                  10hr fuel moisture, slope, windpseed, fuel moisture type,
                  days since significant rainfall, and length of ignition.

        fuelbeds
                : a list of Fuel Characteristic Classification System (FCCS)
                  (http://www.fs.fed.us/pnw/fera/fccs/index.shtml) fuelbed ID
                  numbers (1-900).

        area
                : a nparray (or single number to be used for all fuelbeds) of
                  numbers in acres that represents area for the corresponding
                  FCCS fuelbed ID listed in the 'fuelbeds_fccs_ids' variable.

        ecoregion
                : a list (or single region to be used for all fuelbeds) of
                  ecoregions ('western', 'southern', or 'boreal') that
                  represent the ecoregion for the corresponding FCCS fuelbed ID
                  listed in the 'fuelbeds_fccs_ids' variable. Regions within the
                  US that correspond to each broad regional description can be
                  found in the official Consume 3.0 User's Guide, p. 60. Further
                  info on Bailey's ecoregions can be found here:
                www.eoearth.org/article/Ecoregions_of_the_United_States_(Bailey)
                  Default is 'western'

        fm_1000hr
                : 1000-hr fuel moisture in the form of a number or nparray of
                  numbers ranging from 0-100 representing a percentage.
                  Default is 50%

        fm_10hr
                : <specific to 'activity' burns>
                  10-hr fuel moisture in the form of a number or nparray of
                  numbers ranging from 0-100 representing a percentage.
                  Default is 50%

        fm_duff
                : Duff fuel moisture. A number or nparray of numbers ranging from
                  0-100 representing a percentage.
                  Default is 50%.

        can_con_pct
                : Percent canopy consumed. A number or nparray of numbers ranging
                  from 0-100 representing a percentage. Set to '-1' to
                  use an FCCS-fuelbed dependent precalculated canopy consumption
                  percentage based on crown fire initiation potential, crown to
                  crown transmissivity, and crown fire spreading potential.
                  (note: auto-calc is not available for FCCS ID's 401-456)
                  Default is -1

        shrub_black_pct
                : Percent of shrub that has been blackened. A number or nparray
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

        lengthOfIgnition
                : <specific to 'activity' burns>
                  The amount of time (minutes) it will take to ignite the area
                  to be burned. Used to determine if a fire will be of high
                  intensity, which affects diameter reduction of large woody
                  fuels in 'activity' fuelbeds.

        """
        #a = np.array
        if type(fm_type) == list:
            fm_type = fm_type[0]

        def _get_fuel_loadings(fuelbeds):
            """ Retrieves FCCS loadings values based on scenario FCCS IDs """
            def _setup_loading_dictionary():
                """ Sets up the FCCS fuel loadings dictionary """
                LD = {} # fuel loading dictionary
                for t in zip(*dd.LoadDefs)[1]: # lists internal tags
                    LD[t] = []
                return LD

            LD = _setup_loading_dictionary()
            # skip loading these b/c will just hog memory
            skips = ['ecoregion', 'cover_type', 'site_desc']

            # load all fuel loadings for all corresponding fccs id's
            loadings = []
            for f in fuelbeds:
                for bed in self.FCCS.data:
                    if str(f) == str(bed[0]):
                        loadings.append(bed)

            data = zip(*loadings)
            for lds in dd.LoadDefs:
                if lds[1] not in skips:
                    LD[lds[1]] = data[lds[2]]

            # convert to numpy arrays
            for t in zip(*dd.LoadDefs)[1]:
                if t != 'fccs_id':
                    LD[t] = np.array(LD[t])

            if len(self.customized_fuel_loadings) != 0:
                for flc in self.customized_fuel_loadings:
                    f_index = flc[0] - 1
                    ld_name = flc[1]
                    ld_value = float(flc[2])
                    LD[ld_name][f_index] = ld_value

            self._fccs_loadings = LD

            return LD

        LD = _get_fuel_loadings(fuelbeds)
        # Setup ecoregion masks for equations that vary by ecoregion
        ecodict = {"maskb": {"boreal":1, "western":0, "southern":0},
                     "masks": {"boreal":0, "western":0, "southern":1},
                     "maskw": {"boreal":0, "western":1, "southern":0}}

        ecob_mask = [ecodict["maskb"][e] for e in ecoregion]
        ecos_mask = [ecodict["masks"][e] for e in ecoregion]
        ecow_mask = [ecodict["maskw"][e] for e in ecoregion]

        zeroes = np.array([0.0] * len(LD['fccs_id']), dtype=float)

        # Repeated functions
        def csdist(tot, csd):
            """Portions consumption by consumption stage"""
            return np.array([tot * csd[0], tot * csd[1], tot * csd[2], tot * sum(csd)])

        def propcons(x):
            """ Equation to calculate proportion consumed for various strata"""
            return math.e ** (x) / (1 + math.e ** x)

        # Consumption calculation methods
        def ccon_canopy ():
            """ Canopy consumption, activity & natural, p.166
            Proportions for snag1nf are not specified in the manual; right now,
            the class 1 wood values are in place, which seem to correspond to
            the GUI <<< """

            pct = can_con_pct / 100.0
            can_params = [['overstory', [0.75, 0.05, 0.0]],
                          ['midstory', [0.80, 0.05, 0.0]],
                          ['understory', [0.85, 0.05, 0.0]],
                          ['snag1f', [0.75, 0.04, 0.01]],
                          ['snag1w', [0.03, 0.01, 0.01]],
                          ['snag1nf', [0.03, 0.01, 0.01]],
                          ['snag2', [0.05, 0.1, 0.1]],
                          ['snag3', [0.10, 0.20, 0.20]],
                          ['ladder', [0.75, 0.10, 0.0]]]

            return [csdist(LD[t[0]] * pct, t[1]) for t in can_params]


        def ccon_shrub():
            """ Shrub consumption, activity & natural, p.168

            ## The manual specifies the following equation to calculate percent
            ## black:
            ##      y = -1.6693 + (0.1185 * nw_pctcv) - (0.2453 * fm_10hr)
            ##                  + (0.1697 * WindxSlopeCategory)
            ##  shrub_black_pct = 100 * math.e**(y) / (1 + math.e**(y))
            ##
            ## However, there is no explanation on how to derive
            ## 'WindxSlopeCategory' """
            csd_live = [0.95, 0.05, 0.0]
            csd_dead = [0.90, 0.10, 0.0]

            shb_load_total = LD['shrub_prim'] + LD['shrub_seco']
            if sum(shb_load_total) > 0:

                z = -2.6573 + (0.0956 * shb_load_total) + (0.0473 * shrub_black_pct)

                shb_cnsm_total = shb_load_total * propcons(z)
                divzero = np.not_equal(shb_load_total, 0.0)

                shb_prim_total = np.where(divzero,
                      shb_cnsm_total * (LD['shrub_prim'] / shb_load_total), 0.0)
                shb_seco_total = np.where(divzero,
                      shb_cnsm_total * (LD['shrub_seco'] / shb_load_total), 0.0)

                pctlivep = LD['shrub_prim_pctlv']
                pctdeadp = 1 - pctlivep
                pctlives = LD['shrub_seco_pctlv']
                pctdeads = 1 - pctlives

                return (csdist(shb_prim_total * pctlivep, csd_live),
                        csdist(shb_prim_total * pctdeadp, csd_dead),
                        csdist(shb_seco_total * pctlives, csd_live),
                        csdist(shb_seco_total * pctdeads, csd_dead))
            else:
                hold = csdist(zeroes, [0.0, 0.0, 0.0])
                return hold, hold, hold, hold


        def ccon_nw():
            """ Nonwoody consumption, activity & natural, p.169 """

            nw_prim_total = LD['nw_prim'] * 0.9274
            nw_seco_total = LD['nw_seco'] * 0.9274

            csd_live = [0.95, 0.05, 0.0]
            csd_dead = [0.95, 0.05, 0.0]

            pctlivep = LD['nw_prim_pctlv']
            pctdeadp = 1 - pctlivep
            pctlives = LD['nw_seco_pctlv']
            pctdeads = 1 - pctlives

            return (csdist(nw_prim_total * pctlivep, csd_live),
                    csdist(nw_prim_total * pctdeadp, csd_dead),
                    csdist(nw_seco_total * pctlives, csd_live),
                    csdist(nw_seco_total * pctdeads, csd_dead))


        ###################################################################
        ### LITTER LICHEN MOSS (LLM) CONSUMPTION - ACTIVITY and NATURAL ###
        ###################################################################
        # p. 175 in the manual

        def ccon_ffr():
            """ Forest-floor reduction calculation, p.177  """

            # total duff depth (inches)
            duff_depth = LD['duff_upper_depth'] + LD['duff_lower_depth']
            # total forest floor depth (inches)
            ff_depth = (duff_depth + LD['lit_depth'] +
                        LD['lch_depth'] + LD['moss_depth'])

                # boreal
            y_b = 1.2383 - (0.0114 * fm_duff) # used to calc squirrel mid. redux
            ffr_boreal = ff_depth * propcons(y_b)

                # southern
            ffr_southern = (-0.0061 * fm_duff) + (0.6179 * ff_depth)
            ffr_southern = np.where(
                        np.less_equal(ffr_southern, 0.25), # if ffr south <= .25
                        (0.006181 * math.e**(0.398983 * (ff_depth - # true
                        (0.00987 * (fm_duff-60.0))))),
                        ffr_southern)                               # false

                # western
            y = -0.8085 - (0.0213 * fm_duff) + (1.0625 * ff_depth)
            ffr_western = ff_depth * propcons(y)

            return [((ecos_mask * ffr_southern) +
                     (ecob_mask * ffr_boreal) +
                     (ecow_mask * ffr_western)), y_b, duff_depth]

        def ccon_lch():
            """ Lichen consumption, activity & natural"""
            csd_lch = [0.95, 0.05, 0.00]
            lch_pretot = np.minimum(LD['lch_depth'], LD['ff_reduction_successive'])
            LD['ff_reduction_successive'] = LD['ff_reduction_successive'] - lch_pretot
            if 'activity' in burn_type:
                lch_pretot = np.where(ecob_mask, lch_pretot, LD['lch_depth'])

            lch_total = (lch_pretot * 0.5 * LD['lch_pctcv'])

            return csdist(lch_total, csd_lch)

        def ccon_moss():
            """ Moss consumption, activity & natural"""
            csd_moss = [0.95, 0.05, 0.00]
            moss_pretot = np.minimum(LD['moss_depth'], LD['ff_reduction_successive'])
            LD['ff_reduction_successive'] = LD['ff_reduction_successive'] - moss_pretot
            if 'activity' in burn_type:
                moss_pretot = np.where(ecob_mask, moss_pretot, LD['moss_depth'])

            moss_total = (moss_pretot * 1.5 * LD['moss_pctcv'])
            return csdist(moss_total, csd_moss)

        def ccon_litter():
            """ Litter consumption, activity & natural"""
            csd_lit = [0.90, 0.10, 0.00]
            lit_pretot = np.minimum(LD['lit_depth'], LD['ff_reduction_successive'])
            LD['ff_reduction_successive'] = LD['ff_reduction_successive'] - lit_pretot
            if 'activity' in burn_type:
                lit_pretot = np.where(ecob_mask, lit_pretot, LD['lit_depth'])
            mean_weighted_litterbd = ((LD['lit_s_ndl_pct'] * 3.0)
                                + (LD['lit_l_ndl_pct'] * 3.0)
                                + (LD['lit_o_ndl_pct'] * 3.0)
                                + (LD['lit_blf_d_pct'] * 1.5)
                                + (LD['lit_blf_e_pct'] * 1.5)
                                + (LD['lit_palm_pct'] * 0.3)
                                + (LD['lit_grass_pct'] * 0.5))
            LD['lit_mean_bd'] = mean_weighted_litterbd
            lit_total = (lit_pretot * LD['lit_pctcv'] * mean_weighted_litterbd)
            return csdist(lit_total, csd_lit)


        ################################
        ### Ground FUELS CONSUMPTION ###
        ################################
        # p. 179-183 in the manual

        def ccon_bas():
            """ Basal accumulations consumption, activity & natural

             The following equations in the next 4 lines of code for basal
             accumulation consumption are NOT in the manual, but were derived
             from the source code and in consultation with Susan Prichard(USFS)
             an original developer of Consume 3.0.
            """
            csd_bas = [0.10, 0.40, 0.50]
            # '43560' refers to the conversion factor from square feet to acres.
            # '0.8333' refers to default tree radius (in ft, based on 20" diam)
            bas_density = LD['bas_pct'] / 2.0 #<<< should pct be div by 100?
            bas_area = np.maximum((
                        ((math.pi * (LD['bas_rad'] ** 2.0) / 43560.0) -
                        (math.pi * 0.8333 / 43560.0)) * bas_density), 0.0)
            bas_total = (np.minimum(LD['bas_depth'], LD['ff_reduction'])
                         * bas_area * 12.0)

            return csdist(bas_total, csd_bas)


        def ccon_sqm():
            """ Squirrel middens consumption, activity & natural
            # These squirrel midden consumption equations are not included in
            # the 3.0 manual; they were derived from the source code.
            # Squirrel midden reduction is zero unless in a boreal
            # ecoregion.
            # Note: the source code uses squirrel midden 'height' instead
            #   of 'depth'...not sure if they are interchangeable. The FCCS
            #   xml file appears to only list 'depth' data, hence our usage
            #   here """
            csd_sqm = [0.10, 0.30, 0.60]
            sqm_reduction = LD['sqm_depth'] * propcons(y_b) * ecob_mask
            sqm_area = (LD['sqm_density'] * math.pi *
                        (LD['sqm_radius']**2.0) / 43560.0)
            sqm_total = sqm_reduction * sqm_area * 12.0

            return csdist(sqm_total, csd_sqm)


        def ccon_duff(duff_reduction):
            """ Duff consumption, activity & natural*
                * note that there are different equations for activity/natural
                  to calculate duff_reduction
            #   Refer to p. 181-184 in the 3.0 manual
            #   General equation:
            Consumption(tons/ac.) = Reduction(in.) * Bulk density(tons/acre-in.)
            """
            csd_duffu = [0.10, 0.70, 0.20]
            csd_duffl = [0.0, 0.20, 0.80]

            # duff upper
            redux_up = np.where(     # select where: depth <= reduction
                       np.less_equal(LD['duff_upper_depth'], duff_reduction),
                       LD['duff_upper_depth'],              # if true
                       duff_reduction)                      # if false

            # duff lower
            redux_lo = np.where(     # select where: depth >= reduction
                       np.greater_equal(LD['duff_upper_depth'], duff_reduction),
                       zeroes,                                  # true
                       duff_reduction - LD['duff_upper_depth']) # false

            # upper
            duff_upper = np.maximum(redux_up * 8.0 * LD['duff_upper_pctcv'], 0.0)

            # lower
            lo_total = redux_lo * LD['duff_lower_pctcv']
            bulk_dens = (np.where(np.equal(LD['duff_lower_deriv'], 3), 18.0, 0.0) +
                         np.where(np.equal(LD['duff_lower_deriv'], 4), 22.0, 0.0))
            duff_lower = np.maximum(lo_total * bulk_dens, 0.0)

            return (csdist(duff_upper, csd_duffu),
                    csdist(duff_lower, csd_duffl))


        ##############################
        ### WOODY FUEL CONSUMPTION ###
        ##############################
        # p. 169-175 in the manual

        def ccon_stumps():
            """ STUMP CONSUMPTION - ACTIVITY and NATURAL """
            stump_params = [['stump_sound', 0.10, [0.50, 0.50, 0.0]],
                            ['stump_rotten', 0.50, [0.10, 0.30, 0.60]],
                            ['stump_lightered', 0.50, [0.40, 0.30, 0.30]]]

            return [csdist(LD[s[0]] * s[1], s[2]) for s in stump_params]

        ### WOODY FUEL CONSUMPTION NATURAL EQUATIONS ###
        def ccon_one_nat():
            """ 1-hr (0 to 1/4"), natural """
            csd = [0.95, 0.05, 0.00]
            return csdist(LD['one_hr_sound'], csd)

        def ccon_ten_nat():
            """ 10-hr (1/4" to 1"), natural, p.169"""
            csd = [0.90, 0.10, 0.00]
            total = LD['ten_hr_sound'] * 0.8650
            return csdist(total, csd)

        def ccon_hun_nat():
            """ 100-hr (1 to 3"), natural """
            csd = [0.85, 0.10, 0.05]
            total = np.where(
                    np.equal(ecos_mask, 1),       # if southern ecoregion,
                    LD['hun_hr_sound'] * 0.4022,    # true
                    LD['hun_hr_sound'] * 0.7844)    # false
            return csdist(total, csd)

        def ccon_oneK_snd_nat():
            """ 1000-hr (3 to 9") sound, natural """
            csd = [0.60, 0.30, 0.10]
            y = 0.0302 - (0.0379 * fm_duff)
            z = 3.1052 - (0.0559 * fm_1000hr)
            total = np.where(
                   np.equal(ecos_mask, 1),      # if southern ecoregion,
                   LD['oneK_hr_sound'] * propcons(y),   # true
                   LD['oneK_hr_sound'] * propcons(z))   # false
            return csdist(total, csd)

        def ccon_tenK_snd_nat():
            """ 10K-hr (9 to 20") sound, natural """
            csd = [0.40, 0.40, 0.20]
            x = 0.7869 - (0.0387 * fm_1000hr)
            total = LD['tenK_hr_sound'] * propcons(x)
            return csdist(total, csd)

        def ccon_tnkp_snd_nat():
            """ 10K+ hr (>20") sound, natural """
            csd = [0.20, 0.40, 0.40]
            z = 0.3960 - (0.0389 * fm_1000hr)
            total = LD['tnkp_hr_sound'] * propcons(z)
            return csdist(total, csd)

        def ccon_oneK_rot_nat():
            """ 1000-hr (3 to 9") rotten, natural """
            csd = [0.20, 0.30, 0.50]
            y = 4.0139 - (0.0600 * fm_duff) + (0.8341 * LD['oneK_hr_rotten'])
            z = 0.5052 - (0.0434 * fm_duff)
            total = np.where(np.equal(ecos_mask, 1),    # if southern ecoegion,
                    LD['oneK_hr_rotten'] * propcons(z),     # true
                    LD['oneK_hr_rotten'] * propcons(y))     # false
            return csdist(total, csd)

        def ccon_tenK_rot_nat():
            """ 10K-hr (9 to 20") rotten, natural """
            csd = [0.10, 0.30, 0.60]
            y = 2.1218 - (0.0438 * fm_duff)
            total = LD['tenK_hr_rotten'] * propcons(y)
            return csdist(total, csd)

        def ccon_tnkp_rot_nat():
            """ 10K+ hr (>20") rotten, natural """
            csd = [0.10, 0.30, 0.60]
            y = 0.8022 - (0.0266 * fm_duff)
            total = LD['tnkp_hr_rotten'] * propcons(y)
            return csdist(total, csd)


        def duff_redux_natural():
            """ Duff reduction calculation, natural """

            # total depth of litter, lichen, and moss layer, used in duff calc.
            llm_depth = LD['lit_depth'] + LD['lch_depth'] + LD['moss_depth']

            #Duff reduction equation (natural fuels):

            #if llm_depth[n] >= duff_reduction:   #<<<EQUATIONS DOCUMENTATION
            #if llm_depth[n] > duff_depth[n]:    #<<< USER'S GUIDE - SUSAN PRICHARD SAYS THIS IS THE CORRECT COMPARISON
            #if llm_depth[n] >= ff_reduction[n]:  #<<< SOURCE CODE

            # KS - if the duff_reduction value is greater than zero use it,
            # otherwise, use zero.
            duff_reduction_tmp = (LD['ff_reduction'] - llm_depth)
            non_zero = duff_reduction_tmp > 0.0
            return (duff_reduction_tmp * non_zero)

        ### WOODY FUEL CONSUMPTION ACTIVITY EQUATIONS ###
        def ccon_activity():
            """ Woody fuel activity equations, p. 142 """
            def pct_hun_hr_calc():
                """ Calculate % of 100-hour fuels consumed, p. 142, ln 4541 """

                # Eq. A: Default 100-hr load
                hun_hr_def = 4.8

                # Eq. B: Heat flux correction, ln 4557
                heat_flux_crx = ((LD['hun_hr_sound'] / hun_hr_def) *
                                       (1.0 + ((slope - 20.0)/60.0) +
                                       (windspeed / 4.0)))

                #"(%) 3.0% (amount of change in moisture content for each
                # doubling of flux [Rothermel 1972])
                fm_flux = 3.0

                # Eq. C: 10-hr fuel moisture correction
                fm_10hr_correction = np.where(
                          np.equal(heat_flux_crx, 0.0),
                          0.0,
                          fm_flux * (np.log(heat_flux_crx) / math.log(2.0)))

                # Eq. D: Adjusted 10-hr fuel moisture content, p. 143, ln 4563
                adj_fm_10hr = fm_10hr - fm_10hr_correction

                # Eq. E: Percentage consumption of 100-hr fuels, ln 4564
                return np.clip(np.where(
                        np.less(adj_fm_10hr, 26.7),   # if adj10hrFM < 26.7,
                        0.9 - (adj_fm_10hr - 12.0) * 0.0535,       # true
                        (-169.08 - (adj_fm_10hr * 18.393) -  # false
                        (((adj_fm_10hr)**2) * 0.6646) +
                        (((adj_fm_10hr)**3) * 0.00798)) *
                        np.less_equal(adj_fm_10hr, 29.3)), # mask out > 29.3%
                        0.0,1.0) # clip range to 0-1

            def diam_redux_calc():
                """ Calculation of diameter reduction for woody fuels activity
                    equations """
                def final1000hr():
                    """Eq. G: Evaluating if curing has occurred, p.146-7
                    ln 5009 -> according to source code, this analysis is not
                    included- a relic of Consume 2.1. """
                   #uncured_FM = 119.64 * (math.e ** (-0.0069 * snow_free_days))
                   # 'DRED_FM'='diameter reduction fuel moisture'
                   #DRED_FM = np.where(np.greater(uncured_FM, fm_1000hr),
                   #         uncured_FM,
                   #         fm_1000hr)

                #return np.where(np.greater(DRED_FM, 60.0), uncured_FM, DRED_FM)

                    return fm_1000hr * cdic['adj'][fm_type]

                def spring_summer_adjustment():
                    """ p. 148, ln 5063
                     note: NFDRS #'s div by 1.4 in source code, NOT in doc.
                     Eq. H: Evaluating spring-like burning conditions occurred
                     Eq. I: Spring-like diameter reduction equation
                     Eq. J: Summer-like diameter reduction equation
                    """

                    def calc_mb(x):
                        """ create m & b masks  """
                        sprg = cdic['spring'][fm_type][x]
                        sumr = cdic['summer'][fm_type][x]
                        # note: transitional equation NOT in documentation-
                        # retrieved from source code
                        return ((mask_spring * sprg) +
                         (mask_summer * sumr) +
                         (mask_trans * ((spring_ff + sprg) * (sumr - sprg))))

                    # make masks
                    mask_spring = np.less_equal(pct_hun_hr, 0.75)
                    mask_trans = np.logical_and(np.greater(pct_hun_hr, 0.75),
                                                np.less(pct_hun_hr, 0.85))
                    mask_summer = np.greater_equal(pct_hun_hr, 0.85)
                    spring_ff = (pct_hun_hr - 0.75) / 0.1

                    m = calc_mb(0)
                    b = calc_mb(1)

                    diam_reduction = (adjfm_1000hr * m) + b # ln 5129

                    # ln 5130: not in doc, to keep DRED from reaching 0:
                    diam_reduction = np.where(np.less(diam_reduction, 0.5),
                       (adjfm_1000hr / cdic['adj'][fm_type] * (-0.005)) + 0.731,
                        diam_reduction)


                    # Eq. K: High fuel moisture diameter reduction p.149 ln 4594
                    diam_reduction = np.where(np.logical_and(
                                     np.greater(adjfm_1000hr, 44.0),
                                     np.less(adjfm_1000hr, 60.0)),
                                     (-0.0178 * adjfm_1000hr) + 1.499,
                                     diam_reduction)

                    return np.where(np.greater(adjfm_1000hr, 60.0),
                                     (-0.005 * adjfm_1000hr) + 0.731,
                                     diam_reduction)


                def ignitionConst_calc():
                    """ Calculate Ignition Constant ln 5146
                    Maximum Ignition Duration (minutes): "The total number of
                    minutes that can elapse in the ignition period and still be
                    considered a mass ignition"
                    """

                    igd1 = np.where(np.less(area, 20.0),
                                    area, 0.5 * area + 10.0)
                    igd2 = np.where(                    # if length <= maxidndur
                          np.less_equal(lengthOfIgnition, igd1),
                            igd1,
                            np.where(np.less(area, 20.0),
                             2.0 * area,
                             20.0 + area))

                    igd3 = np.where(np.less_equal(lengthOfIgnition, igd2),
                            igd2,
                            np.where(np.less(area, 20.0),
                             4.0 * area,
                             40.0 + (4.0 * area)))
                    igd4 = np.where(np.less_equal(lengthOfIgnition, igd3),
                            igd3,
                            np.where(np.less(area, 20.0),
                             8.0 * area,
                             80.0 + (4.0 * area)))

                    # ignition coefficient
                    igc = np.where(np.less_equal(lengthOfIgnition, igd1),
                           np.where(np.less(area, 10.0),
                                      4.0 - (10.0 - area) / 100.0, 4.0),
                           np.where(np.less_equal(lengthOfIgnition, igd2),
                            3.0 + ((igd2 - lengthOfIgnition) / (igd2 - igd1)),
                            np.where(np.less_equal(lengthOfIgnition, igd3),
                             2.0 + ((igd3 - lengthOfIgnition) / (igd3 - igd2)),
                             np.where(np.less_equal(lengthOfIgnition, igd4),
                             1.0 + ((igd4 - lengthOfIgnition) / (igd4 - igd3)),
                             1.0))))

                    # adjust for 10 hour fuel moisture ln 5239
                    # if > 18, igc = 1.0, if b/t 15-18, that equation
                    igc = np.where(np.greater(fm_10hr, 15.0),
                           np.where(np.greater(fm_10hr, 18.0),
                            igc - (igc - 1.0) * ((fm_10hr - 15.0) / 3.0),
                            1.0),
                            igc)

                    # adjust for 1000hr fuel moisture ln5255
                    turnpt = (igc * -3.333) + 53.333
                    igc = np.where(np.greater(fm_1000hr, turnpt),
                           (fm_1000hr * (-3.0 / 20.0)) + 8.0 + (0.5 * igc), igc)

                    igc = np.where(np.less(igc, 1.0), 1.0, igc)

                    return igc

                def high_intensity_adjustment(diam_reduction):
                    """ Eq. L: p.150, ln 4607-4609 """
                    reduxFactor = (1.0 - (0.11 * (ignitionConst_calc() - 1.0)))
                    return diam_reduction * reduxFactor

                # Execute calculations for diam reduction
                adjfm_1000hr = final1000hr()
                diam_reduction = spring_summer_adjustment()
                diam_reduction = high_intensity_adjustment(diam_reduction)

                return diam_reduction, adjfm_1000hr


            def duff_redux_activity():
                """Duff reduction calculation, activity
                   p160 ln 4765"""

                # Eq. R: Y-intercept adjustment ln 4766-4770
                YADJ = np.minimum((diam_reduction / 1.68), 1.0)

                # Eq. S: Drying period equations - This equation requires
                # "days since significant rainfall" data: the # of days since
                # at least 0.25 inches fell...
                days_to_moist = 21.0 * ((duff_depth / 3.0)**1.18) # ln 4772
                days_to_dry = 57.0 * ((duff_depth / 3.0)**1.18) # ln 4773

                # Eq. T, U, V: Wet, moist, & dry duff redxu equation ln 4774
                wet_df_redux = ((0.537 * YADJ) + (0.057 *
                       (oneK_fsrt[0][3] + tenK_fsrt[0][3] + tnkp_fsrt[0][3])))

                moist_df_redux = (0.323 * YADJ) + (1.034 *
                                                  (diam_reduction ** 0.5))

                # p161 ln 4784
                adj_wet_duff_redux = (wet_df_redux +
                                     (moist_df_redux - wet_df_redux) *
                                     (days_since_rain / days_to_moist))


                # adjusted wet duff, to smooth the transition ln 4781
                dry_df_redux = (moist_df_redux +
                               ((days_since_rain - days_to_dry) / 27.0))

                # these conditionals illustrated on p.161 ln 4782-4800
                duff_reduction = np.where(
                               np.less(days_since_rain,days_to_moist),
                               adj_wet_duff_redux,
                                 np.where(
                                 np.greater_equal(days_since_rain, days_to_dry),
                                 np.maximum(dry_df_redux, wet_df_redux),
                                 np.maximum(moist_df_redux, wet_df_redux)))

                # Eq. W: Shallow duff adjustment p. 162, ln 4802-4811
                duff_reduction2 = np.where(
                                 np.less_equal(duff_depth, 0.5),
                                 duff_reduction * 0.5,
                                 duff_reduction * ((0.25 * duff_depth) + 0.375))

                duff_reduction = np.where(
                                 np.greater(duff_depth, 2.5),
                                 duff_reduction,
                                 duff_reduction2)

                # not in manual- but in source code, and common sense ln 4812-15
                duff_reduction = np.minimum(duff_reduction, duff_depth)

                return duff_reduction


            def qmd_redux_calc(q):
                """ Eq. N p. 152 ln 4611, 4616 Quadratic mean diameter reduction
                For 1000hr and 10khr fuels.
                p. 152 "Quadratic mean diameter is used to convert calculated
                inches of diameter reduction into % volume reduction."

                QMD, inches: "represents the diameter of a log in a woody size
                               class with average volume" """
                return (1.0 - ((q - diam_reduction) / q)**2.0)

            def flaming_DRED_calc(hun_hr_total):
                """ p. 155, ln 4655
                Flaming diameter reduction (inches)
                (%) this is a fixed value, from Ottmar 1983 """
                # stuck an 'abs' in there b/c of nan problems
                flaming_portion = (1.0 - math.e**-(abs((((20.0 - hun_hr_total)
                                   / 20.0) - 1.0) / 0.2313)**2.260))
                return diam_reduction * flaming_portion, flaming_portion

            def flamg_portion(q, tlc, tld, fDRED):
                """ ln 4683, 4693, 4702
                    Calculates flaming portion of large woody fuels and
                    ensures that flaming portion is not greater than total"""
                def check(t, tot):
                    """ Check that flaming consumption does not exceed total """
                    f = tld[t] * pct
                    return np.where(np.greater(f, tot), tot, f)

                pct = (1.0 - (((q - fDRED)**2.0) / (q**2.0)))
                return np.array([check(t, tl) for t, tl in enumerate(tlc)])

            def csdist_act(f, tots, rF):
                """ Distribute woody activity consumption by combustion stage
                    f = flaming consumption
                    tots = total consumption [snd, rot]
                    rF = residual fractions [snd, rot]"""
                #print f, tots, rF
                #aprint f.shape, tots.shape, rF.shape
                dist = [f,                            # flaming
                       (tots - f) * (1.0 - rF),       # smoldering
                       (tots - f) * rF,               # residual
                       tots]

                return np.array(list(zip(*dist)))

            def ccon_one_act():
                """ 1-hr (0 to 1/4") woody fuels consumption, activity """
                csd = [1.0, 0.0, 0.0]
                return csdist(LD['one_hr_sound'], csd)

            def ccon_ten_act():
                """ 10-hr (1/4" to 1") woody fuels consumption, activity
                    ln 4537 """
                csd = [1.0, 0.0, 0.0]
                total = LD['ten_hr_sound']
                return csdist(total, csd)

            def ccon_hun_act():
                """ Eq. F: Total 100-hr (1" - 3") fuel consumption, activity
                    p.144 ln 4585"""
                resFrac = np.array([0.0])
                QMD_100hr = 1.68
                total = LD['hun_hr_sound'] * pct_hun_hr
                [flamgDRED, flaming_portion] = flaming_DRED_calc(total)

                # Flaming consumption for 100-hr fuels... ln 4657
                flamg = np.where(np.greater_equal(flamgDRED, QMD_100hr),
                        total,
                        flamg_portion(QMDs[0], [total],
                                      [LD['hun_hr_sound']], flamgDRED)[0]) # <<< confirm that this is correct- ln 4663

                # make sure flaming doesn't exceed total... ln 4665
                flamg = np.where(np.greater(flamg, total), total, flamg)
                return np.array([zip(*csdist_act(flamg, total, resFrac))]), flamgDRED, flaming_portion

            def ccon_oneK_act():
                """ 1000-hr (3" - 9") woody fuels consumption, activity
                    Eq. O, ln 4610-4613 """
                resFrac = np.array([[0.25], [0.63]]) # [snd, rot] non-flaming resid pct
                totld = np.array([LD['oneK_hr_sound'], LD['oneK_hr_rotten']])
                oneK_redux = qmd_redux_calc(QMDs[1])
                total_snd = oneK_redux * totld[0]
                total_rot = oneK_redux * totld[1]
                flamg = flamg_portion(QMDs[1], [total_snd, total_rot], totld, flamgDRED)
                return csdist_act(flamg, np.array([total_snd, total_rot]), resFrac)

            def ccon_tenK_act():
                """ 10K-hr (9 to 20") woody fuels consumption, activity
                    Eq. O, ln 4615-4618 """
                resFrac = np.array([[0.33], [0.67]]) # [snd, rot] non-flaming resid pct
                totld = np.array([LD['tenK_hr_sound'], LD['tenK_hr_rotten']])
                tenK_redux = qmd_redux_calc(QMDs[2])
                total_snd = tenK_redux * totld[0]
                total_rot = tenK_redux * totld[1]
                flamg = flamg_portion(QMDs[2], [total_snd, total_rot], totld, flamgDRED)
                return csdist_act(flamg, np.array([total_snd, total_rot]), resFrac)

            def ccon_tnkp_act():
                """ >10,000-hr (20"+) woody fuel consumption, activity
                 p. 153 Table P, ln 4619
                 Documentation does not include the condition that where
                 1000hr FM < 31%, redux is always 5%"""
                resFrac = np.array([[0.5], [0.67]]) # [snd, rot] non-flaming resid pct
                pct_redux = (np.less(adjfm_1000hr, 35.0) *  # mask out above 35%
                       (np.where(np.less(adjfm_1000hr, 31.0),# where < 31%
                          0.05,                                   # true
                         (35.0 - adjfm_1000hr) / 100.0)))       # false - Table P.

                total_snd = pct_redux * LD['tnkp_hr_sound']
                total_rot = pct_redux * LD['tnkp_hr_rotten']
                # <<< DISCREPANCY b/t SOURCE and DOCUMENTATION here
                # corresponds to source code right now for testing-sake
                flamgsnd = LD['tnkp_hr_sound'] * flaming_portion
                flamgrot = LD['tnkp_hr_rotten'] * flaming_portion
                flamgsnd = np.where(np.greater(flamgsnd, total_snd),
                                    total_snd, flamgsnd)
                flamgrot = np.where(np.greater(flamgrot, total_rot),
                                    total_rot, flamgrot)
                return csdist_act(np.array([flamgsnd, flamgrot]), np.array([total_snd, total_rot]), resFrac)


            # Variables that need to be defined for these equations
            #snow_free_days = 30 # need for curing eval, if still valid

            # "global"s

            # quadratic mean diameters: [hun, oneK, tenK, tnkp]
            QMDs = [1.68, 5.22, 12.10, 25.00]
            cdic = {
              'spring' : {"MEAS-Th" : [-0.097, 4.747],  # spring-like
                    "ADJ-Th" : [-0.096, 4.6495],
                    "NFDRS-Th" : [-0.120 / 1.4, 4.305]},
              'summer' : {"MEAS-Th" : [-0.108, 5.68],   # summer-like
                    "ADJ-Th" : [-0.1251, 6.27],
                    "NFDRS-Th" : [-0.150 / 1.4, 5.58]},
              'adj' : {"MEAS-Th" : 1.0,            # for the <0.5 adj
                    "ADJ-Th" : 1.0,
                    "NFDRS-Th" : 1.4}}

            # execute calculations
            pct_hun_hr = pct_hun_hr_calc()
            [diam_reduction, adjfm_1000hr] = diam_redux_calc()
            [[hun_hr_fsrt], flamgDRED, flaming_portion] = ccon_hun_act()
            one_fsrt = ccon_one_act()
            ten_fsrt = ccon_ten_act()
            oneK_fsrt = ccon_oneK_act()
            tenK_fsrt = ccon_tenK_act()
            tnkp_fsrt = ccon_tnkp_act()

            # <<< below included to jive with source code- not in manual, tho
            woody = (oneK_fsrt[0][3] + oneK_fsrt[1][3] +
                     tenK_fsrt[0][3] + tenK_fsrt[1][3] +
                     tnkp_fsrt[0][3] + tnkp_fsrt[1][3])
            diam_reduction = np.where(np.equal(woody, 0.0), 0.0, diam_reduction)

            return (one_fsrt, ten_fsrt, hun_hr_fsrt,
                    oneK_fsrt, tenK_fsrt, tnkp_fsrt,
                   ccon_duff(duff_redux_activity()))


           ########################################################
        ############ Fuel Consumption Calculation Execution ##########
           ########################################################

        [can_over_fsrt, can_mid_fsrt, can_under_fsrt, can_snag1f_fsrt,
         can_snag1w_fsrt, can_snag1nf_fsrt, can_snag2_fsrt, can_snag3_fsrt,
         can_ladder_fsrt] = ccon_canopy()

        [shb_prim_live_fsrt, shb_prim_dead_fsrt,
         shb_seco_live_fsrt, shb_seco_dead_fsrt] = ccon_shrub()

        [nw_prim_live_fsrt, nw_prim_dead_fsrt,
         nw_seco_live_fsrt, nw_seco_dead_fsrt] = ccon_nw()

        [LD['ff_reduction'], y_b, duff_depth] = ccon_ffr()

        LD['ff_reduction_successive'] = LD['ff_reduction']
        lch_fsrt = ccon_lch()
        moss_fsrt = ccon_moss()
        lit_fsrt = ccon_litter()

        bas_fsrt = ccon_bas()
        sqm_fsrt = ccon_sqm()

        [stump_snd_fsrt, stump_rot_fsrt, stump_ltr_fsrt] = ccon_stumps()

        if burn_type in ['natural', ['natural']]:
            one_hr_fsrt = ccon_one_nat()
            ten_hr_fsrt = ccon_ten_nat()
            hun_hr_fsrt = ccon_hun_nat()
            oneK_hr_snd_fsrt = ccon_oneK_snd_nat()
            tenK_hr_snd_fsrt = ccon_tenK_snd_nat()
            tnkp_hr_snd_fsrt = ccon_tnkp_snd_nat()
            oneK_hr_rot_fsrt = ccon_oneK_rot_nat()
            tenK_hr_rot_fsrt = ccon_tenK_rot_nat()
            tnkp_hr_rot_fsrt = ccon_tnkp_rot_nat()
            [duff_upper_fsrt, duff_lower_fsrt] = ccon_duff(duff_redux_natural())

        else:
            [one_hr_fsrt, ten_hr_fsrt, hun_hr_fsrt,
            [oneK_hr_snd_fsrt, oneK_hr_rot_fsrt],
            [tenK_hr_snd_fsrt, tenK_hr_rot_fsrt],
            [tnkp_hr_snd_fsrt, tnkp_hr_rot_fsrt],
            [duff_upper_fsrt, duff_lower_fsrt]] = ccon_activity()

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
        woody_fsrt = sum([stump_snd_fsrt, stump_rot_fsrt, stump_ltr_fsrt,
                    one_hr_fsrt, ten_hr_fsrt, hun_hr_fsrt, oneK_hr_snd_fsrt,
                    oneK_hr_rot_fsrt, tenK_hr_snd_fsrt, tenK_hr_rot_fsrt,
                    tnkp_hr_snd_fsrt, tnkp_hr_rot_fsrt])

        all_fsrt = sum([can_fsrt, shb_fsrt, nw_fsrt,
                        llm_fsrt, gf_fsrt, woody_fsrt])

        #######################
        #### OUTPUT EXPORT ####
        #######################

        self._ucons_data = np.array([all_fsrt, can_fsrt, shb_fsrt, nw_fsrt, llm_fsrt,
                gf_fsrt,woody_fsrt, can_over_fsrt, can_mid_fsrt, can_under_fsrt,
                can_snag1f_fsrt, can_snag1w_fsrt, can_snag1nf_fsrt,
                can_snag2_fsrt, can_snag3_fsrt, can_ladder_fsrt,
                shb_prim_live_fsrt, shb_prim_dead_fsrt, shb_seco_live_fsrt,
                shb_seco_dead_fsrt, nw_prim_live_fsrt, nw_prim_dead_fsrt,
                nw_seco_live_fsrt, nw_seco_dead_fsrt, lit_fsrt, lch_fsrt,
                moss_fsrt, duff_upper_fsrt, duff_lower_fsrt, bas_fsrt,
                sqm_fsrt, stump_snd_fsrt, stump_rot_fsrt, stump_ltr_fsrt,
                one_hr_fsrt, ten_hr_fsrt, hun_hr_fsrt, oneK_hr_snd_fsrt,
                oneK_hr_rot_fsrt, tenK_hr_snd_fsrt, tenK_hr_rot_fsrt,
                tnkp_hr_snd_fsrt, tnkp_hr_rot_fsrt])

        self._cons_debug_data = np.array([LD['lit_mean_bd'], LD['ff_reduction']])

        # delete extraneous memory hogging variables
        del (all_fsrt, can_fsrt, shb_fsrt, nw_fsrt, llm_fsrt,
                gf_fsrt,woody_fsrt, can_over_fsrt, can_mid_fsrt, can_under_fsrt,
                can_snag1f_fsrt, can_snag1w_fsrt, can_snag1nf_fsrt,
                can_snag2_fsrt, can_snag3_fsrt, can_ladder_fsrt,
                shb_prim_live_fsrt, shb_prim_dead_fsrt, shb_seco_live_fsrt,
                shb_seco_dead_fsrt, nw_prim_live_fsrt, nw_prim_dead_fsrt,
                nw_seco_live_fsrt, nw_seco_dead_fsrt, lit_fsrt, lch_fsrt,
                moss_fsrt, duff_upper_fsrt, duff_lower_fsrt, bas_fsrt,
                sqm_fsrt, stump_snd_fsrt, stump_rot_fsrt, stump_ltr_fsrt,
                one_hr_fsrt, ten_hr_fsrt, hun_hr_fsrt, oneK_hr_snd_fsrt,
                oneK_hr_rot_fsrt, tenK_hr_snd_fsrt, tenK_hr_rot_fsrt,
                tnkp_hr_snd_fsrt, tnkp_hr_rot_fsrt)

        if self._unique_check:
            self._cons_data = _unpack(self._ucons_data, self._runlnk)
        else:
            self._cons_data = self._ucons_data
