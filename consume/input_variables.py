import data_desc as dd
import numpy as np
import util_consume as util

NaturalInputVarParameters =[
#keyword, name, intname, validvals, defvalue, array, spec to activity equations
    ['fuelbeds', 'FCCS fuelbeds (ID#)', '.fuelbed_fccs_ids', [], '1', False, False],
    ['area', 'Fuelbed area (acres)', '.fuelbed_area_acres', [0,1000000], 1.0, True, False],
    ['ecoregion', 'Fuelbed ecoregion', '.fuelbed_ecoregion', dd.list_valid_ecoregions(), 'western', False, False],
    ['fm_1000hr', 'Fuel moisture (1000-hr, %)', '.fuel_moisture_1000hr_pct', [0,140], 50.0, True, False],
    ['fm_duff', 'Fuel moisture (duff, %)', '.fuel_moisture_duff_pct', [0,400], 50.0, True, False],
    ['can_con_pct', 'Canopy consumption (%)', '.canopy_consumption_pct', [0,100], 0, True, False],
    ['shrub_black_pct', 'Shrub blackened (%)', '.shrub_blackened_pct', [0,100], 50.0, True, False],
    ['burn_type', 'Burn type', '.burn_type', dd.list_valid_burntypes(), 'natural', False, False],
    ['units', 'Output units', '.output_units', dd.list_valid_units(), 'tons_ac', False, False],
    ['efg', 'Emissions factor group(s)', '.emissions_factor_group', [0,20], 0, False, False]
]

ActivityInputVarParameters =[
#keyword, name, intname, validvals, defvalue, array, spec to activity equations
    ['slope', 'Slope (%)', '.slope_pct', [0,100], 5.0, True, True],
    ['windspeed', 'Mid-flame windspeed (mph)', '.windspeed', [0, 35], 5.0, True, True],
    ['fm_type', '1000hr fuel moisture type', '.fm_type', dd.list_valid_fm_types(), 'MEAS-Th', False, True],
    ['days_since_rain', 'Days since sgnf. rainfall', '.days_since_rain', [0,365], 20, True, True],
    ['fm_10hr', 'Fuel moisture (10-hr, %)', '.fuel_moisture_10hr_pct', [0,100], 50.0, True, True],
    ['lengthOfIgnition', 'Length of ignition (min.)', '.lengthOfIgnition', [0,10000], 30.0, True, True]
]

InputVarParameters = NaturalInputVarParameters + ActivityInputVarParameters

class InputVar:
    """ A class the stores and validates input parameter data used in the
        FuelConsumption and Emissions objects"""
    def __init__(self, keyword = ""):
        """ InputVar class constructor.

            Upon initialization, loads attributes from the InputVarParameters
            internal data table according to the specified keyword ('kw')."""

        for ivp in InputVarParameters:
            if ivp[0] == keyword:
                self.keyword = ivp[0]
                self.name = ivp[1]
                self.intname = ivp[2]
                self.valids = ivp[3]
                self.value = ivp[4]
                self.default = ivp[4]
                self.array = ivp[5]
                self.activity = ivp[6]

        self.invalids = []

    def __repr__(self):
        return str(self.value)

    def validate(self):
        """ Reformats and validates parameter values """
        self.invalids = []
        self.valid = True
        self.rge = False

        if type(self.value) in (int, float, str):
            self.value = [self.value]

        try:
            if self.array:
                self.value = np.array(self.value, dtype=float)
        except:
            self.valid = False

        if len(self.valids) == 2 and self.array:
            self.rge = True
            for val in self.value:
                if val < self.valids[0]:
                    self.valid = False
                    self.invalids.append(val)
                if val > self.valids[1]:
                    self.valid = False
                    self.invalids.append(val)

        else:
            for val in self.value:
                if val not in self.valids and str(val) not in self.valids:
                    self.valid = False
                    self.invalids.append(val)

        if not self.valid:
            print "\nInvalid input for *" + self.name + "* parameter: "
            #ks print "\t" + str(self.invalids)
            #ks self.display_valid_values()

        return self.valid

    def display_valid_values(self):
        """ Displays the range/grouping of valid values for the parameters """
        tmp = 'range' if self.rge else 'values'
        tmp2 = '-'.join([str(q) for q in self.valids]) if self.rge else ', '.join(self.valids)
        print "\n\tDefault value: " + str(self.default)
        print "\tValid " + tmp + ": " + tmp2


############################################################################
############################################################################

############################################################################
############################################################################


class InputVarSet:
    """ A class that stores, retrieves, and validates input parameters
        for the FuelConsumption and Emissions objects."""
    def __init__(self, params):
        """InputVarSet class constructor

        Required argument:
        params  : a dictionary containing InputVar objects"""
        self.params = params

        #ks - all below
        self.validated_inputs = {}
        if len(params):
            self.validate()
        else:
            print('Error: InputVarSet with no parameters')

    def __repr__(self):
        print('--__repr__ --')
        rep = self.display_input_values(None, print_to_console=True)
        return rep if rep else "Error: no data for InputVarSet"

    def validate(self):
        """ Validates input parameters lengths and values, returns 'True' if
            valid, 'False' if not. If valid, stores validated inputs in the
            .validated_inputs variable.
        """
        valid = True
        ls = [list, np.ndarray]
        self.set_length = p = max([len(m.value) if type(m.value) in ls else 1
                 for m in [self.params[z] for z in self.params]])

        for par in self.params:
            param = self.params[par]
            # validate input ranges
            if not param.validate():
                valid = False

            # validate input lengths
            if type(param.value) in [list, np.ndarray]:
                if not len(param.value) in [p, 1]:
                    valid = False
                    print ("\nInvalid input length for *" + param.name +
                           "* parameter.\nEither set the parameter equal to " +
                           "a single integer or float value, or set equal to " +
                           " a list of length " + str(p) + " to match the" +
                           " length of the other inputs.\nCurrent value: " +
                           str(param.value))

        if valid:
            # Compile input parameters to pass into the dictionary maker method
            for param in self.params:
                tmp = self.params[param]
                self.validated_inputs[tmp.keyword] = tmp.value

        return valid

    def getuniques(self, unique_check):
        """Creates unique consume runs.

        Necessary for reducing processing time on larger (>10000) scenarios

        Can be bypassed (recommened for large runs of non-unique scenarios)
        by setting: unique_check = False
        """

        def mkrun():
            """ Creates variable that links original runs to unique runs """
            rnlnk = []
            for r, run in enumerate(all_runs):
                for u, ur in enumerate(unq_runs):
                    if run == ur:
                        rnlnk.append([r, u])
                        break
            return rnlnk

        def cnvlst():
            """ Converts unique runs to lists """
            for u, ur in enumerate(unq_runs):
                ls = list(ur[:])[:]
                unq_runs[u] = ls
                del ls

        self.uniques_checked = unique_check
        self.unique_inputs = {}
        self._runlnk = []

        if unique_check:
            # transpose unique parameters
            package = []
            dex = 0
            px = {}
            for p in self.validated_inputs:
                if len(self.validated_inputs[p]) > 1:
                    package.append(self.validated_inputs[p])
                    px[p] = dex
                    dex += 1

            all_runs = zip(*package)
            unq_runs = list(set(all_runs))[:]
            runlnk = mkrun()
            runlnk.sort()
            cnvlst()

            # transpose back to get runnable runs
            mod_runs = zip(*list(unq_runs))

            # rebuild input dictionary
            for vi in self.validated_inputs:
                if vi in px:
                    for par in self.params:
                        if par.keyword == vi:
                            if par.array:
                                self.unique_inputs[vi] = np.array(mod_runs[px[vi]])
                            else:
                                self.unique_inputs[vi] = mod_runs[px[vi]]
                else: self.unique_inputs[vi] = self.validated_inputs[vi]
            self._runlnk = runlnk

        else:
            self.unique_inputs = self.validated_inputs

        return self.unique_inputs, self._runlnk

    def save(self, save_file=''):
        """ Saves the input parameter set in CSV format to the specified
            'save_file'"""

        self.validate()
        fl = open(save_file, 'w')
        fl.write(','.join(self.validated_inputs))

        for s in range(0,self.set_length):
            ln = ''
            for val in self.validated_inputs:
                item = self.validated_inputs[val]
                if val in ['burn_type', 'units', 'fm_type']:
                    tmp = str(item[0]) if s == 0 else ''
                else:
                    tmp = str(item[0]) if len(item) == 1 else str(item[s])
                ln += ',' + tmp
            fl.write('\n' + ln.lstrip(','))

        fl.close()
        print "\nInput parameter set saved here: " + save_file


    def load(self, load_file='', display=True):
        """ Loads an input parameter set (that has been saved by the .save()
            method) from the 'load_file'
            Set display to 'False' to not view the loaded data"""

        if display: print "Loading input parameter file: " + load_file

        # reset all inputs
        for par in self.params:
            self.params[par].value = []

        txt = open(load_file, 'r')
        lines = txt.readlines()
        txt.close()
        header = lines[0].replace('\n','').split(',')

        for l,line in enumerate(lines):
            if l > 0:
                ln = line.replace('\n','').split(',')
                for h in header:
                    if h in ['burn_type', 'units', 'fm_type']:
                        if l == 1:
                            self.params[h].value.append(ln[header.index(h)])
                    else:
                        self.params[h].value.append(ln[header.index(h)])

        self.validate()
        if display: self.display_input_values()


    def display_input_values(self, data_source_info, print_to_console=True, tsize=8):
        """Lists the input parameters for the consumption scenario.

        Displays the input parameters for the consumption in the shell. Useful
        as a quick way to check that the scenario parameters have been
        correctly set.

        """
        out = self._display(data_source_info, "value", "Value(s)", "Scenario parameters", tsize)

        if print_to_console: print out
        else: return out


    def display_variable_names(self):
        """ Displays variable names for all parameters """
        print self._display("intname", "Var. Name", "Input parameter variable names")


    def prompt_for_inputs(self):
        """Load scenario inputs from the user.

        Prompts user for the input parameters via the shell in somewhat
        user-friendly manner.

        """

        def validate_input(param):
            prompt ="\t" + param.name + ": "
            t = raw_input(prompt)
            if t in ['v', 'V']:
                param.display_valid_values()
                validate_input(param)
            elif t in ['d', 'D']:
                param.value = param.default
                print "\t  *Default value selected*: " + str(param.default)
            else:
                if param.array:
                    try: param.value = np.hstack([param.value, float(t)])
                    except: param.value = np.hstack([param.value, t])
                else:
                    param.value.append(t)

                if not param.validate():
                    if param.array:
                        param.value = np.delete(param.value, len(param.value) - 1)
                    else:
                        param.value.remove(t)
                    validate_input(param)

        def validate_other_inputs(prompt, vals, tp):
            """ Validates non InputVar object inputs """
            err_message = "\tInvalid input, please try again"
            t = raw_input(prompt)
            try:
                if tp(t) in vals:
                    return t
                else:
                    print err_message
                    t = validate_other_inputs(prompt, vals, tp)
                    return t
            except:
                print err_message
                t = validate_other_inputs(prompt, vals, tp)
                return t


        yes = ['yes', 'y', 'Y', 'YES', 'Yes', 'yeah', 'yup', 'kind of', 'word']
        no = ['n', 'N', 'no', 'NO', 'No', 'naw', 'not really', 'no way', 'get outta here']
        order = ['ecoregion', 'can_con_pct', 'shrub_black_pct',
                 'fm_duff', 'fm_1000hr', 'fm_10hr', 'slope', 'windspeed',
                 'fm_type', 'days_since_rain', 'lengthOfIgnition']
        skipenv = False

        if 'burn_type' not in self.params:
            print "Input prompting is not available for the Emissions object."

        else:
            print ("\n\nYou will now be prompted for each input parameter." +
                   "\n\tInput 'v' at any time to return a list of valid values" +
                   "\n\tInput 'd' to use the default value for the parameter" +
                   "\n\tPress Ctrl-c to abort and quit the prompt\n")

            self.params['burn_type'].value = []
            validate_input(self.params['burn_type'])
            act = True if self.params['burn_type'] in [['activity'], 'activity'] else False

            for param in order + ['fuelbeds', 'area']:
                pact = self.params[param].activity
                if not pact or (pact and act):
                    self.params[param].value = []

            prompt = "\n\tNumber of fuelbeds in scenario: "
            number = int(validate_other_inputs(prompt, range(0,1000), int))

            for i in range(0, int(number)):
                print "\nFuelbed number " + str(i + 1) + ":"

                validate_input(self.params['fuelbeds'])
                validate_input(self.params['area'])

                if not skipenv:
                    print "\nEnvironment parameters: "
                    for keyword in order:
                        pact = self.params[keyword].activity
                        if not pact or (pact and act):
                            validate_input(self.params[keyword])

                if i == 0 and number > 1:
                    prompt = ("\nUse the same environment variables for all" +
                              " fuelbeds? (y or n)")
                    s = validate_other_inputs(prompt, yes + no, str)
                    skipenv = True if s in yes else False

            self.display_input_values(None)


    def _display(self, data_source_information, kwd, kwhead, head, tsize=8):
        """ Displays parameters data based on keyword """
        def tabs(nm):
            t = 4 - (int(len(nm)) / tsize)
            return nm + "\t" * t

        order = ['burn_type', 'fm_type', 'fuelbeds', 'area', 'ecoregion',
                 'fm_1000hr', 'fm_10hr', 'fm_duff', 'can_con_pct',
                 'shrub_black_pct', 'slope', 'windspeed', 'days_since_rain',
                 'lengthOfIgnition', 'efg', 'units']

        txtout = ""
        act = False
        for o in order:
            for par in self.params:
                p = self.params[par]
                dc = {'intname':p.intname, 'value':p.value}
                if o == p.keyword:
                    if o == 'burn_type':
                        bt = p.value
                        if bt in ['activity', ['activity']]:
                            act = True
                    if o == 'fm_type' and act:
                        ft = dc[kwd]

                    if not p.activity or (p.activity and act):
                        txtout += "\n" + tabs(p.name) + str(dc[kwd])

        header =  ("\n" + head + ":\n" + "\n" + tabs("Parameter")
               + tabs(kwhead) + "\n" +
               "--------------------------------------------------------------\n")
        version = util.get_version()
        name = ds_version = date = 'unknown'
        if data_source_information:
            name = data_source_information.generator_name
            ds_version = data_source_information.generator_version
            date = data_source_information.date_generated
        dsi = "\nData source information: {} : {} : {}".format(name, ds_version, date)

        out = header + version + dsi + txtout
        return out
