import os
from .module_locator import module_path

class EmissionsFactorDB:
    """ Emissions Factor Database object

        Loads, stores, and distributes information on the emissions factor
        groups used by Consume 3.0 to calculate emissions from fuel
        consumption data.

        An EmissionsFactorDB is stored within each Emissions object as
        e_obj.efDB
        """

    def __init__(self, emissions_file = "", fuel_consumption_object = None):
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
        self._fco = fuel_consumption_object
        if emissions_file == "":
            mod_path = module_path()
            self.xml_file = os.path.join(mod_path, './input_data/EmissionsFactorDatabase.xml')

        root = get_rootnode(self.xml_file)
        self.data = self._load_emissions_factor_groups(root)

        # this data comes from the loadings input file
        self.fccs_emissions_groups = self._load_emissions_factor_eqid()

        # - only used in the prompt() method, which has been removed
        #ks self.cover_type_descriptions = self._load_covertype()

    def _load_emissions_factor_groups(self, root):
        efg_map = {}
        efg = root.iterfind('EFG')
        for node in efg:
            kids = node.getchildren()
            efg_id = int(get_item('ID', kids))
            components = {}
            for kid in kids:
                components[kid.tag] = get_float(kid.text)
            efg_map[efg_id] = components
        return efg_map

    def _load_emissions_factor_eqid(self):
        ef_eqid_map = {}
        loadings = self._fco.FCCS.loadings_data_
        for i in loadings.fccs_id:
            try:
                components = {}
                components['natural'] = int(loadings.ix[loadings.fccs_id==i].efg_natural)
                components['activity'] = int(loadings.ix[loadings.fccs_id==i].efg_activity)
                ef_eqid_map[i] = components
            except:
                print('Function "_load_emissions_factor_eqid()". Error with fuelbed id: {}'.format(i))
        return ef_eqid_map

    def _load_covertype(self):
        assert False # - this may not be necessary


    def get_key(self, burn_type):
        # could be single element list or simply a string
        key = burn_type[0] if 1 == len(burn_type) else burn_type
        assert key == 'natural' or key == 'activity'
        return key


    def get_efgs(self, fuelbed_list):
        """Gets the appropriate emissions factor groups for the given FCCS IDs

        Links the SAF Cover Type data provided in the FCCS data to the
        appropriate emissions factors from the EmissionsFactorDatabase.xml,
        If multiple cover types exist the first is chosen and mapped to SAF data.
        """
        ef_nums = []
        for f in fuelbed_list:
            eq_id_key = self.get_key(self._fco.burn_type)
            if f in self.fccs_emissions_groups:
                efgs = self.fccs_emissions_groups[f]
                group = efgs[eq_id_key]
                ef_nums.append(group)
            else:
                print("Error: emissions database does not contain equation id for fuelbed {}".format(f))
        return ef_nums

    def browse(self):
        """Display the emissions factor table

        Displays a table of emissions factor groups and their associated
        fuel types and references.
        """
        print ("\nID#\tFuel type\t\t\tReference\n" +
               "-------------------------------------------------")
        for c in self.data:
            out = "{}\t{}\t\t\t{}".format(c,
                self.data[c]['fuel_type'], self.data[c]['references'])
            print(out)

    def info(self, efg_id, ret = False, tsize = 8):
        """Display an emission factor group description.

        Displays emissions factor information for the emissions factor group
        with the specified group id. Requires emissions factor group ID number
        as the only argument. For a list of valid emissions factor groups, use
        the .browse() method.
        """
        check = False
        dat = self.data[int(efg_id)]
        txt = "Emission factor group ID# : " + str(dat['ID'])
        txt += "\nFuel type : " + str(dat['fuel_type'])
        txt += "\nN : " + str(dat['n'])
        txt += "\nReference : " + str(dat['references'])
        txt += ("\n\nEmissions factors (lbs/ton consumed):" +
               "\n\n\t\t" + tabs(tsize, "flaming\t\tsmoldering/residual"))

        for es in ['PM   ', 'PM10b', 'PM25', 'CO   ', 'CO2 ', 'CH4 ', 'NMHC']:
            fla = dat[es.strip() + '_flaming']
            smo = dat[es.strip() + '_smold_resid']
            if not type(fla) is str and not type(smo) is str:
                fla = "%.1f" % fla
                smo = "%.1f" % smo
            txt += "\n" + tabs(tsize, es.rstrip('b')) + tabs(tsize, fla) + tabs(tsize, smo)

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
            print(txt)


def tabs(tsize, nm):
    t = 2 - (int(len(nm)) / tsize)
    return nm + "\t" * t

def get_float(in_str):
    try:
        ret_val = float(in_str)
    except:
        ret_val = in_str
    return ret_val

def get_item(tag, container):
    for item in container:
        if item.tag == tag:
            if item.text: return item.text
            else: print("Error - empty tag {}".format(item.tag))
    print("Error: incorrect file format. Missing tag {}".format(tag))

def get_rootnode(filename):
    from xml.etree import ElementTree as ET
    tree = ET.parse(filename)
    root = tree.getroot()
    del tree
    return root
