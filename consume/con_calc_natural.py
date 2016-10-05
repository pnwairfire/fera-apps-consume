import math
import numpy as np
from . import util_consume as util
from . util_consume import values

def bracket(load, cons):
    # ensure that results are between 0 and initial load value)
    return np.where(0 > cons, 0, np.where(cons > load, load, cons))


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

SEASON_SPRING = 1
SEASON_ALL_OTHER = 0

def shrub_calc(shrub_black_pct, loadings, ecoregion_masks, season=SEASON_ALL_OTHER):
    """ Shrub consumption, western, southern, activity """
    def get_calculator(shrub_black_pct, season):
        class Calculator(object):
            def __init__(self, shrub_black_pct, season):
                self._shrub_black_pct = shrub_black_pct
                self._season = season

            def southern_cons(self, load):
                tmp = np.e ** (-0.1889 + (0.9049 * np.log(to_mgha(load)) + 0.0676 * self._season))
                return to_tons(tmp)

            def western_cons(self, load):
                tmp = (0.1102 + 0.1139 * to_mgha(load)
                            + ((1.9647 * self._shrub_black_pct) - (0.3296 * self._season)))
                return to_tons(tmp**tmp)

        return Calculator(shrub_black_pct, season)

    return multi_layer_calc(loadings, ecoregion_masks,
                'shrub_prim', 'shrub_seco', 'shrub_prim_pctlv', 'shrub_seco_pctlv',
                get_calculator(shrub_black_pct, season))

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
def litter_calc(loadings, fm_duff, fm_1000, ecoregion_masks):
    def boreal_cons(load, fm_duff):
        return 0.9794*load - 0.0281*fm_duff
        
    def southern_cons(load):
        return 0.6918*load

    def western_cons(load, fm_duff):
        #assert False, '{}\n{}'.format(load, fm_duff)
        return 0.6804*load - 0.007*fm_duff

    litter_load = values(loadings, 'litter_loading')
    #assert False, fm_1000
    cons = np.where(litter_load > 0,
        np.where(ecoregion_masks['southern'],
            southern_cons(litter_load),
            np.where(ecoregion_masks['western'],
                western_cons(litter_load, fm_duff/100), boreal_cons(litter_load, fm_duff/100))), 0)

    return cons

def duff_calc(loadings, fm_duff, fm_litter, ecoregion_masks):
    def southern_cons(load, fm_litter):
        return 2.9711 + load*0.0702 + fm_litter*-0.1715

    def western_cons(load, fm_duff):
        #assert False, '{}\n{}'.format(load, fm_duff)
        return 0.6456*load - 0.0969*fm_duff

    # No good model - use western?
    def boreal_cons(load, fm_duff):
        return western_cons(load, fm_duff)

    duff_load_total = values(loadings, 'duff_upper_loading') + values(loadings, 'duff_lower_loading')
    cons = np.where(duff_load_total > 0,
        np.where(ecoregion_masks['southern'],
            southern_cons(duff_load_total, fm_litter/100),
            np.where(ecoregion_masks['western'],
                western_cons(duff_load_total, fm_duff/100), boreal_cons(duff_load_total, fm_duff/100))), 0)

    return cons
    
def proportion_of_other_calc(loadings, proportion, flame_smolder_resid):
    cons = loadings * proportion_of_other_calc
    return util.csdist(cons, flame_smolder_resid)



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

def stump_calc(LD):
    """ STUMP CONSUMPTION - ACTIVITY and NATURAL """
    stump_params = [['stump_sound', 0.10, [0.50, 0.50, 0.0]],
                    ['stump_rotten', 0.50, [0.10, 0.30, 0.60]],
                    ['stump_lightered', 0.50, [0.40, 0.30, 0.30]]]

    return [util.csdist(values(LD, s[0]) * s[1], s[2]) for s in stump_params]

def pile_calc(pct_consumed, LD):
    """  pile loading appears as clean, dirty, and verydirty """
    # Flaming, smoldering, residual
    csd = [0.70, 0.15, 0.15]
    pct = pct_consumed * 0.01
    total_pile_loading = values(LD, 'pile_clean_loading') + values(LD, 'pile_dirty_loading') + values(LD, 'pile_vdirty_loading')
    total_consumed = pct * total_pile_loading
    return util.csdist(total_consumed, csd)

### WOODY FUEL CONSUMPTION NATURAL EQUATIONS ###
def sound_one_calc(LD):
    """ 1-hr (0 to 1/4"), natural """
    # ks - this is unchanged based on Susan's spreadsheet, although the modeling
    #  indicated a fraction, not all, is consumed
    csd = [0.95, 0.05, 0.00]
    return util.csdist(values(LD, 'one_hr_sound'), csd)

def sound_ten_calc(LD):
    """ 10-hr (1/4" to 1"), natural, p.169"""
    csd = [0.90, 0.10, 0.00]
    total = values(LD, 'ten_hr_sound') * 0.8469
    return util.csdist(total, csd)

def sound_hundred_calc(loadings, ecos_mask):
    """ 100-hr (1 to 3"), natural """
    csd = [0.85, 0.10, 0.05]
    total = np.where(
            np.equal(ecos_mask, 1),       # if southern ecoregion,
            values(loadings, 'hun_hr_sound') * 0.5725,    # true
            values(loadings, 'hun_hr_sound') * 0.7127)    # false
    return util.csdist(total, csd)

def sound_large_wood_calc(loadings, fm_1000, ecos_mask):
    def western_cons(load, fm_1000):
        return 2.735 + 0.3285*load - 0.0457*fm_1000

    sound_wood_columns = ['oneK_hr_sound', 'tenK_hr_sound', 'tnkp_hr_sound']
    total = sum([values(loadings, col) for col in sound_wood_columns])

    # ks - is this correct?
    csd = [0.60, 0.30, 0.10]
    cons = western_cons(total, fm_1000)

    return util.csdist(cons, csd)

def rotten_large_wood_calc(loadings, fm_1000, ecos_mask):
    def western_cons(load, fm_1000):
        return 1.9024 + 0.4933*load - 0.0338*fm_1000

    sound_wood_columns = ['oneK_hr_rotten', 'tenK_hr_rotten', 'tnkp_hr_rotten']
    total = sum([values(loadings, col) for col in sound_wood_columns])

    # ks - is this correct?
    csd = [0.60, 0.30, 0.10]
    cons = western_cons(total, fm_1000)
    cons = bracket(total, cons)

    return util.csdist(cons, csd)
