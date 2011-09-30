import math
import numpy as np
import util_consume as util

# Consumption calculation methods
def ccon_canopy(can_con_pct, LD):
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

    return [util.csdist(LD[t[0]] * pct, t[1]) for t in can_params]


def ccon_shrub(shrub_black_pct, LD):
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

        shb_cnsm_total = shb_load_total * util.propcons(z)

        # - this works correctly but still generates a warning, use the
        #   context manager to swallow the benign warning
        with np.errstate(divide='ignore', invalid='ignore'):
            nonzero_loading = np.not_equal(shb_load_total, 0.0)
            shb_prim_total = np.where(nonzero_loading,
                  shb_cnsm_total * (LD['shrub_prim'] / shb_load_total), 0.0)
            shb_seco_total = np.where(nonzero_loading,
                  shb_cnsm_total * (LD['shrub_seco'] / shb_load_total), 0.0)

        pctlivep = LD['shrub_prim_pctlv']
        pctdeadp = 1 - pctlivep
        pctlives = LD['shrub_seco_pctlv']
        pctdeads = 1 - pctlives

        return (util.csdist(shb_prim_total * pctlivep, csd_live),
                util.csdist(shb_prim_total * pctdeadp, csd_dead),
                util.csdist(shb_seco_total * pctlives, csd_live),
                util.csdist(shb_seco_total * pctdeads, csd_dead))
    else:
        hold = util.csdist(np.array([0.0] * len(LD['fccs_id']), dtype=float), [0.0, 0.0, 0.0])
        return hold, hold, hold, hold


def ccon_nw(LD):
    """ Nonwoody consumption, activity & natural, p.169 """

    nw_prim_total = LD['nw_prim'] * 0.9274
    nw_seco_total = LD['nw_seco'] * 0.9274

    csd_live = [0.95, 0.05, 0.0]
    csd_dead = [0.95, 0.05, 0.0]

    pctlivep = LD['nw_prim_pctlv']
    pctdeadp = 1 - pctlivep
    pctlives = LD['nw_seco_pctlv']
    pctdeads = 1 - pctlives

    return (util.csdist(nw_prim_total * pctlivep, csd_live),
            util.csdist(nw_prim_total * pctdeadp, csd_dead),
            util.csdist(nw_seco_total * pctlives, csd_live),
            util.csdist(nw_seco_total * pctdeads, csd_dead))


###################################################################
### LITTER LICHEN MOSS (LLM) CONSUMPTION - ACTIVITY and NATURAL ###
###################################################################
# p. 175 in the manual

def ccon_ffr(fm_duff, burn_type, ecoregion, LD):
    """ Forest-floor reduction calculation, p.177  """
    # total duff depth (inches)
    duff_depth = LD['duff_upper_depth'] + LD['duff_lower_depth']

    # total forest floor depth (inches)
    ff_depth = (duff_depth + LD['lit_depth'] +
                LD['lch_depth'] + LD['moss_depth'])
    y_b = 1.2383 - (0.0114 * fm_duff) # used to calc squirrel mid. redux

    ffr = np.array([])
    if 'activity' in burn_type:
        activity_duff_reduction = duff_redux_activity()
        ffr = (activity_duff_reduction / duff_depth) * ff_depth
    else:
        if 'boreal' in ecoregion:
            ffr = ff_depth * util.propcons(y_b)
        elif 'southern' in ecoregion:
            ffr = (-0.0061 * fm_duff) + (0.6179 * ff_depth)
            ffr = np.where(
                        np.less_equal(ffr, 0.25), # if ffr south <= .25
                        (0.006181 * math.e**(0.398983 * (ff_depth - # true
                        (0.00987 * (fm_duff-60.0))))), ffr) # false
        elif 'western' in ecoregion:
            y = -0.8085 - (0.0213 * fm_duff) + (1.0625 * ff_depth)
            ffr = ff_depth * util.propcons(y)
        else: assert False

    return [ffr, y_b, duff_depth]

def calc_and_reduce_ff(LD, key):
    # if the depth of the layer (LD[key]) is less than the available reduction
    #  use the depth of the layer. Otherwise, use the available reduction
    layer_reduction = np.where(LD[key] < LD['ff_reduction_successive'],
            LD[key], LD['ff_reduction_successive'])
    # reduce the available reduction by the calculated amount
    LD['ff_reduction_successive'] = LD['ff_reduction_successive'] - layer_reduction
    # should never be less than zero
    assert(0 == len(np.where(LD['ff_reduction_successive'] < 0)[0]))
    return layer_reduction

def ccon_lch(LD):
    """ Lichen consumption, activity & natural"""
    csd_lch = [0.95, 0.05, 0.00]
    lch_pretot = calc_and_reduce_ff(LD, 'lch_depth')
    lch_total = (lch_pretot * 0.5 * LD['lch_pctcv'])
    return util.csdist(lch_total, csd_lch)

def ccon_moss(LD):
    """ Moss consumption, activity & natural"""
    csd_moss = [0.95, 0.05, 0.00]
    moss_pretot = calc_and_reduce_ff(LD, 'moss_depth')
    moss_total = (moss_pretot * 1.5 * LD['moss_pctcv'])
    return util.csdist(moss_total, csd_moss)

def ccon_litter(LD):
    """ Litter consumption, activity & natural"""
    csd_lit = [0.90, 0.10, 0.00]
    lit_pretot = calc_and_reduce_ff(LD, 'lit_depth')
    mean_weighted_litterbd = ((LD['lit_s_ndl_pct'] * 3.0)
                        + (LD['lit_l_ndl_pct'] * 3.0)
                        + (LD['lit_o_ndl_pct'] * 3.0)
                        + (LD['lit_blf_d_pct'] * 1.5)
                        + (LD['lit_blf_e_pct'] * 1.5)
                        + (LD['lit_palm_pct'] * 0.3)
                        + (LD['lit_grass_pct'] * 0.5))
    LD['lit_mean_bd'] = mean_weighted_litterbd
    lit_total = (lit_pretot * LD['lit_pctcv'] * mean_weighted_litterbd)
    return util.csdist(lit_total, csd_lit)


################################
### Ground FUELS CONSUMPTION ###
################################
# p. 179-183 in the manual

def ccon_bas(LD, ff_redux_proportion):
    """ Basal accumulations consumption, activity & natural

     The following equations in the next 4 lines of code for basal
     accumulation consumption are NOT in the manual, but were derived
     from the source code and in consultation with Susan Prichard(USFS)
     an original developer of Consume 3.0.
    """
    csd_bas = [0.10, 0.40, 0.50]
##    # '43560' refers to the conversion factor from square feet to acres.
##    # '0.8333' refers to default tree radius (in ft, based on 20" diam)
##    bas_density = LD['bas_pct'] / 2.0 #<<< should pct be div by 100?
##    bas_area = np.maximum((
##                ((math.pi * (LD['bas_rad'] ** 2.0) / 43560.0) -
##                (math.pi * 0.8333 / 43560.0)) * bas_density), 0.0)
##    bas_total = (np.minimum(LD['bas_depth'], LD['ff_reduction'])
##                 * bas_area * 12.0)
##
##    return util.csdist(bas_total, csd_bas)
    bas_redux = ff_redux_proportion * LD['bas_depth']
    return util.csdist(bas_redux, csd_bas)



def ccon_sqm(LD, ff_redux_proportion):
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
##    y_b = 1.2383 - (0.0114 * fm_duff) # used to calc squirrel mid. redux
##    sqm_reduction = LD['sqm_depth'] * util.propcons(y_b) * ecob_mask
##    sqm_area = (LD['sqm_density'] * math.pi *
##                (LD['sqm_radius']**2.0) / 43560.0)
##    sqm_total = sqm_reduction * sqm_area * 12.0
##
##    return util.csdist(sqm_total, csd_sqm)
    sqm_redux = ff_redux_proportion * LD['sqm_depth']
    return util.csdist(sqm_redux, csd_sqm)


def ccon_duff(LD):
    """ Duff consumption, activity & natural*
        * note that there are different equations for activity/natural
          to calculate duff_reduction
    #   Refer to p. 181-184 in the 3.0 manual
    #   General equation:
    Consumption(tons/ac.) = Reduction(in.) * Bulk density(tons/acre-in.)
    """
    csd_duffu = [0.10, 0.70, 0.20]
    csd_duffl = [0.0, 0.20, 0.80]

    upperduff_pretot = calc_and_reduce_ff(LD, 'duff_upper_depth')
    duff_upper = np.maximum(upperduff_pretot * 8.0 * LD['duff_upper_pctcv'], 0.0)

    lowerduff_pretot = calc_and_reduce_ff(LD, 'duff_lower_depth')
    lo_total = lowerduff_pretot * LD['duff_lower_pctcv']

    bulk_dens = (np.where(np.equal(LD['duff_lower_deriv'], 3), 18.0, 0.0) +
                 np.where(np.equal(LD['duff_lower_deriv'], 4), 22.0, 0.0))
    duff_lower = np.maximum(lo_total * bulk_dens, 0.0)

    return (util.csdist(duff_upper, csd_duffu),
            util.csdist(duff_lower, csd_duffl))


##############################
### WOODY FUEL CONSUMPTION ###
##############################
# p. 169-175 in the manual

def ccon_stumps(LD):
    """ STUMP CONSUMPTION - ACTIVITY and NATURAL """
    stump_params = [['stump_sound', 0.10, [0.50, 0.50, 0.0]],
                    ['stump_rotten', 0.50, [0.10, 0.30, 0.60]],
                    ['stump_lightered', 0.50, [0.40, 0.30, 0.30]]]

    return [util.csdist(LD[s[0]] * s[1], s[2]) for s in stump_params]

### WOODY FUEL CONSUMPTION NATURAL EQUATIONS ###
def ccon_one_nat(LD):
    """ 1-hr (0 to 1/4"), natural """
    csd = [0.95, 0.05, 0.00]
    return util.csdist(LD['one_hr_sound'], csd)

def ccon_ten_nat(LD):
    """ 10-hr (1/4" to 1"), natural, p.169"""
    csd = [0.90, 0.10, 0.00]
    total = LD['ten_hr_sound'] * 0.8650
    return util.csdist(total, csd)

def ccon_hun_nat(ecos_mask, LD):
    """ 100-hr (1 to 3"), natural """
    csd = [0.85, 0.10, 0.05]
    total = np.where(
            np.equal(ecos_mask, 1),       # if southern ecoregion,
            LD['hun_hr_sound'] * 0.4022,    # true
            LD['hun_hr_sound'] * 0.7844)    # false
    return util.csdist(total, csd)

def ccon_oneK_snd_nat(fm_duff, fm_1000hr, ecos_mask, LD):
    """ 1000-hr (3 to 9") sound, natural """
    csd = [0.60, 0.30, 0.10]
    y = 0.0302 - (0.0379 * fm_duff)
    z = 3.1052 - (0.0559 * fm_1000hr)
    total = np.where(
           np.equal(ecos_mask, 1),      # if southern ecoregion,
           LD['oneK_hr_sound'] * util.propcons(y),   # true
           LD['oneK_hr_sound'] * util.propcons(z))   # false
    return util.csdist(total, csd)

def ccon_tenK_snd_nat(fm_1000hr, LD):
    """ 10K-hr (9 to 20") sound, natural """
    csd = [0.40, 0.40, 0.20]
    x = 0.7869 - (0.0387 * fm_1000hr)
    total = LD['tenK_hr_sound'] * util.propcons(x)
    return util.csdist(total, csd)

def ccon_tnkp_snd_nat(fm_1000hr, LD):
    """ 10K+ hr (>20") sound, natural """
    csd = [0.20, 0.40, 0.40]
    z = 0.3960 - (0.0389 * fm_1000hr)
    total = LD['tnkp_hr_sound'] * util.propcons(z)
    return util.csdist(total, csd)

def ccon_oneK_rot_nat(fm_duff, ecos_mask, LD):
    """ 1000-hr (3 to 9") rotten, natural """
    csd = [0.20, 0.30, 0.50]
    y = 4.0139 - (0.0600 * fm_duff) + (0.8341 * LD['oneK_hr_rotten'])
    z = 0.5052 - (0.0434 * fm_duff)
    total = np.where(np.equal(ecos_mask, 1),    # if southern ecoegion,
            LD['oneK_hr_rotten'] * util.propcons(z),     # true
            LD['oneK_hr_rotten'] * util.propcons(y))     # false
    return util.csdist(total, csd)

def ccon_tenK_rot_nat(fm_duff, LD):
    """ 10K-hr (9 to 20") rotten, natural """
    csd = [0.10, 0.30, 0.60]
    y = 2.1218 - (0.0438 * fm_duff)
    total = LD['tenK_hr_rotten'] * util.propcons(y)
    return util.csdist(total, csd)

def ccon_tnkp_rot_nat(fm_duff, LD):
    """ 10K+ hr (>20") rotten, natural """
    csd = [0.10, 0.30, 0.60]
    y = 0.8022 - (0.0266 * fm_duff)
    total = LD['tnkp_hr_rotten'] * util.propcons(y)
    return util.csdist(total, csd)


##        def duff_redux_natural(LD):
##            """ Duff reduction calculation, natural """
##
##            # total depth of litter, lichen, and moss layer, used in duff calc.
##            llm_depth = LD['lit_depth'] + LD['lch_depth'] + LD['moss_depth']
##
##            #Duff reduction equation (natural fuels):
##
##            #if llm_depth[n] >= duff_reduction:   #<<<EQUATIONS DOCUMENTATION
##            #if llm_depth[n] > duff_depth[n]:    #<<< USER'S GUIDE - SUSAN PRICHARD SAYS THIS IS THE CORRECT COMPARISON
##            #if llm_depth[n] >= ff_reduction[n]:  #<<< SOURCE CODE
##
##            # KS - if the duff_reduction value is greater than zero use it,
##            # otherwise, use zero.
##            duff_reduction_tmp = (LD['ff_reduction'] - llm_depth)
##            non_zero = duff_reduction_tmp > 0.0
##            return (duff_reduction_tmp * non_zero)
