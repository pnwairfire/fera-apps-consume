''' ---------------------------------------------------------------------------
Code in this file deals with input settings to consume
---------------------------------------------------------------------------- '''
import data_desc as dd
import numpy as np
import pandas as pan
import os

def validate_null(input_vals, permitted=None):
    return (True, input_vals, [])

def validate_range(input_vals, permitted_vals):
    ''' Check submitted values against permitted values and convert to
        numpy array
    '''
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
            print("\nError: can't convert sequence to numpy array")
    return (0 == len(invalid), valid, invalid)

def validate_list(input_vals, permitted_vals):
    ''' Is the input value part of the permitted list?
    '''
    valid = []
    invalid = []
    for val in input_vals:
        if val not in permitted_vals:
            invalid.append(val)
    if 0 == len(invalid):
        valid = input_vals
    return (0 == len(invalid), valid, invalid)

def is_sequence(maybe_seq):
    try:
        iter(maybe_seq)
        return True
    except:
        return False

class ConsumeInputSettings(object):
    '''
    TODO:  how should errors be displayed?

    Settings for a consume run.
    burn_type dictates how many settings are necessary
    There are no defaults.
    '''
    #keyword, name, internal name, permitted values, validator function
    ActivityInputVarParameters = {
        'slope' : ['Slope (%)',  [0,100], validate_range],
        'windspeed' : ['Mid-flame windspeed (mph)', [0, 35], validate_range],
        'days_since_rain' : ['Days since sgnf. rainfall', [0,365], validate_range],
        'fm_10hr' : ['Fuel moisture (10-hr, %)', [0,100], validate_range],
        'length_of_ignition' : ['Length of ignition (min.)', [0,10000], validate_range]}
    NaturalInputVarParameters = {
        'fuelbeds' : ['FCCS fuelbeds (ID#)', "", validate_null],
        'area' : ['Fuelbed area (acres)', [0,1000000], validate_range],
        'ecoregion' : ['Fuelbed ecoregion',  dd.list_valid_ecoregions(), validate_list],
        'fm_1000hr' : ['Fuel moisture (1000-hr, %)', [0,140], validate_range],
        'fm_duff' : ['Fuel moisture (duff, %)', [0,400], validate_range],
        'can_con_pct' : ['Canopy consumption (%)', [0,100], validate_range],
        'shrub_black_pct' : ['Shrub blackened (%)', [0,100], validate_range],
        }

    AllInputParameters = dict(NaturalInputVarParameters.items() + ActivityInputVarParameters.items())

    NaturalSNames = [s for s in NaturalInputVarParameters]
    ActivitySNames = [s for s in ActivityInputVarParameters]
    AllSNames = NaturalSNames + ActivitySNames

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
            print("Error: the only permitted values for burn_type are:")
            for i in dd.list_valid_burntypes():
                print("\t{}".format(i))

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
        if self._burn_type:
            if self._burn_type == 'activity':
                if value in dd.list_valid_fm_types():
                    self._fm_type = value
                else:
                    print("\nError: the only permitted values for fm_type are:")
                    for i in dd.list_valid_fm_types():
                        print("\t{}".format(i))
            else:
                print("\nError: fm_type is valid only when the burn_type is 'activity'.")
        else:
            print("\nError: burn_type must be set first as the valid parameter set depends on it.")

    def set(self, name, sequence):
        ''' All "tagged" settings get set here. burn_type must be specified prior to
            setting anything via this method because burn_type dictates what settings
            are valid.
        '''
        result = False
        if self._burn_type:
            #print("\nSetting {} ...".format(name))
            valid_names = list(ConsumeInputSettings.NaturalSNames) if 'natural' == self._burn_type else list(ConsumeInputSettings.AllSNames)
            if name in valid_names:
                validator = ConsumeInputSettings.AllInputParameters[name][2]
                permitted_values = ConsumeInputSettings.AllInputParameters[name][1]
                sequence = sequence if is_sequence(sequence) else [sequence]
                valid, valid_values, invalid_values = validator(sequence, permitted_values)
                if valid:
                    self._settings[name] = valid_values
                    result = True
                else:
                    print("Error: the following values are not permitted:")
                    print(invalid_values)
            else:
                print("\nError: '{}' is not a valid setting name".format(name))
                print("Valid names for the current burn_type ({}) are:".format(self._burn_type))
                for i in valid_names: print("\t{}".format(i))
        else:
            print("Error: burn_type must be specified before adding other settings")
        return result

    def get(self, name):
        ''' The getter for "tagged" settings
        '''
        if name in self._settings.keys():
            return self._settings[name]
        return None

    def settings_are_complete(self):
        ''' Have all the required settings been set?
        '''
        check_props = self._burn_type and self._units and (self._fm_type if 'activity' == self._burn_type else True)
        if check_props:
            valid_names = set(ConsumeInputSettings.NaturalSNames if 'natural' == self._burn_type else ConsumeInputSettings.AllSNames)
            current_settings = set(self._settings.keys())
            if valid_names == current_settings:
                self._settings['fuelbeds'] = self._settings['fuelbeds']
                return True
            else:
                assert(current_settings.issubset(valid_names))
                print("\nError settings problem ---> {}".format(valid_names.difference(current_settings)))
        else:
            def dbg_msg():
                needed = []
                if None == self._burn_type: needed.append('burn_type')
                if None == self._units: needed.append('units')
                if 'activity' == self._burn_type and None == self._fm_type: needed.append("fm_type")
                print("\n !!! Error settings problem, the following are required:")
                for i in needed:
                    print("\t{}".format(i))
            dbg_msg()
        return False

    def display_settings(self):
        ''' TODO: very basic settings display
        '''
        settings = []
        settings.append("burn_type\t{}".format(self._burn_type))
        settings.append("units\t{}".format(self._units))
        if 'activity' == self._burn_type:
            settings.append("fm_type\t{}".format(self._fm_type))
        for k, v in self._settings.iteritems():
            settings.append("{}\t{}".format(k, v))
        return "\n".join(settings)

    def package(self):
        if self.settings_are_complete():
            add_me = {}
            # - make these settings occur for each line. Allows iterating over results
            #   in a uniform way.
            add_me['burn_type'] = list([self._burn_type] * len(self._settings.get('fuelbeds')))
            add_me['units'] = list([self._units] * len(self._settings.get('fuelbeds')))
            if 'activity' == self.burn_type:
                add_me['fm_type'] = list([self.fm_type] * len(self._settings.get('fuelbeds')))
            return dict(self._settings.items() + add_me.items())

    def _get_valid_column_names_all(self, burn_type):
        ''' includes all valid names, even attribute names.
            used for reading from a file
        '''
        valid_names = self._get_valid_column_names_no_attributes(burn_type)
        if valid_names:
            valid_names.append('units')
            if 'activity' == burn_type: valid_names.append('fm_type')
        return valid_names

    def _get_valid_column_names_no_attributes(self, burn_type):
        ''' valid names, not including attribute names
        '''
        valid_names = None
        if burn_type == 'natural':
            valid_names = list(ConsumeInputSettings.NaturalSNames)
        elif burn_type == 'activity':
            valid_names = list(ConsumeInputSettings.AllSNames)
        return valid_names

    def _valid_file_columns(self, burn_type, supplied_columns):
        ''' Are the columns in the input file valid based on the burn_type?
        '''
        valid_names = self._get_valid_column_names_all(burn_type)
        if valid_names:
            s1 = set(valid_names)
            s2 = set(supplied_columns)
            if s1 == s2:
                return True
            else:
                print("\nError: invalid input file for this burn_type")
                if s2.issubset(s1):
                    print("The following columns are missing:")
                    for item in s1.difference(s2):
                        print("\t{}".format(item))
                else:
                    print("The following columns are not required:")
                    for item in s2.difference(s1):
                        print("\t{}".format(item))
        else:
            print("\nError: burn_burn_type must be 'natural' or 'activity'.")
            print(" ---- > {}".format(burn_type))
        return False

    def _column_content_identical(self, column):
        ''' results in a 1-element list if all the column elements are the same.
            column is a pandas Series / numpy array
        '''
        return 1 == len(column.unique())

    def load_from_file(self, filename):
        ''' Load settings from a csv file.
            burn_type MUST be set at this point
        '''
        result = False
        if self.burn_type:
            if os.path.exists(filename):
                contents = pan.read_csv(filename)
                if self._valid_file_columns(self.burn_type, contents.columns):
                    # - all of the values should be the same in the following 3 columns
                    unit_check = self._column_content_identical(contents.units)
                    fm_type_check = True
                    if 'activity' == self.burn_type:
                        fm_type_check = self._column_content_identical(contents.fm_type)
                        eco_check_must_be_western = self._column_content_identical(contents.ecoregion)
                        # - brute force, ensure ecoregion is western for activity burn_types
                        contents.ecoregion = 'western'

                    if unit_check and fm_type_check:
                        # - assign the single-input-value / property items
                        self.units = contents.units[0]
                        if 'activity' == self.burn_type: self.fm_type = contents.fm_type[0]

                        # - set the 'tagged' input items
                        valid_names = self._get_valid_column_names_no_attributes(self.burn_type)
                        for name in valid_names:
                            self.set(name, contents.get(name))
                        result = True
                    else:
                        print("\nError: burn_type, units, and fm_type columns must have identical values.")
                        print("Additionally, if the burn_type is 'activity', the ecoregion must be 'western'.")
            else:
                print("\nError: filename '{}' does not exist".format(filename))
        else:
            print("\nError: burn_type must be set prior to loading an input file")
        return result









