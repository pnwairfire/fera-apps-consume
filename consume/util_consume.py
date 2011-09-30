import numpy as np
import math
import data_desc as dd

def make_dictionary_of_lists(cons_data, heat_data, emis_data, inputs, cons_debug_data=""):
    """

    Creates a dictionary of lists (accessed by calling the 'results' property)
    from the 'cons_data' and 'emis_data' arrays that are generated from the
    FUELCONSUMPTIONOBJECT._calculate() and EMISSIONSOBJECT._calculate()
    methods respectively.

    Note: the dictionary can be created without 'emis_data' if only consumption
          data is desired/needed.

    """
    def cons_dict(s):
        """ Return consumption dictionary for specified index"""
        return {
        'flaming' : cons_data[s][0],
        'smoldering' : cons_data[s][1],
        'residual' : cons_data[s][2],
        'total' : cons_data[s][3]}

    def cons_debug_dict(s):
        """ Return consumption dictionary for specified index"""
        if len(cons_debug_data):
            return { 'total' : cons_debug_data[s] }
        else:
            return None

    def emis_dict(s, p):
        """ Return emissions dictionary for specified index & species """
        return {
            'flaming' : emis_data[p][s][0],
            'smoldering' : emis_data[p][s][1],
            'residual' : emis_data[p][s][2],
            'total' : emis_data[p][s][3]}

    def emis_dict_detail(p):
        """ Return detailed emissions dictionary for specified species """
        return {
            'canopy' : emis_dict(1, p),
            'shrub' : emis_dict(2, p),
            'nonwoody' : emis_dict(3, p),
            'litter-lichen-moss' : emis_dict(4, p),
            'ground fuels' : emis_dict(5, p),
            'woody fuels' : emis_dict(6, p)}

    all_heat = {
        'flaming' : heat_data[0][0],
        'smoldering' : heat_data[0][1],
        'residual' : heat_data[0][2],
        'total' : heat_data[0][3]}

    all_cnsm = cons_dict(0)
    can_cnsm = cons_dict(1)
    shb_cnsm = cons_dict(2)
    nw_cnsm = cons_dict(3)
    llm_cnsm = cons_dict(4)
    gf_cnsm = cons_dict(5)
    woody_cnsm = cons_dict(6)
    can_over = cons_dict(7)
    can_mid = cons_dict(8)
    can_under = cons_dict(9)
    can_snags_1_f = cons_dict(10)
    can_snags_1_w = cons_dict(11)
    can_snags1nf = cons_dict(12)
    can_snags_2 = cons_dict(13)
    can_snags_3 = cons_dict(14)
    can_ladder = cons_dict(15)
    shb_prim_live = cons_dict(16)
    shb_prim_dead = cons_dict(17)
    shb_seco_live = cons_dict(18)
    shb_seco_dead = cons_dict(19)
    nw_prim_live = cons_dict(20)
    nw_prim_dead = cons_dict(21)
    nw_seco_live = cons_dict(22)
    nw_seco_dead = cons_dict(23)
    llm_litter = cons_dict(24)
    llm_lichen = cons_dict(25)
    llm_moss = cons_dict(26)
    gf_duff_upper = cons_dict(27)
    gf_duff_lower = cons_dict(28)
    gf_ba = cons_dict(29)
    gf_sm = cons_dict(30)
    wd_stumps_snd = cons_dict(31)
    wd_stumps_rot = cons_dict(32)
    wd_stumps_lgt = cons_dict(33)
    wd_hr1 = cons_dict(34)
    wd_hr10 = cons_dict(35)
    wd_hr100 = cons_dict(36)
    wd_hr1000_snd = cons_dict(37)
    wd_hr1000_rot = cons_dict(38)
    wd_hr10000_snd = cons_dict(39)
    wd_hr10000_rot = cons_dict(40)
    wd_hr10kp_snd = cons_dict(41)
    wd_hr10kp_rot = cons_dict(42)

    lit_mean_bd = cons_debug_dict(0)
    ff_reduction = cons_debug_dict(1)

    results = {'parameters' : inputs,
               'heat release' : all_heat,

               'consumption' : { 'summary' : {
                                    'total' : all_cnsm,
                                    'canopy' : can_cnsm,
                                    'shrub' : shb_cnsm,
                                    'nonwoody' : nw_cnsm,
                                    'litter-lichen-moss' : llm_cnsm,
                                    'ground fuels' : gf_cnsm,
                                    'woody fuels' : woody_cnsm},
                                 'canopy' : {
                                    'overstory' : can_over,
                                    'midstory' : can_mid,
                                    'understory' : can_under,
                                    'snags class 1 foliage' : can_snags_1_f,
                                    'snags class 1 wood' : can_snags_1_w,
                                    'snags class 1 no foliage' : can_snags1nf,
                                    'snags class 2' : can_snags_2,
                                    'snags class 3' : can_snags_3,
                                    'ladder fuels' : can_ladder},
                                'shrub' : {
                                    'primary live' : shb_prim_live,
                                    'primary dead' : shb_prim_dead,
                                    'secondary live' : shb_seco_live,
                                    'secondary dead' :  shb_seco_dead},
                                'nonwoody' : {
                                    'primary live' : nw_prim_live,
                                    'primary dead' : nw_prim_dead,
                                    'secondary live' : nw_seco_live,
                                    'secondary dead' :  nw_seco_dead},
                                'litter-lichen-moss' : {
                                    'litter' : llm_litter,
                                    'lichen' : llm_lichen,
                                    'moss' : llm_moss},
                                'ground fuels' : {
                                    'duff upper' : gf_duff_upper,
                                    'duff lower' : gf_duff_lower,
                                    'basal accumulations' : gf_ba,
                                    'squirrel middens' : gf_sm},
                                'woody fuels' : {
                                    'stumps sound' : wd_stumps_snd,
                                    'stumps rotten' : wd_stumps_rot,
                                    'stumps lightered' : wd_stumps_lgt,
                                    '1-hr fuels' : wd_hr1,
                                    '10-hr fuels' : wd_hr10,
                                    '100-hr fuels' : wd_hr100,
                                    '1000-hr fuels sound' : wd_hr1000_snd,
                                    '1000-hr fuels rotten' : wd_hr1000_rot,
                                    '10000-hr fuels sound' : wd_hr10000_snd,
                                    '10000-hr fuels rotten' : wd_hr10000_rot,
                                    '10k+-hr fuels sound' : wd_hr10kp_snd,
                                    '10k+-hr fuels rotten' : wd_hr10kp_rot},
                                'debug' : {
                                    'litter_bulk_density' : lit_mean_bd,
                                    'forest floor reduction' : ff_reduction}
                                    }}


    if len(emis_data) != 0:
        pm_emis = emis_dict(0, 0)
        pm10_emis = emis_dict(0, 1)
        pm25_emis = emis_dict(0, 2)
        co_emis = emis_dict(0, 3)
        co2_emis = emis_dict(0, 4)
        ch4_emis = emis_dict(0, 5)
        nmhc_emis = emis_dict(0, 6)

        pm_detail = emis_dict_detail(0)
        pm10_detail = emis_dict_detail(1)
        pm25_detail = emis_dict_detail(2)
        co_detail = emis_dict_detail(3)
        co2_detail = emis_dict_detail(4)
        ch4_detail = emis_dict_detail(5)
        nmhc_detail = emis_dict_detail(6)


        results['emissions'] = { 'pm' : pm_emis,
                                    'pm10' : pm10_emis,
                                    'pm25' : pm25_emis,
                                    'co' : co_emis,
                                    'co2' : co2_emis,
                                    'ch4' : ch4_emis,
                                    'nmhc' : nmhc_emis,
                                    'stratum' : {
                                        'pm' : pm_detail,
                                        'pm10' : pm10_detail,
                                        'pm25' : pm25_detail,
                                        'co' : co_detail,
                                        'co2' : co2_detail,
                                        'ch4' : ch4_detail,
                                        'nmhc' : nmhc_detail,}}

    return results


############################################################################
############################################################################

############################################################################
############################################################################


def _unpack(data, runlnk):
    """
    Unpacks unique scenarios into a data output that contains all scenarios
    """
    def trans(d):
        """ Transposes data """
        return d.transpose()

    def trans2(d):
        """ Transposes data again """
        return np.transpose(d)

    def trans3(d):
        """ Returns array of listed data """
        return np.array(d)

    dt = []
    cdtemp = []

    datat = trans(data)

    for run in runlnk:
        cdtemp.append(datat[run[1]])

    del datat
    cdtemp = trans2(cdtemp)

    for i in range(0, len(data)):
        dt.append(cdtemp[i])

    del cdtemp
    dt = trans3(dt)

    return dt


def unit_conversion(data, area, from_units, output_units):
    """
    Converts units b/t english and metric and b/t per units area and total.
    """

    undict = {'tons_ac' : 1,
              'lbs_ac' : 0.0005,
              'lbs' : 0.0005,
              'kg' : 0.00110231131,
              'kg_ha' : 0.0004460891,
              'kg_m^2' : 4.46089561,
              'kg_km^2' : 0.000004460891,
              'tonnes' : 1.10231131,
              'tonnes_ha' : 0.446089561,
              'tonnes_km^2' : 0.00446089561}

              #'from_tons' : {'tons_ac' : 1,
               #             'lbs_ac' : 2000.0,
                ##           'kg' : 907.18474,
                  #          'kg_ha' : 2241.70231,
                   #         'kg_m^2' : 0.224170231,
                    #        'kg_km^2' : 224170.231,
                     #       'tonnes' : 0.90718474,
                      #      'tonnes_ha' : 2.24170231,
                       #     'tonnes_km^2' : 224.170231}}"""

    if from_units == output_units:
        return [output_units, data]

    else:
        # Convert everything to tons right off the bat...
        cv = undict[from_units]

        data *= cv
        if from_units in dd.perarea():
            data *= area

        from_units = "tons"

        if output_units == 'tons':
            return [output_units, data]

        else:
            # And then perform whatever conversion necessary from there:
            data *= (1 / undict[output_units])
            if output_units in dd.perarea():
                 data /= area

            return [output_units, data]

# Repeated functions
def csdist(tot, csd):
    """Portions consumption by consumption stage"""
    return np.array([tot * csd[0], tot * csd[1], tot * csd[2], tot * sum(csd)])

def propcons(x):
    """ Equation to calculate proportion consumed for various strata"""
    return math.e ** (x) / (1 + math.e ** x)

#-------------------------------------------------------------------------------
#   For testing
#-------------------------------------------------------------------------------
def main():
    a = 42.3847781507
    b = 23.2962946918

    for i in ['tons_ac', 'lbs_ac', 'lbs', 'kg', 'kg_ha', 'kg_m^2', 'kg_km^2', 'tonnes', 'tonnes_ha', 'tonnes_km^2']:
        for j in ['tons_ac', 'lbs_ac', 'lbs', 'kg_ha', 'kg_m^2', 'kg_km^2', 'tonnes', 'tonnes_ha', 'tonnes_km^2']:
            print(unit_conversion(a, 100, i, j ))
            print(unit_conversion(b, 100, i, j))

if __name__ == '__main__':
    main()











