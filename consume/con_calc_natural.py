import math
import numpy as np
from . import util_consume as util
from . util_consume import values

def bracket(load, cons):
    # ensure that results are between 0 and initial load value)
    return np.where(0 > cons, 0, np.where(cons > load, load, cons))


# Consumption calculation methods
def ccon_canopy(can_con_pct, LD):
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

def multi_layer_calc(loadings, ecoregion_masks, primary, secondary, calculator):
    ''' This function is called by both the shrub and herb calculators. The general tasks are handled
        here, and the specific setup is done in the respective calling functions
    '''
    # determine primary and secondary percentages
    total_load = values(loadings, primary) + values(loadings, secondary)
    #print('total_load has nan - {}'.format(np.isnan(total_load).any()))
    with np.errstate(invalid='ignore', divide='ignore'):
        primary_pct = np.where(total_load > 0, values(loadings, primary) / total_load, 0)
    secondary_pct = 1.0 - primary_pct
    assert(not np.isnan(secondary_pct).all())

    if total_load.any():  # any positive totals
        cons = np.where(total_load > 0,
            np.where(ecoregion_masks['southern'],   # for southern use southern, everything else is western
                calculator.southern_cons(total_load),
                calculator.western_cons(total_load)), 0)
        cons = bracket(total_load, cons)

        primary_total = cons * primary_pct
        secondary_total = cons * secondary_pct
        assert np.isnan(primary_total).any() == False, '{}'.format(primary_pct)
        assert np.isnan(secondary_total).any() == False, '{}'.format(secondary_total)

        fsr = [0.90, 0.10, 0.0]

        return (util.csdist(primary_total, fsr), util.csdist(secondary_total, fsr))
    else:
        hold = util.csdist(np.array([0.0] * len(loadings['fccs_id']), dtype=float), [0.0, 0.0, 0.0])
        return hold, hold

CVT_MGHA_TO_TONS = 0.44609
CVT_TONS_TO_MGHA = 1.0 / CVT_MGHA_TO_TONS

def to_mgha(tons):
    return tons * CVT_TONS_TO_MGHA

def to_tons(mgha):
    return mgha * CVT_MGHA_TO_TONS

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
                with np.errstate(invalid='ignore', divide='ignore'):
                    tmp = np.where(load > 0, np.e ** (-0.1889 + (0.9049 * np.log(to_mgha(load)) + 0.0676 * self._season)), 0)
                return to_tons(tmp)

            def western_cons(self, load):
                tmp = (0.1102 + (0.1139*to_mgha(load)) + 1.9647*self._shrub_black_pct - 0.3296*self._season)
                return to_tons(tmp*tmp)

        return Calculator(shrub_black_pct, season)

    return multi_layer_calc(loadings, ecoregion_masks,
                'shrub_prim', 'shrub_seco', get_calculator(shrub_black_pct/100, season))

def herb_calc(loadings, ecoregion_masks):
    """ Herbaceous consumption, activity & natural, p.169 """
    def get_calculator():
        class Calculator(object):
            def southern_cons(self, load):
                return load * 0.9713
            
            def western_cons(self, load):
                return load * 0.9274
            
        return Calculator()

    return multi_layer_calc(loadings, ecoregion_masks, 'nw_prim', 'nw_seco', get_calculator())


###################################################################
### LITTER LICHEN MOSS (LLM) CONSUMPTION - ACTIVITY and NATURAL ###
###################################################################
def southern_cons_litter(load):
    return 0.6918*load

def western_cons_litter(load, fm_duff):
    # mgha dependent equation: return 0.6804*load - 0.007*fm_duff
    return 0.6804*load - 0.00312263*fm_duff

FSR_PROP_LITTER = [0.9, 0.1, 0.0]        
def litter_calc(loadings, fm_duff, fm_1000, ecoregion_masks):
    
    load = values(loadings, 'litter_loading')
    cons = np.where(load > 0,
        np.where(ecoregion_masks['southern'],
            southern_cons_litter(load),
            western_cons_litter(load, fm_duff)),
            0)
                
    cons = bracket(load, cons)
    with np.errstate(invalid='ignore', divide='ignore'):
        proportion_consumed = np.where(load > 0, cons / load, 0)
    
    return util.csdist(cons, FSR_PROP_LITTER), proportion_consumed
    
def use_proportional_litter_cons(loadings, fsr_prop,
        fm_duff, fm_litter, ecoregion_masks, proportional_consumption):
    cons = np.where(loadings > 0,
        np.where(proportional_consumption > 0,
            loadings * proportional_consumption,
        np.where(ecoregion_masks['southern'],
            southern_cons_litter(loadings),
            western_cons_litter(loadings, fm_duff))),
        0)
    cons = bracket(loadings, cons)
    return util.csdist(cons, fsr_prop)
    
def lichen_calc(loadings, fm_duff, fm_litter, ecoregion_masks, proportion_litter_consumed):
    lichen_load = values(loadings, 'lichen_loading')
    return use_proportional_litter_cons(lichen_load,
            [0.95, 0.05, 0.0], fm_duff, fm_litter, ecoregion_masks, proportion_litter_consumed)
    
def moss_calc(loadings, fm_duff, fm_litter, ecoregion_masks, proportion_litter_consumed):
    moss_load = values(loadings, 'moss_loading')
    return use_proportional_litter_cons(moss_load,
            [0.95, 0.05, 0.0], fm_duff, fm_litter, ecoregion_masks, proportion_litter_consumed)
    
def southern_cons_duff(load, fm_litter):
    # mgha dependent equation: return 2.9711 + load*0.0702 + fm_litter*-0.1715
    return 1.3254 + load*0.0702 + fm_litter*-0.0765

def western_cons_duff(load, fm_duff):
    #mgha dependent equation: return 0.6456*load - 0.0969*fm_duff
    return 0.6456*load - 0.0432*fm_duff

def duff_calc(loadings, fm_duff, fm_litter, ecoregion_masks, duff_pct_available):
    duff_load_total = values(loadings, 'duff_upper_loading') + values(loadings, 'duff_lower_loading')
    
    pct = (duff_pct_available/100.0)

    duff_load_total_adjusted = values(loadings, 'duff_upper_loading')*(pct) + values(loadings, 'duff_lower_loading')*(pct)

    cons = np.where(duff_load_total_adjusted > 0,
        np.where(ecoregion_masks['southern'],
            southern_cons_duff(duff_load_total_adjusted, fm_litter),
            western_cons_duff(duff_load_total_adjusted, fm_duff)), 0)
    
    cons = bracket(duff_load_total_adjusted, cons)
    # calculate proportion_consumed based on non-adjusted duff_load_total
    # otherwise would probably over estimate consumption of basal and squirrel middens
    with np.errstate(invalid='ignore', divide='ignore'):
        proportion_consumed = np.where(duff_load_total > 0, cons / duff_load_total, 0)
    
    # consume the available upper duff first, remainder is from available lower duff
    cons_duff_upper = np.where(cons > values(loadings, 'duff_upper_loading')*(pct), 
        values(loadings, 'duff_upper_loading')*(pct), cons)
    cons_duff_lower = np.where(cons > values(loadings, 'duff_upper_loading')*(pct), 
        (cons - values(loadings, 'duff_upper_loading')*(pct)), 0)
    assert(np.all(cons_duff_lower >= 0))
    
    return util.csdist(cons_duff_upper, [0.1, 0.7, 0.2]), util.csdist(cons_duff_lower, [0, 0.2, 0.8]), proportion_consumed



################################
### Ground FUELS CONSUMPTION ###
################################
# todo: duplicate, pull into common include file    
FSR_PROP_BAS_ACC = [0.10, 0.40, 0.50]
FSR_PROP_SQ_MID = [0.10, 0.30, 0.60]

def use_proportional_duff_cons(loadings, fsr_prop,
        fm_duff, fm_litter, ecoregion_masks, proportional_duff_consumption):
    cons = np.where(loadings > 0,
        np.where(proportional_duff_consumption > 0,
            loadings * proportional_duff_consumption,
        np.where(ecoregion_masks['southern'],
            southern_cons_duff(loadings, fm_litter),
            western_cons_duff(loadings, fm_duff))),
        0)
    cons = bracket(loadings, cons)
    return util.csdist(cons, fsr_prop)

def basal_accumulation_calc(loadings, fm_duff, fm_litter, ecoregion_masks, proportional_duff_consumption):
    basal_load = values(loadings, 'bas_loading')
    return use_proportional_duff_cons(
        basal_load, FSR_PROP_BAS_ACC, fm_duff, fm_litter, ecoregion_masks, proportional_duff_consumption)
    
def squirrel_midden_calc(loadings, fm_duff, fm_litter, ecoregion_masks, proportional_duff_consumption):
    sq_mid_load = values(loadings, 'sqm_loading')
    return use_proportional_duff_cons(
        sq_mid_load, FSR_PROP_SQ_MID, fm_duff, fm_litter, ecoregion_masks, proportional_duff_consumption)


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
def sound_one_calc(loadings, ecos_mask):
    """ 1-hr (0 to 1/4"), natural """
    csd = [0.95, 0.05, 0.00]
    total = np.where(
            np.equal(ecos_mask, 1),       # if southern ecoregion,
            values(loadings, 'one_hr_sound') * 0.8259,    # true
            values(loadings, 'one_hr_sound') * 0.8469)    # false
    return util.csdist(total, csd)

def sound_ten_calc(loadings, ecos_mask):
    """ 10-hr (1/4" to 1"), natural, p.169"""
    csd = [0.90, 0.10, 0.00]
    total = np.where(
            np.equal(ecos_mask, 1),       # if southern ecoregion,
            values(loadings, 'ten_hr_sound') * 0.3727,    # true
            values(loadings, 'ten_hr_sound') * 0.8469)    # false
    return util.csdist(total, csd)

def sound_hundred_calc(loadings, ecos_mask):
    """ 100-hr (1 to 3"), natural """
    csd = [0.85, 0.10, 0.05]
    total = np.where(
            np.equal(ecos_mask, 1),       # if southern ecoregion,
            values(loadings, 'hun_hr_sound') * 0.5725,    # true
            values(loadings, 'hun_hr_sound') * 0.7127)    # false
    return util.csdist(total, csd)

TIMELAG_RATIO_SOUND_WOOD_1K = 0.5    
TIMELAG_RATIO_SOUND_WOOD_10K = 0.3    
TIMELAG_RATIO_SOUND_WOOD_10K_PLUS = 0.2    
def sound_large_wood_calc(loadings, fm_1000, sound_cwd_pct_available):
    pct = (sound_cwd_pct_available/100.0)
    sound_wood_columns = ['oneK_hr_sound', 'tenK_hr_sound', 'tnkp_hr_sound']
    total_swload = sum([values(loadings, col)*pct for col in sound_wood_columns])

    # mgha dependent: cons_total = 2.735 + 0.3285*total_swload - 0.0457*fm_1000
    cons_total = 1.2201 + 0.3285*total_swload - 0.0203863*fm_1000
    
    onek_load = loadings['oneK_hr_sound']
    tenk_load = loadings['tenK_hr_sound']
    tenk_plus_load = loadings['tnkp_hr_sound']
    
    ideal_onek = onek_load * TIMELAG_RATIO_SOUND_WOOD_1K
    ideal_tenk = tenk_load * TIMELAG_RATIO_SOUND_WOOD_10K
    ideal_tenk_plus = tenk_plus_load * TIMELAG_RATIO_SOUND_WOOD_10K_PLUS
    ideal_sw_total = ideal_onek + ideal_tenk + ideal_tenk_plus
    
    # determine a correction factor based on the relationship of the ideal total to the 
    #  calculated consumption (done on a single loading value)
    correction = np.where(ideal_sw_total > 0, cons_total/ideal_sw_total, 0)
    
    one_k_cons = bracket(onek_load, ideal_onek * correction)
    ten_k_cons = bracket(tenk_load, ideal_tenk * correction)
    ten_k_plus_cons = bracket(tenk_plus_load, ideal_tenk_plus * correction)
    
    return (util.csdist(one_k_cons, [.6, .3, .1]),
            util.csdist(ten_k_cons, [.4, .4, .2]),
            util.csdist(ten_k_plus_cons, [.2, .4, .4]))    

TIMELAG_RATIO_ROTTEN_WOOD_1K = 0.47    
TIMELAG_RATIO_ROTTEN_WOOD_10K = 0.33   
TIMELAG_RATIO_ROTTEN_WOOD_10K_PLUS = 0.2    
def rotten_large_wood_calc(loadings, fm_1000, rotten_cwd_pct_available):
    pct = (rotten_cwd_pct_available/100.0)
    rotten_wood_columns = ['oneK_hr_rotten', 'tenK_hr_rotten', 'tnkp_hr_rotten']
    total_rload = sum([values(loadings, col)*pct for col in rotten_wood_columns])
    
    # mgha dependent: cons_total = 1.9024 + 0.4933*load - 0.0338*fm_1000
    cons_total =  0.848641616 + 0.4933*total_rload - 0.015077842*fm_1000
    
    onek_load = loadings['oneK_hr_rotten']
    tenk_load = loadings['tenK_hr_rotten']
    tenk_plus_load = loadings['tnkp_hr_rotten']
    
    ideal_onek = onek_load * TIMELAG_RATIO_ROTTEN_WOOD_1K
    ideal_tenk = tenk_load * TIMELAG_RATIO_ROTTEN_WOOD_10K
    ideal_tenk_plus = tenk_plus_load * TIMELAG_RATIO_ROTTEN_WOOD_10K_PLUS
    ideal_rw_total = ideal_onek + ideal_tenk + ideal_tenk_plus
    
    # determine a correction factor based on the relationship of the ideal total to the 
    #  calculated consumption (done on a single loading value)
    correction = np.where(ideal_rw_total > 0, cons_total/ideal_rw_total, 0)
    
    one_k_cons = bracket(onek_load, ideal_onek * correction)
    ten_k_cons = bracket(tenk_load, ideal_tenk * correction)
    ten_k_plus_cons = bracket(tenk_plus_load, ideal_tenk_plus * correction)
    
    return (util.csdist(one_k_cons, [.2, .3, .5]),
            util.csdist(ten_k_cons, [.1, .3, .6]),
            util.csdist(ten_k_plus_cons, [.1, .3, .6]))    




















