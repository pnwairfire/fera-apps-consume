import os

class EmissionsFactorDB:
    """ Emissions Factor Database object

        Loads, stores, and distributes information on the emissions factor
        groups used by Consume 3.0 to calculate emissions from fuel
        consumption data.

        An EmissionsFactorDB is stored within each Emissions object as
        e_obj.efDB"""

    def __init__(self, emissions_file = "", FCobj = None):
        """EmissionsFactorDB class contructor

           Upon initialization, loads emissions factor data from the
           EmissionsFactorDatabase XML file in the input_data directory
           of the consume.py package.

           Optional argument:

           emissions_file   : directory location of the emissions factor
                              database XML. Leave blank to load the default
                              database.
        """

        self.xml_file = emissions_file
        self.FCobj = FCobj
        if emissions_file == "":
            self.xml_file = os.path.join(os.path.split(__file__)[0],
                                      #'input_data/EmissionsFactorDatabase_kjell.xml')
                                      'input_data/EmissionsFactorDatabase.xml')

        self.data = self._load_from_xml_db("EFG")
        self.fccs_emissions_groups = self._load_emissions_factor_eqid(self.xml_file)
        self.cover_type_descriptions = self._load_from_xml_db("cover_type")

        self.valid_efgs = [-1, -2, -5]#, -11, -12, -13, -14] # for later...
        for d in self.data:
            self.valid_efgs.append(d['ID'])
        self.valid_efgs.sort()

    def get_item(self, tag, container):
        for item in container:
            if item.tag == tag:
                if item.text: return item.text
                else: print("Error - empty tag {}".format(item.tag))
        print("Error: incorrect file format. Missing tag {}".format(tag))

    def _load_emissions_factor_eqid(self, file):
        from xml.etree import ElementTree as ET
        tree = ET.parse(file)
        root = tree.getroot()
        del tree

        ef_eqid_map = {}
        ef_eqid = root.iterfind('FCCS_EFG')
        for node in ef_eqid:
            kids = node.getchildren()
            id = self.get_item('fccs_id', kids)
            components = {}
            components['all_nat'] = self.get_item('all_nat', kids)
            components['all_act_west'] = self.get_item('all_act_west', kids)
            components['all_act_other'] = self.get_item('all_act_other', kids)
            ef_eqid_map[id] = components
        return ef_eqid_map

    def load_data(self, node, tag_name, text_data):
        """ Loads data from xml file based on the given tag name """
        if tag_name in text_data:
            data = node.findtext(tag_name)
        else:
            if node.findtext(tag_name) == 'na':
                data = 'na'
            else:
                data = 0.0
                data = node.findtext(tag_name)
                if not data or float(data) < 0:
                    data = 0.0
                else:
                    data = float(data)
        return data

    def _load_from_xml_db(self, tag):
        """Load emissions factor data from an external xml file
        """
        tag_name_efg = ['ID', 'fuel_type', 'n', 'references', 'PM_flaming',
                        'PM10b_flaming', 'PM25_flaming', 'CO_flaming',
                        'CO2_flaming', 'CH4_flaming', 'NMHC_flaming',
                        'PM_smold_resid', 'PM10b_smold_resid',
                        'PM25_smold_resid', 'CO_smold_resid', 'CO2_smold_resid',
                        'CH4_smold_resid', 'NMHC_smold_resid']

        tag_name_ct = ['cover_type_ID', 'type_number', 'type_name']
        text_data = (['ID', 'fuel_type', 'references', 'n', 'fccs_id'] + tag_name_ct)

        from xml.etree import ElementTree as ET
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        del tree

        if tag == "EFG":
            tag_names = tag_name_efg
        elif tag == "cover_type":
            tag_names = tag_name_ct
        else:
            assert False
            print "Weird error somewhere"

        allData = []
        for node in root:
            temp = {}
            if node.tag == tag:
                for tn in tag_names:
                    temp[tn] = (self.load_data(node, tn, text_data))
                allData.append(temp)

        del root
        return allData


    def browse(self):
        """Display the emissions factor table

        Displays a table of emissions factor groups and their associated
        fuel types and references.
        """
        print ("\nID#\tFuel type\t\tReference\n" +
               "-------------------------------------------------")
        for c in self.data:
            print (str(c['ID']) + "\t" + str(c['fuel_type']) +
                "\t" + str(c['references']))

    def tabs(self, nm):
        t = 2 - (int(len(nm)) / tsize)
        return nm + "\t" * t

    check = True
    txt = ""

    def info(self, efg_id, ret = False, tsize = 8):
        """Display an emission factor group description.

        Displays emissions factor information for the emissions factor group
        with the specified group id. Requires emissions factor group ID number
        as the only argument. For a list of valid emissions factor groups, use
        the .browse() method.
        """

        for i in range(0, len(self.data)):
            if int(self.data[i]['ID']) == int(efg_id):
                check = False
                dat = self.data[i]
                txt += "Emission factor group ID# : " + str(dat['ID'])
                txt += "\nFuel type : " + str(dat['fuel_type'])
                txt += "\nN : " + str(dat['n'])
                txt += "\nReference : " + str(dat['references'])
                txt += ("\n\nEmissions factors (lbs/ton consumed):" +
                       "\n\n\t\t" + self.tabs("flaming\t\tsmoldering/residual"))

                for es in ['PM   ', 'PM10b', 'PM25', 'CO   ', 'CO2 ', 'CH4 ', 'NMHC']:
                    fla = dat[es.strip() + '_flaming']
                    smo = dat[es.strip() + '_smold_resid']
                    if not type(fla) is str and not type(smo) is str:
                        fla = "%.1f" % fla
                        smo = "%.1f" % smo
                    txt += "\n" + self.tabs(es.rstrip('b')) + self.tabs(fla) + self.tabs(smo)

        if int(efg_id) == -1:
            check = False
            txt += ('\nSetting emissions factor group ID# to -1 will ' +
                    'auto-select an emissions group based on the selected ' +
                    'FCCS ID#.\n\nThe group selected is based on the SAM/SRF' +
                    ' Covertypes associated with the FCCS ID#. For fuelbeds' +
                    ' for which multiple groups are valid, the majority will' +
                    ' selected. If no majority exists, the first group will' +
                    ' be selected')

        if check:
            txt += ("\nEmissions factor group ID# " + str(efg_id) +
                   " was not found. Valid group ID#s are listed below:")
            self.browse()

        if ret:
            return txt
        else:
            print txt


    def get_key(self, burn_type, ecoregion):
        key = 'bogus'
        if burn_type == 'natural':
            key = 'all_nat'
        elif burn_type == 'activity':
            key = 'all_act_west' if ecoregion == 'western' else 'all_act_other'
        return key

    def get_group_id(self, efgs, key):
        id = 0
        group = efgs[key]
        id = group.split('|')[0] if '|' in group else group
        return id


    def get_efgs(self, emissions_factor_group, fuelbed_list, ecoregion):
        """Gets the appropriate emissions factor groups for the given FCCS IDs

        Links the SAF Cover Type data provided in the FCCS data to the
        appropriate emissions factors from the EmissionsFactorDatabase.xml,
        then checks if multiple appropriate emissions factors exist.

        If multiple valid sets exist, the emissions_factor_group argument
        determines whether a group is automatically selected (auto selection
        chooses the majority set or the first set listed if no majority
        exists) or prompts the user to choose a group of emissions factors.

        emissions_factor_group  :   # valid (acc. to Ottmar/Prichard) groupings:
                                    -1 = all burns, auto-select
                                    -2 = all burns, user-select

                                    # proposed/not yet validated groupings:
                                    -11 = natural burns, auto-select
                                    -12 = natural burns, user-select
                                    -13 = activity burns, auto-select
                                    -14 = activity burns, user-select

        """
        # Main program
        ef_nums = []
        for f in range(0, len(fuelbed_list)): #<<< uinput
            fuelbed_id = fuelbed_list[f]
            eq_id_key = self.get_key(self.FCobj.burn_type.value[0], ecoregion)
            if fuelbed_id in self.fccs_emissions_groups:
                efgs = self.fccs_emissions_groups[fuelbed_id]
                group = efgs[eq_id_key]
                ef_nums.append(self.get_group_id(efgs, eq_id_key))
            else:
                print("Error: emissions database does not contain equation id for fuelbed {}".
                    format(fuelbed_id))
        return ef_nums

##        def majority(lst):
##            """ Returns the majority value of a given list """
##            mlst = [[lst[0], 0]]
##            for i in lst:
##                found = False
##                for j in range(0, len(mlst)):
##                    if i == mlst[j][0]:
##                        mlst[j][1] += 1
##                        found = True
##                if not found:
##                    mlst.append([i, 1])
##
##            maj = mlst[0][0]
##            cnt = 1
##            for k in mlst:
##                if k[1] > cnt:
##                    maj = k[0]
##                    cnt = k[1]
##
##            return maj
##
##        def run_prompt():
##            """ Prompts user to choose which emissions factor group they'd
##                like to use """
##
##            ef_eqs = []
##            ct_names = []
##            ct_display = ""
##            opt = 1
##            for fd in self.FCobj.FCCS.data:
##                if int(fd[0]) == int(fuelbed_id):
##                    fbct = fd[2].split(',')
##                    sn = fd[59]
##                    break
##
##            for fb in fbct:
##                for ct in self.cover_type_descriptions:
##                    if fb == ct[0]:
##                        ct_names.append(' - '.join(ct[1:3]))
##
##            for ct_name in ct_names:
##                ct_display += ("\n\t" + str(opt) + ". " + ct_name +
##                " - emissions factor set #" + efgs[opt-1])
##                opt += 1
##
##            ct_display += ("\n\t" + str(opt)
##                            + ". Default - emissions factor set #0")
##
##            print ("\nFCCS fuelbed " + str(fuelbed_id) + #<<< uin
##           ": " + sn +
##           "\nFor the given parameters, multiple emissions factor types are " +
##           "valid.\nChoose an SAF/SRM cover type from which to derive " +
##           "appropriate emissions factors from among the following:")
##
##            choice = get_input(len(efgs) + 1, ct_display)
##            if choice == (len(ct_names) + 1):
##                ans = 0
##            else:
##                ans = int(efgs[int(choice) - 1])
##
##            return ans
##
##        def get_input(length, ct_display):
##            """ Pulls choice from the shell and validates"""
##            print ct_display
##            choice = input("\nCover type choice (1-" + str(length) + "): ")
##
##            if choice not in range(1, (length + 1)):
##                print "Invalid choice. Please select among: "
##                choice = get_input(length, ct_display)
##                return choice
##            else:
##                return choice
