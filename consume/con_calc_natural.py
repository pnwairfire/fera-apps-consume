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

def multi_layer_calc(loadings, ecoregion_masks, primary, secondary, primary_pct_live, secondary_pct_live, calculator):
    ''' This function is called by both the shrub and herb calculators. The general tasks are handled
        here, and the specific setup is done in the respective calling functions
    '''
    # determine primary and secondary percentages, replace nan value with zeros
    total_load = values(loadings, primary) + values(loadings, secondary)
    primary_pct = values(loadings, primary) / total_load
    primary_pct = np.where(np.isnan(primary_pct), 0, primary_pct)
    secondary_pct = 1.0 - primary_pct
    secondary_pct = np.where(np.isnan(secondary_pct), 0, secondary_pct)

    if total_load.any():  # any positive totals
        cons = np.where(total_load > 0,
            np.where(ecoregion_masks['southern'],   # for southern use southern, everything else is western
                calculator.southern_cons(total_load),
                calculator.western_cons(total_load)), 0)

        primary_total = cons * primary_pct
        secondary_total = cons * secondary_pct
        assert np.isnan(primary_total).any() == False, '{}'.format(primary_pct)
        assert np.isnan(secondary_total).any() == False, '{}'.format(secondary_total)

        pctlivep = values(loadings, primary_pct_live)
        pctdeadp = 1.0 - pctlivep
        pctlives = values(loadings, secondary_pct_live)
        pctdeads = 1.0 - pctlives

        csd_live = [0.95, 0.05, 0.0]
        csd_dead = [0.90, 0.10, 0.0]

        return (util.csdist(primary_total * pctlivep, csd_live),
                util.csdist(primary_total * pctdeadp, csd_dead),
                util.csdist(secondary_total * pctlives, csd_live),
                util.csdist(secondary_total * pctdeads, csd_dead))
    else:
        hold = util.csdist(np.array([0.0] * len(loadings['fccs_id']), dtype=float), [0.0, 0.0, 0.0])
        return hold, hold, hold, hold

CVT_MGHA = 0.44609
def to_mgha(tons):
    return tons / CVT_MGHA

def to_tons(mgha):
    return mgha * CVT_MGHA

def shrub_calc(shrub_black_pct, loadings, ecoregion_masks):
    """ Shrub consumption, western, southern, activity """
    def get_calculator(shrub_black_pct):
        class Calculator(object):
            SEASON = 1
            MGHA_2_TONSAC = 0.4461

            def __init__(self, shrub_black_pct):
                self._shrub_black_pct = shrub_black_pct

            def southern_cons(self, load):
                tmp = np.e ** (-0.1889 + (0.9049 * np.log(to_mgha(load)) + 0.0676 * Calculator.SEASON))
                return to_tons(tmp)

            def western_cons(self, load):
                tmp = (0.1102 + 0.1139 * to_mgha(load)
                            + ((1.9647 * self._shrub_black_pct) - (0.3296 * Calculator.SEASON)))
                return to_tons(tmp ** tmp)

        return Calculator(shrub_black_pct)

    return multi_layer_calc(loadings, ecoregion_masks,
                'shrub_prim', 'shrub_seco', 'shrub_prim_pctlv', 'shrub_seco_pctlv', get_calculator(shrub_black_pct))

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

def herb_calc(loadings, ecoregion_masks):
    """ Herbaceous consumption, activity & natural, p.169 """
    def get_calculator(shrub_black_pct):
        class Calculator(object):
            def southern_cons(load):
                return load * 0.9713
            
            def western_cons(load):
                return load * 0.9274
            
        return Calculator()

    return multi_layer_calc(loadings, ecoregion_masks,
                            'nw_prim', 'nw_seco', 'nw_prim_pctlv', 'nw_seco_pctlv',
                            get_calculator(nw_black_pct))


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

def litter_calc(loadings, fm_duff, fm_1000, ecoregion_masks):
    def southern_cons(load, fm_1000):
        return 0.7428*load - 0.0013*fm_1000

    def western_cons(load, fm_duff):
        #assert False, '{}\n{}'.format(load, fm_duff)
        return 0.6804*load - 0.007*fm_duff

    def boreal_cons(load, fm_duff):
        return 0.9794*load - 0.0281*fm_duff

    litter_load = values(loadings, 'litter_loading')
    #assert False, fm_1000
    cons = np.where(litter_load > 0,
        np.where(ecoregion_masks['southern'],
            southern_cons(litter_load, fm_1000/100),
            np.where(ecoregion_masks['western'],
                western_cons(litter_load, fm_duff/100), boreal_cons(litter_load, fm_duff/100))), 0)

    return cons

def duff_calc(loadings, fm_duff, fm_litter, ecoregion_masks):
    def southern_cons(load, fm_litter):
        return 0.7428*load - 0.0013*fm_litter

    def western_cons(load, fm_duff):
        #assert False, '{}\n{}'.format(load, fm_duff)
        return 0.1288*load - 0.0267*fm_duff

    # No good model - use western?
    #def boreal_cons(load, fm_duff):
    #    return 0.5845*load - 0.0917*fm_duff

    duff_load_total = values(loadings, 'duff_upper_loading') + values(loadings, 'duff_lower_loading')
    #assert False, fm_1000
    cons = np.where(duff_load_total > 0,
        np.where(ecoregion_masks['southern'],
            southern_cons(duff_load_total, fm_litter/100),
            np.where(ecoregion_masks['western'],
                western_cons(duff_load_total, fm_duff/100), boreal_cons(litter_load, fm_duff/100))), 0)

    return cons




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

def sound_one_nat(LD):
    """ 1-hr (0 to 1/4"), natural """
    # ks - this is unchanged based on Susan's spreadsheet, although the modeling
    #  indicated a fraction, not all, is consumed
    csd = [0.95, 0.05, 0.00]
    return util.csdist(values(LD, 'one_hr_sound'), csd)

def ccon_ten_nat(LD):
    """ 10-hr (1/4" to 1"), natural, p.169"""
    csd = [0.90, 0.10, 0.00]
    total = values(LD, 'ten_hr_sound') * 0.8650
    return util.csdist(total, csd)

def sound_ten_nat(LD):
    """ 10-hr (1/4" to 1"), natural, p.169"""
    csd = [0.90, 0.10, 0.00]
    total = values(LD, 'ten_hr_sound') * 0.8469
    return util.csdist(total, csd)

def ccon_hun_nat(ecos_mask, LD):
    """ 100-hr (1 to 3"), natural """
    csd = [0.85, 0.10, 0.05]
    total = np.where(
            np.equal(ecos_mask, 1),       # if southern ecoregion,
            values(LD, 'hun_hr_sound') * 0.4022,    # true
            values(LD, 'hun_hr_sound') * 0.7844)    # false
    return util.csdist(total, csd)

def sound_hundred_nat(loadings, ecos_mask):
    """ 100-hr (1 to 3"), natural """
    csd = [0.85, 0.10, 0.05]
    total = np.where(
            np.equal(ecos_mask, 1),       # if southern ecoregion,
            values(loadings, 'hun_hr_sound') * 0.5725,    # true
            values(loadings, 'hun_hr_sound') * 0.7127)    # false
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

def sound_large_wood(loadings, fm_1000, ecos_mask):
    def western_cons(load, fm_1000):
        return 2.735 + 0.3285*load - 0.0457*fm_1000

    sound_wood_columns = ['oneK_hr_sound', 'tenK_hr_sound', 'tnkp_hr_sound']
    total = sum([values(loadings, col) for col in sound_wood_columns])

    # ks - is this correct?
    csd = [0.60, 0.30, 0.10]
    cons = western_cons(total, fm_1000)

    return util.csdist(cons, csd)


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

