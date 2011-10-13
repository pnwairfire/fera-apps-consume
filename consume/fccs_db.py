import data_desc as dd
import os

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
            self.xml_file = os.path.join('./input_data/FCCS_loadings.xml')

        self.data = self._load_data_from_xml()
        self.data.sort()
        self.valids = []
        for f in self.data:
            self.valids.append(str(f[0]))


    def _load_data_from_xml(self):
        """Load FCCS data from an external file.

        Loads FCCS data from an XML file in the format of the FCCS XML file
        that is used by the official GUI version of CONSUME

        """

        text_data = ['site_name', 'ecoregion', 'cover_type', 'site_description',
            'srm_id', 'srm_description']

        pct_data = ['shrubs_Primary_perc_live', 'shrubs_Secondary_perc_live',
                    'nw_Primary_perc_live', 'nw_Secondary_perc_live',
                    'lichenDep_perc', 'mossDep_perc', 'litterShortNeedle_perc',
                    'litterLongNeedle_perc', 'litterOtherConf_perc',
                    'litterBroadleafDecid_perc', 'litterBroadleafEver_perc',
                    'litterPalmFrond_perc', 'litterGrass_perc',
                    'g_DuffDep_Upper_perc', 'g_DuffDep_Lower_perc',
                    'litterDep_perc'] # gBasPercent not included purposefully

        def load_data(node, tag_name):
            """ Loads data from xml file for the given tag name """

            if tag_name in text_data:
                return node.findtext(tag_name)

            elif tag_name in ['fuelbed_number', 'fccs_id']:
                fb_num = int(node.findtext(tag_name))
                return fb_num
            else:
                data = 0
                data = node.findtext(tag_name)
                if not data or float(data) < 0:
                    data = 0.0
               #FCCS shrub loadings are multipled by 3 for use by Consume.
               #Not sure why, but it's in the CONSUME 3.0 manual (p. 75)
                if tag_name in ['shrubs_Primary', 'shrubs_Secondary']:
                    data = float(data) * 3.0

                if tag_name in pct_data:
                    data = float(data) / 100.0

            return float(data)

        from xml.etree import ElementTree as ET
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        del tree

        fccs = []
        for node in root:
            temp = [0] * len(dd.LoadDefs)
            for ld in dd.LoadDefs:
                temp[ld[2]] = load_data(node, ld[0])
            fccs.append(temp)

        del root
        return fccs

    def get_canopy_pct(self, fcs):
        """Returns the auto-calculated canopy consumption percent value for the
           given FCCS fuelbed ID#"""

        err = ("No auto-calculated canopy consumption percent value " +
                       "for the selected fuelbed ID: ")
        if type(fcs) in (str, int, float):
            if int(fcs) in self.fccs_canopy_consumption_pct:
                return self.fccs_canopy_consumption_pct[int(fcs)]
            else:
                print err + str(fcs)

        else:
            ccs = []
            for f in fcs:
                if int(f) in self.fccs_canopy_consumption_pct:
                    ccs.append(self.fccs_canopy_consumption_pct[int(f)])
                else:
                    print err + str(f)
                    return ""
            return ccs


    def browse(self):
        """Display a list of FCCS fuelbeds.

        Displays a list of FCCS ID#'s and their corresponding site names. Useful
        as a quick reference.

        """

        for c in self.data:
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
        print "   Litter % cover\t\tlit_pctcv\t\t" + pu
        print "   Litter type distribution:"
        print "      Short needle\t\tlit_s_ndl_pct\t\t" + pu
        print "      Long needle\t\tlit_l_ndl_pct\t\t" + pu
        print "      Other conifer\t\tlit_o_ndl_pct\t\t" + pu
        print "      Broadleaf deciduous\tlit_blf_d_pct\t\t" + pu
        print "      Broadleaf evergreen\tlit_blf_e_pct\t\t" + pu
        print "      Palm frond\t\tlit_palm_pct\t\t" + pu
        print "      Grass\t\t\tlit_grass_pct\t\t" + pu
        print "   Lichen depth\t\t\tlch_depth\t\t" + du
        print "   Lichen % cover\t\tlch_pctcv\t\t" + pu
        print "   Moss depth\t\t\tmoss_depth\t\t" + du
        print "   Moss % cover\t\t\tmoss_pctcv\t\t" + pu
        print "   Moss type\t\t\tmoss_type\t\t" + nau
        print header
        print "\n Ground fuel loadings"
        print "   Duff depth, upper\t\tduff_upper_depth\t" + du
        print "   Duff % cover, upper\t\tduff_upper_pctcv\t" + pu
        print "   Duff derivation, upper\tduff_upper_deriv\t" + nau
        print "   Duff depth, lower\t\tduff_lower_depth\t" + du
        print "   Duff % cover, lower\t\tduff_lower_pctcv\t" + pu
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
        for i in range(0, len(self.data)):
            if int(self.data[i][0]) == int(fccs_id):
                check = False
                data = self.data[i]
                text += "\nFCCS ID# : " + str(data[0])
                text += "\nSite name: " + str(data[59])
                text += "\n\nSite description: " + str(data[60])

                if detail:
                    lu = ' tons/ac'     # loading units
                    du = ' in'          # depth units
                    pu = '%'             # percent units
                    nu = ' #/acre'      # density units (basal acc., sq. middens)
                    ru = ' feet'         # radius units
                    text += "\n\n\tBailey's ecoregion division(s): " + str(data[1])
                    text += "\n\tSAM/SRM cover type(s): " + str(data[2])

                    text += "\n\n\tCanopy loadings"
                    text += "\n\t   Overstory: " + str(data[3]) + lu
                    text += "\n\t   Midstory: " + str(data[4]) + lu
                    text += "\n\t   Understory: " + str(data[5]) + lu
                    text += "\n\t   Snags, class 1, foliage: " + str(data[6]) + lu
                    text += "\n\t   Snags, class 1, wood: " + str(data[7]) + lu
                    text += "\n\t   Snags, class 1, w/o foliage: " + str(data[8]) + lu
                    text += "\n\t   Snags, class 2: " + str(data[9]) + lu
                    text += "\n\t   Snags, class 3: " + str(data[10]) + lu
                    text += "\n\t   Ladder fuels: " + str(data[11]) + lu

                    text += "\n\n\tShrub loadings"
                    text += "\n\t   Shrub Primary: " + str(data[12]) + lu
                    text += "\n\t   Shrub Primary % live: " + str(data[13]*100) + pu
                    text += "\n\t   Shrub Secondary: " + str(data[14]) + lu
                    text += "\n\t   Shrub Secondary % live: " + str(data[15]*100) + pu

                    text += "\n\n\tNonwoody loadings"
                    text += "\n\t   NW Primary: " + str(data[16]) + lu
                    text += "\n\t   NW Primary % live: " + str(data[17]*100) + pu
                    text += "\n\t   NW Secondary: " + str(data[18]) + lu
                    text += "\n\t   NW Secondary % live: " + str(data[19]*100) + pu

                    text += "\n\n\tLitter-lichen-moss loadings"
                    text += "\n\t   Litter depth: " + str(data[23]) + du
                    text += "\n\t   Litter % cover: " + str(data[24]*100) + pu
                    text += "\n\t   Litter type distribution:"
                    text += "\n\t      Short needle: " + str(data[30]*100) + pu
                    text += "\n\t      Long needle: " + str(data[31]*100) + pu
                    text += "\n\t      Other conifer: " + str(data[32]*100) + pu
                    text += "\n\t      Broadleaf deciduous: " + str(data[33]*100) + pu
                    text += "\n\t      Broadleaf evergreen: " + str(data[34]*100) + pu
                    text += "\n\t      Palm frond: " + str(data[35]*100) + pu
                    text += "\n\t      Grass: " + str(data[36]*100) + pu
                    text += "\n\t   Lichen depth: " + str(data[25]) + du
                    text += "\n\t   Lichen % cover: " + str(data[26]*100) + pu
                    text += "\n\t   Moss depth: " + str(data[27]) + du
                    text += "\n\t   Moss % cover: " + str(data[28]*100) + pu
                    text += "\n\t   Moss type: " + str(data[29])

                    text += "\n\n\tGround fuel loadings"
                    text += "\n\t   Duff depth, upper: " + str(data[37]) + du
                    text += "\n\t   Duff % cover, upper: " + str(data[38]*100) + pu
                    text += "\n\t   Duff derivation, upper: " + str(data[39])
                    text += "\n\t   Duff depth, lower: " + str(data[40]) + du
                    text += "\n\t   Duff % cover, lower: " + str(data[41]*100) + pu
                    text += "\n\t   Duff derivation, lower: " + str(data[42])
                    text += "\n\t   Basal accumulations depth: " + str(data[43]) + du
                    text += "\n\t   Basal accum. % cover: " + str(data[44]*100) + pu
                    text += "\n\t   Basal accumulations radius: " + str(data[45]) + ru
                    text += "\n\t   Squirrel midden depth: " + str(data[46]) + du
                    text += "\n\t   Squirrel midden density: " + str(data[47]) + nu
                    text += "\n\t   Squirrel midden radius: " + str(data[48]) + ru

                    text += "\n\n\tWoody fuel loadings"
                    text += '\n\t   1-hr (0-0.25"): ' + str(data[49]) + lu
                    text += '\n\t   10-hr (0.25-1"): ' + str(data[50]) + lu
                    text += '\n\t   100-hr (1-3"): ' + str(data[51]) + lu
                    text += '\n\t   1000-hr (3-9"), sound: ' + str(data[52]) + lu
                    text += '\n\t   10,000-hr (9-20"), sound: ' + str(data[53]) + lu
                    text += '\n\t   10,000-hr+ (>20"), sound: ' + str(data[54]) + lu
                    text += '\n\t   1000-hr (3-9"), rotten: ' + str(data[55]) + lu
                    text += '\n\t   10,000-hr (9-20"), rotten: ' + str(data[56]) + lu
                    text += '\n\t   10,000-hr+ (>20"), rotten: ' + str(data[57]) + lu
                    text += "\n\t   Stumps, sound: " + str(data[20]) + lu
                    text += "\n\t   Stumps, rotten: " + str(data[21]) + lu
                    text += "\n\t   Stumps, lightered: " + str(data[22]) + lu

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
