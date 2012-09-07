import os
import data_desc as dd
from collections import namedtuple
import module_locator

class FCCSDB():
    """ A class the stores, retrieves, and distributes FCCS fuelbed information
    """
    def __init__(self, fccs_file=""):
        """ FCCSDB class constructor.

        Upon initialization, FCCS data is loaded into the DB object.

        Argument:

        fccs_file : directory location of the FCCS Loadings XML provided
                    with the consume.py package"""

        self.xml_file = fccs_file
        if fccs_file == "":
            mod_path = module_locator.module_path()
            self.xml_file = os.path.join(mod_path, './input_data/fccs_loadings_1_458.csv')

        #(self.loadings_data_, self.data_info) = self._load_data_from_xml()
        (self.loadings_data_, self.data_info) = self._load_data_from_csv()
        self.valid_fuelbeds_ = [int(i) for i in self.loadings_data_.fccs_id]

        '''
        self.loadings_data_.sort()
        self.valid_fuelbeds_ = []
        for f in self.loadings_data_:
            self.valid_fuelbeds_.append(str(f[0]))
        '''

    @property
    def data_source_info(self): return self.data_info

    def _load_data_from_xml(self):
        """Load FCCS data from an external file.
        """

        text_data = ['site_name', 'ecoregion', 'cover_type', 'site_description',
                     'srm_id', 'srm_description']

        pct_data = ['shrubs_primary_perc_live', 'shrubs_secondary_perc_live', \
                    'nw_primary_perc_live', 'nw_secondary_perc_live']

        def load_data(node, tag_name):
            """ Loads data from xml file for the given tag name
                The data structue returned is a list of lists of the values in the
                dd.LoadDefs structure
            """

            if tag_name in text_data:
                return node.findtext(tag_name)

            elif tag_name in ['fccs_id', 'fccs_id']:
                fb_num = int(node.findtext(tag_name))
                return fb_num
            else:
                data = node.findtext(tag_name)
                if not data or float(data) < 0:
                    data = 0.0

                if tag_name in pct_data:
                    data = float(data) / 100.0

            return float(data)

        from xml.etree import ElementTree as ET
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        del tree

        data_info = self._get_data_info(root)

        fccs = []
        for node in root:
            if node.tag == "generator_info": continue

            ### - zero initialized list size of LoadDefs
            temp = [0] * len(dd.LoadDefs)
            for ld in dd.LoadDefs:
                temp[ld[2]] = load_data(node, ld[0])
            fccs.append(temp)

        del root
        return (fccs, data_info)

    def _load_data_from_csv(self):
        """Load FCCS data from an external file.
        """
        DataInfo = namedtuple('DataInfo', ['generator_name', 'generator_version', 'date_generated'])
        pct_data = ['shrubs_primary_perc_live', 'shrubs_secondary_perc_live', 'nw_primary_perc_live', 'nw_secondary_perc_live']
        import pandas as pan
        loadings_data = pan.read_csv(self.xml_file)

        # - todo: convert percentage data. should this be done in FCCS?
        loadings_data[pct_data] = loadings_data[pct_data] * 0.01

        for item in dd.LoadDefs:
            loadings_data.rename(columns={item[0] : item[1]}, inplace=True)

        return(loadings_data, DataInfo("unknown", "unknown", "unknown"))

    def _get_data_info(self, root):
        DataInfo = namedtuple('DataInfo', ['generator_name', 'generator_version', 'date_generated'])
        node = root.find('generator_info')
        if None != node:
            name = node.find('generator_name')
            version = node.find('generator_version')
            date = node.find('date_generated')
            g_name = name.text if None != name else "unknown"
            g_version = version.text if None != version else "unknown"
            g_date = date.text if None != date else "unknown"
            data_info = DataInfo(g_name, g_version, g_date)
        else:
            print("\nWarning: consume loadings file has no generator information!\n")
            data_info = DataInfo("unknown", "unknown", "unknown")
        return data_info

    def get_available_fuelbeds(self):
        return self.valid_fuelbeds_

    def browse(self):
        """Display a list of FCCS fuelbeds.

        Displays a list of FCCS ID#'s and their corresponding site names. Useful
        as a quick reference.

        """

        for c in self.loadings_data_:
            print "ID# " + str(c[0]) + "\t: " + str(c[59])

        print ("\nFor more information on a specific fuelbed, use the " +
               ".info(id#, detail=True/False) method.\n")


    def list_fuel_loading_names(self):
        """Displays a list of variable names for fuel loadings.

        Lists variable names for FCCS fuel loadings as a guide for users
        who would like to customize fuel loadings using the
        '.customized_fuel_loadings' method.

        """

        lu = ' tons/acre'     # loading units
        du = ' inches'          # depth units
        pu = ' %'             # percent units
        nu = ' #/acre'      # density units (basal acc., sq. middens)
        ru = ' feet'         # radius units
        nau = ' integer b/t 1-4'
        header = (
        "\n------------------------------------------------------------"
        + "-----\n   Fuel stratum\t\t\tVariable name\t\t Units\n-----" +
        "------------------------------------------------------------")


        print header
        print "\n Canopy loadings"
        print "   Overstory\t\t\toverstory\t\t" + lu
        print "   Midstory\t\t\tmidstory\t\t" + lu
        print "   Understory\t\t\tunderstory\t\t" + lu
        print "   Snags, class 1, foliage\tsnag1f\t\t\t" + lu
        print "   Snags, class 1, wood\t\tsnag1w\t\t\t" + lu
        print "   Snags, class 1, w/o foliage\tsnag1nf\t\t\t" + lu
        print "   Snags, class 2\t\tsnag2\t\t\t" + lu
        print "   Snags, class 3\t\tsnag3\t\t\t" + lu
        print "   Ladder fuels\t\t\tladder\t\t\t" + lu

        print "\n Shrub loadings"
        print "   Primary\t\t\tshrub_prim\t\t" + lu
        print "   Primary % live\t\tshrub_prim_pctlv\t" + pu
        print "   Secondary\t\t\tshrub_seco\t\t" + lu
        print "   Secondary % live\t\tshrub_seco_pctlv\t" + pu

        print "\n Nonwoody loadings"
        print "   Primary\t\t\tnw_prim\t\t\t" + lu
        print "   Primary % live\t\tnw_prim_pctlv\t\t" + pu
        print "   Secondary\t\t\tnw_seco\t\t\t" + lu
        print "   Secondary % live\t\tnw_seco_pctlv\t\t" + pu
        print header
        print "\n Litter-lichen-moss loadings"
        print "   Litter depth\t\t\tlit_depth\t\t" + du
        print "   Lichen depth\t\t\tlch_depth\t\t" + du
        print "   Moss depth\t\t\tmoss_depth\t\t" + du
        print "   Moss type\t\t\tmoss_type\t\t" + nau
        print header
        print "\n Ground fuel loadings"
        print "   Duff depth, upper\t\tduff_upper_depth\t" + du
        print "   Duff derivation, upper\tduff_upper_deriv\t" + nau
        print "   Duff depth, lower\t\tduff_lower_depth\t" + du
        print "   Duff derivation, lower\tduff_lower_deriv\t" + nau
        print "   Basal accumulations depth\tbas_depth\t\t" + du
        print "   Basal accumulations % cover\tbas_pct\t\t\t" + pu
        print "   Basal accumulations radius\tbas_rad\t\t\t" + ru
        print "   Squirrel midden depth\tsqm_depth\t\t" + du
        print "   Squirrel midden density\tsqm_density\t\t" + nu
        print "   Squirrel midden radius\tsqm_radius\t\t" + ru

        print "\n Woody fuel loadings"
        print '   1-hr (0-0.25")\t\tone_hr_sound\t\t' + lu
        print '   10-hr (0.25-1")\t\tten_hr_sound\t\t' + lu
        print '   100-hr (1-3")\t\thun_hr_sound\t\t' + lu
        print '   1000-hr (3-9"), sound\toneK_hr_sound\t\t' + lu
        print '   10,000-hr (9-20"), sound\ttenK_hr_sound\t\t' + lu
        print '   10,000-hr+ (>20"), sound\ttnkp_hr_sound\t\t' + lu
        print '   1000-hr (3-9"), rotten\toneK_hr_rotten\t\t' + lu
        print '   10,000-hr (9-20"), rotten\ttenK_hr_rotten\t\t' + lu
        print '   10,000-hr+ (>20"), rotten\ttnkp_hr_rotten\t\t' + lu
        print "   Stumps, sound\t\tstump_sound\t\t" + lu
        print "   Stumps, rotten\t\tstump_rotten\t\t" + lu
        print "   Stumps, lightered\t\tstump_lightered\t\t" + lu

    def info(self, fccs_id, detail=False, ret = False):
        """Display an FCCS fuelbed description.

        Prints fuel loading information on the fuelbed with the specified
        FCCS ID. Requires one argument: an integer refering to a specific FCCS
        ID. For a list of valid FCCS IDs, use the .browse_fccs() method.

        """

        check = True
        text = ""
        for i in range(0, len(self.loadings_data_)):
            if int(self.loadings_data_[i][0]) == int(fccs_id):
                check = False
                data = self.loadings_data_[i]
                text += "\nFCCS ID# : " + str(data[0])
                text += "\nSite name: " + str(data[1])
                text += "\n\nSite description: " + str(data[2])

                if detail:
                    lu = ' tons/ac'     # loading units
                    du = ' in'          # depth units
                    pu = '%'             # percent units
                    nu = ' #/acre'      # density units (basal acc., sq. middens)
                    ru = ' feet'         # radius units
                    text += "\n\n\tBailey's ecoregion division(s): " + str(data[3])
                    text += "\n\n\tCanopy loadings"
                    text += "\n\t   Overstory: " + str(data[4]) + lu
                    text += "\n\t   Midstory: " + str(data[5]) + lu
                    text += "\n\t   Understory: " + str(data[6]) + lu
                    text += "\n\t   Snags, class 1, foliage: " + str(data[7]) + lu
                    text += "\n\t   Snags, class 1, wood: " + str(data[8]) + lu
                    text += "\n\t   Snags, class 1, w/o foliage: " + str(data[9]) + lu
                    text += "\n\t   Snags, class 2: " + str(data[10]) + lu
                    text += "\n\t   Snags, class 3: " + str(data[11]) + lu
                    text += "\n\t   Ladder fuels: " + str(data[12]) + lu

                    text += "\n\n\tShrub loadings"
                    text += "\n\t   Shrub Primary: " + str(data[13]) + lu
                    text += "\n\t   Shrub Primary % live: " + str(data[14]*100) + pu
                    text += "\n\t   Shrub Secondary: " + str(data[15]) + lu
                    text += "\n\t   Shrub Secondary % live: " + str(data[16]*100) + pu

                    text += "\n\n\tNonwoody loadings"
                    text += "\n\t   NW Primary: " + str(data[17]) + lu
                    text += "\n\t   NW Primary % live: " + str(data[18]*100) + pu
                    text += "\n\t   NW Secondary: " + str(data[19]) + lu
                    text += "\n\t   NW Secondary % live: " + str(data[20]*100) + pu

                    text += "\n\n\tLitter-lichen-moss loadings"
                    text += "\n\t   Litter depth: " + str(data[24]) + du
                    text += "\n\t   Litter loading: " + str(data[25]) + lu

                    text += "\n\t   Lichen depth: " + str(data[26]) + du
                    text += "\n\t   Lichen loading: " + str(data[27]) + lu

                    text += "\n\t   Moss depth: " + str(data[28]) + du
                    text += "\n\t   Moss loading: " + str(data[29]) + lu

                    text += "\n\n\tGround fuel loadings"
                    text += "\n\t   Duff depth, upper: " + str(data[30]) + du
                    text += "\n\t   Duff loading, upper: " + str(data[31]) + lu
                    text += "\n\t   Duff depth, lower: " + str(data[32]) + du
                    text += "\n\t   Duff loading, lower: " + str(data[33]) + lu
                    text += "\n\t   Basal accumulations loading: " + str(data[34]) + lu
                    text += "\n\t   Squirrel midden loading: " + str(data[35]) + ru

                    text += "\n\n\tWoody fuel loadings"
                    text += '\n\t   1-hr (0-0.25"): ' + str(data[36]) + lu
                    text += '\n\t   10-hr (0.25-1"): ' + str(data[37]) + lu
                    text += '\n\t   100-hr (1-3"): ' + str(data[38]) + lu
                    text += '\n\t   1000-hr (3-9"), sound: ' + str(data[39]) + lu
                    text += '\n\t   10,000-hr (9-20"), sound: ' + str(data[40]) + lu
                    text += '\n\t   10,000-hr+ (>20"), sound: ' + str(data[41]) + lu
                    text += '\n\t   1000-hr (3-9"), rotten: ' + str(data[42]) + lu
                    text += '\n\t   10,000-hr (9-20"), rotten: ' + str(data[43]) + lu
                    text += '\n\t   10,000-hr+ (>20"), rotten: ' + str(data[44]) + lu
                    text += "\n\t   Stumps, sound: " + str(data[21]) + lu
                    text += "\n\t   Stumps, rotten: " + str(data[22]) + lu
                    text += "\n\t   Stumps, lightered: " + str(data[23]) + lu

        if check:
            text += ("\nFuelbed ID# " + str(fccs_id) + " was not found." +
                   "  Use the .browse_fccs() method to view a list of valid "
                   + "fuelbeds.")

        if ret:
            return text
        else: print text

"""class FuelLoadingParameter(object):
    def __init__(self, xmltag, inttag, strtag, idx, units):
        self.xmltag = xmltag
        self.inttag = inttag
        self.strtag = strtag
        self.idx = idx
        self.units = units

    def __repr__(self):
        return self.strtag"""
