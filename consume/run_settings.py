import data_desc as dd
import numpy as np
import util_consume as util

def validate_range(input_vals, permitted_vals):
    valid = []
    invalid = []
    for val in input_vals:
        if val < permitted_vals[0] or val > permitted_vals[1]:
            invalid.append(val)
    if 0 == len(invalid):
        try:
            valid = np.array(input_vals, dtype=float)
        except:
            invalid.append(0.0)
            print("Error: can't convert sequence to numpy array")
    return (0 == len(invalid), valid, invalid)

def validate_list(input_vals, permitted_vals):
    invalid = []
    for val in input_vals:
        if val not in permitted_vals:
            invalid.append(val)
    return (0 == len(invalid), invalid)

class RunSettings(object):
    #keyword, name, intname, validvals, validator
    ActivityInputVarParameters = {
        'slope' : ['Slope (%)', '.slope_pct', [0,100], validate_range],
        'windspeed' : ['Mid-flame windspeed (mph)', '.windspeed', [0, 35], validate_range],
        'fm_type' : ['1000hr fuel moisture type', '.fm_type', dd.list_valid_fm_types(), validate_list],
        'days_since_rain' : ['Days since sgnf. rainfall', '.days_since_rain', [0,365], validate_range],
        'fm_10hr' : ['Fuel moisture (10-hr, %)', '.fuel_moisture_10hr_pct', [0,100], validate_range],
        'length_of_ignition' : ['Length of ignition (min.)', '.length_of_ignition', [0,10000], validate_range]}
    NaturalInputVarParameters = {
        'fuelbeds' : ['FCCS fuelbeds (ID#)', [1,10000], validate_range],
        'area' : ['Fuelbed area (acres)', [0,1000000], validate_range],
        'ecoregion' : ['Fuelbed ecoregion',  dd.list_valid_ecoregions(), validate_list],
        'fm_1000hr' : ['Fuel moisture (1000-hr, %)', [0,140], validate_range],
        'fm_duff' : ['Fuel moisture (duff, %)', [0,400], validate_range],
        'can_con_pct' : ['Canopy consumption (%)', [0,100], validate_range],
        'shrub_black_pct' : ['Shrub blackened (%)', [0,100], validate_range],
        'efg' : ['Emissions factor group(s)', [0,20], validate_range]}

    AllInputParameters = dict(NaturalInputVarParameters.items() + ActivityInputVarParameters.items())

    NaturalSNames = [s for s in NaturalInputVarParameters]
    ActivitySNames = [s for s in ActivityInputVarParameters]

    def __init__(self):
        ### - these are single value settings
        self._units = None
        self._fm_type = None
        self._burn_type = None

        ### - dictionary of multi-value settings, empty on initialization
        self._settings = {}

    @property
    def burn_type(self): return self._burn_type
    @burn_type.setter
    def burn_type(self, value):
        tmp = value.lower()
        if tmp in dd.list_valid_burntypes():
            self._burn_type = tmp
        else:
            print("Error: the only permitted values for burn_type are: 'natural' and 'activity'.")

    @property
    def units(self): return self._units
    @units.setter
    def units(self, value):
        tmp = value.lower()
        if tmp in dd.list_valid_units():
            self._units = tmp
        else:
            print("Error: the only permitted values for units are:")
            for i in dd.list_valid_units():
                print("\t{}".format(i))

    @property
    def fm_type(self): return self._fm_type
    @fm_type.setter
    def fm_type(self, value):
        if value in dd.list_valid_fm_types():
            self._fm_type = value
        else:
            print("Error: the only permitted values for units are:")
            for i in dd.list_valid_fm_types():
                print("\t{}".format(i))
        
    def add(self, name, sequence):
        result = False
        if self._burn_type:
            valid_names = RunSettings.NaturalSNames if 'natural' == self._burn_type else RunSettings.NaturalSNames + ActivitySNames 
            if name in valid_names:
                validator = RunSettings.AllInputParameters[name][2]
                permitted_values = RunSettings.AllInputParameters[name][1]
                valid, valid_values, invalid_values = validator(sequence, permitted_values)
                if valid:
                    self._settings[name] = valid_values
                    result = True
                else:
                    print("Error: the following values are not permitted:")
                    print(invalid_values)
            else:
                print("\nError: '{}' is not a valid setting name".format(name))
                print("Valid names for the current burn_type ({}) are".format(self._burn_type))
                for i in valid_names: print("\t{}".format(i))
        else:
            print("Error: burn_type must be specified before adding other settings")
        return result

    def get(self, name):
        if name in self._settings.keys():
            return self._settings[name]
        else:
            print("Error: '{}' is not a current setting".format(name))

