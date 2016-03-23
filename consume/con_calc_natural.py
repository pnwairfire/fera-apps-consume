import math
import numpy as np
from . import util_consume as util
from . util_consume import values

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

    return [util.csdist(values(LD, t[0]) * pct, t[1]) for t in can_params]


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

    shb_load_total = values(LD, 'shrub_prim') + values(LD, 'shrub_seco')
    if sum(shb_load_total) > 0:

        z = -2.6573 + (0.0956 * shb_load_total) + (0.0473 * shrub_black_pct)

        shb_cnsm_total = shb_load_total * util.propcons(z)

        # - this works correctly but still generates a warning, use the
        #   context manager to swallow the benign warning
        with np.errstate(divide='ignore', invalid='ignore'):
            nonzero_loading = np.not_equal(shb_load_total, 0.0)
            shb_prim_total = np.where(nonzero_loading,
                  shb_cnsm_total * (values(LD, 'shrub_prim') / shb_load_total), 0.0)
            shb_seco_total = np.where(nonzero_loading,
                  shb_cnsm_total * (values(LD, 'shrub_seco') / shb_load_total), 0.0)

        pctlivep = values(LD, 'shrub_prim_pctlv')
        pctdeadp = 1 - pctlivep
        pctlives = values(LD, 'shrub_seco_pctlv')
        pctdeads = 1 - pctlives

        return (util.csdist(shb_prim_total * pctlivep, csd_live),
                util.csdist(shb_prim_total * pctdeadp, csd_dead),
                util.csdist(shb_seco_total * pctlives, csd_live),
                util.csdist(shb_seco_total * pctdeads, csd_dead))
    else:
        hold = util.csdist(np.array([0.0] * len(LD['fccs_id']), dtype=float), [0.0, 0.0, 0.0])
        return hold, hold, hold, hold

def shrub_calc(shrub_black_pct, loadings, ecoregion_masks):
    """ Shrub consumption, western, southern, activity """
    SEASON = 1
    MGHA_2_TONSAC = 0.44609
    def southern_cons(load):
        return (-0.1889 + 0.9049*(np.log(load)) + 0.0676 * SEASON) * MGHA_2_TONSAC

    def western_cons(load, shrub_black_pct):
        tmp_sqrt = (0.1102 + 0.1139*(load) + ((1.9647*shrub_black_pct) - (0.3296 * SEASON)))
        return (tmp_sqrt**tmp_sqrt) * MGHA_2_TONSAC
        #return (tmp_sqrt**2) * MGHA_2_TONSAC

    csd_live = [0.95, 0.05, 0.0]
    csd_dead = [0.90, 0.10, 0.0]

    shrub_load_total = values(loadings, 'shrub_prim') + values(loadings, 'shrub_seco')
    shrub_cons = np.zeros_like(shrub_load_total)
    if sum(shrub_load_total) > 0:
        shrub_cons = western_cons(shrub_load_total, 0.8)

        pctlivep = values(loadings, 'shrub_prim_pctlv')
        pctdeadp = 1 - pctlivep
        pctlives = values(loadings, 'shrub_seco_pctlv')
        pctdeads = 1 - pctlives

        # TODO: kjell, finish this!
        return shrub_cons

        '''
        return (util.csdist(shb_prim_total * pctlivep, csd_live),
                util.csdist(shb_prim_total * pctdeadp, csd_dead),
                util.csdist(shb_seco_total * pctlives, csd_live),
                util.csdist(shb_seco_total * pctdeads, csd_dead))
        '''
    else:
        hold = util.csdist(np.array([0.0] * len(loadings['fccs_id']), dtype=float), [0.0, 0.0, 0.0])
        return hold, hold, hold, hold


def ccon_nw(LD):
    """ Nonwoody consumption, activity & natural, p.169 """

    nw_prim_total = values(LD, 'nw_prim') * 0.9274
    nw_seco_total = values(LD, 'nw_seco') * 0.9274

    csd_live = [0.95, 0.05, 0.0]
    csd_dead = [0.95, 0.05, 0.0]

    pctlivep = values(LD, 'nw_prim_pctlv')
    pctdeadp = 1 - pctlivep
    pctlives = values(LD, 'nw_seco_pctlv')
    pctdeads = 1 - pctlives

    return (util.csdist(nw_prim_total * pctlivep, csd_live),
            util.csdist(nw_prim_total * pctdeadp, csd_dead),
            util.csdist(nw_seco_total * pctlives, csd_live),
            util.csdist(nw_seco_total * pctdeads, csd_dead))


###################################################################
### LITTER LICHEN MOSS (LLM) CONSUMPTION - ACTIVITY and NATURAL ###
###################################################################
# p. 175 in the manual

def ccon_ffr(fm_duff, ecoregion_masks, LD):
    """ Forest-floor reduction calculation, p.177  """

    # total duff depth (inches)
    duff_depth = values(LD, 'duff_upper_depth') + values(LD, 'duff_lower_depth')
    # total forest floor depth (inches)
    ff_depth = (duff_depth + values(LD, 'lit_depth') +
                values(LD, 'lch_depth') + values(LD, 'moss_depth'))

    # boreal
    y_b = 1.2383 - (0.0114 * fm_duff) # used to calc squirrel mid. redux
    ffr_boreal = ff_depth * util.propcons(y_b)

    # southern
    ffr_southern = (-0.0061 * fm_duff) + (0.6179 * ff_depth)
    ffr_southern = np.where(
                np.less_equal(ffr_southern, 0.25), # if ffr south <= .25
                (0.006181 * math.e**(0.398983 * (ff_depth - # true
                (0.00987 * (fm_duff-60.0))))),
                ffr_southern)                               # false

    # western
    y = -0.8085 - (0.0213 * fm_duff) + (1.0625 * ff_depth)
    ffr_western = ff_depth * util.propcons(y)

    ffr = ((ecoregion_masks['southern'] * ffr_southern) +
            (ecoregion_masks['boreal'] * ffr_boreal) +
            (ecoregion_masks['western'] * ffr_western))
    return [ffr, y_b, duff_depth]


def calc_and_reduce_ff(LD, ff_reduction, key):
    # if the depth of the layer (LD[key]) is less than the available reduction
    #  use the depth of the layer. Otherwise, use the available reduction
    layer_reduction = np.where(LD[key] < ff_reduction, LD[key], ff_reduction)
    # reduce the available reduction by the calculated amount
    ff_reduction -= layer_reduction
    # should never be less than zero
    assert 0 == len(np.where(ff_reduction < 0)[0]), "Error: Negative ff reduction found in calc_and_reduce_ff()"
    assert False == np.isnan(ff_reduction).any(), "Error: NaN found in calc_and_reduce_ff()"
    return layer_reduction

def ccon_forest_floor(LD, ff_reduction, key_depth, key_loading, csd):
    ''' Same procedure for litter, lichen, moss, upper and lower duff
    '''
    # - get per-layer reduction
    layer_reduction = calc_and_reduce_ff(LD, ff_reduction, key_depth)

    # - how much was it reduced relative to the layer depth
    proportional_reduction = np.where(LD[key_depth] > 0.0,
        layer_reduction / LD[key_depth], 0.0)

    total = proportional_reduction * values(LD, key_loading)
    return util.csdist(total, csd)


################################
### Ground FUELS CONSUMPTION ###
################################
# p. 179-183 in the manual

def ccon_bas(basal_loading, ff_redux_proportion):
    """ Basal accumulations consumption, activity & natural
    """
    csd_bas = [0.10, 0.40, 0.50]
    basal_consumption = np.array([])
    basal_consumption = basal_loading * ff_redux_proportion
    return util.csdist(basal_consumption, csd_bas)

def ccon_sqm(sqm_loading, ff_redux_proportion):
    """ Squirrel middens consumption, activity & natural
    """
    csd_sqm = [0.10, 0.30, 0.60]
    sqm_consumption = sqm_loading * ff_redux_proportion
    return util.csdist(sqm_consumption, csd_sqm)


##############################
### WOODY FUEL CONSUMPTION ###
##############################
# p. 169-175 in the manual

def ccon_stumps(LD):
    """ STUMP CONSUMPTION - ACTIVITY and NATURAL """
    stump_params = [['stump_sound', 0.10, [0.50, 0.50, 0.0]],
                    ['stump_rotten', 0.50, [0.10, 0.30, 0.60]],
                    ['stump_lightered', 0.50, [0.40, 0.30, 0.30]]]

    return [util.csdist(values(LD, s[0]) * s[1], s[2]) for s in stump_params]

def ccon_piles(pct_consumed, LD):
    """  pile loading appears as clean, dirty, and verydirty """
    # Flaming, smoldering, residual
    csd = [0.70, 0.15, 0.15]
    pct = pct_consumed * 0.01
    total_pile_loading = values(LD, 'pile_clean_loading') + values(LD, 'pile_dirty_loading') + values(LD, 'pile_vdirty_loading')
    total_consumed = pct * total_pile_loading
    return util.csdist(total_consumed, csd)

### WOODY FUEL CONSUMPTION NATURAL EQUATIONS ###
def ccon_one_nat(LD):
    """ 1-hr (0 to 1/4"), natural """
    csd = [0.95, 0.05, 0.00]
    return util.csdist(values(LD, 'one_hr_sound'), csd)

def ccon_ten_nat(LD):
    """ 10-hr (1/4" to 1"), natural, p.169"""
    csd = [0.90, 0.10, 0.00]
    total = values(LD, 'ten_hr_sound') * 0.8650
    return util.csdist(total, csd)

def ccon_hun_nat(ecos_mask, LD):
    """ 100-hr (1 to 3"), natural """
    csd = [0.85, 0.10, 0.05]
    total = np.where(
            np.equal(ecos_mask, 1),       # if southern ecoregion,
            values(LD, 'hun_hr_sound') * 0.4022,    # true
            values(LD, 'hun_hr_sound') * 0.7844)    # false
    return util.csdist(total, csd)

def ccon_oneK_snd_nat(fm_duff, fm_1000hr, ecos_mask, LD):
    """ 1000-hr (3 to 9") sound, natural """
    csd = [0.60, 0.30, 0.10]
    y = 0.0302 - (0.0379 * fm_duff)
    z = 3.1052 - (0.0559 * fm_1000hr)
    total = np.where(
           np.equal(ecos_mask, 1),      # if southern ecoregion,
           values(LD, 'oneK_hr_sound') * util.propcons(y),   # true
           values(LD, 'oneK_hr_sound') * util.propcons(z))   # false
    return util.csdist(total, csd)

def ccon_tenK_snd_nat(fm_1000hr, LD):
    """ 10K-hr (9 to 20") sound, natural """
    csd = [0.40, 0.40, 0.20]
    x = 0.7869 - (0.0387 * fm_1000hr)
    total = values(LD, 'tenK_hr_sound') * util.propcons(x)
    return util.csdist(total, csd)

def ccon_tnkp_snd_nat(fm_1000hr, LD):
    """ 10K+ hr (>20") sound, natural """
    csd = [0.20, 0.40, 0.40]
    z = 0.3960 - (0.0389 * fm_1000hr)
    total = values(LD, 'tnkp_hr_sound') * util.propcons(z)
    return util.csdist(total, csd)

def ccon_oneK_rot_nat(fm_duff, ecos_mask, LD):
    """ 1000-hr (3 to 9") rotten, natural """
    csd = [0.20, 0.30, 0.50]
    y = 4.0139 - (0.0600 * fm_duff) + (0.8341 * values(LD, 'oneK_hr_rotten'))
    z = 0.5052 - (0.0434 * fm_duff)
    total = np.where(np.equal(ecos_mask, 1),    # if southern ecoegion,
            values(LD, 'oneK_hr_rotten') * util.propcons(z),     # true
            values(LD, 'oneK_hr_rotten') * util.propcons(y))     # false
    return util.csdist(total, csd)

def ccon_tenK_rot_nat(fm_duff, LD):
    """ 10K-hr (9 to 20") rotten, natural """
    csd = [0.10, 0.30, 0.60]
    y = 2.1218 - (0.0438 * fm_duff)
    total = values(LD, 'tenK_hr_rotten') * util.propcons(y)
    return util.csdist(total, csd)

def ccon_tnkp_rot_nat(fm_duff, LD):
    """ 10K+ hr (>20") rotten, natural """
    csd = [0.10, 0.30, 0.60]
    y = 0.8022 - (0.0266 * fm_duff)
    total = values(LD, 'tnkp_hr_rotten') * util.propcons(y)
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
