import math
import numpy as np
import util_consume as util
# "global"s

# quadratic mean diameters: [hun, oneK, tenK, tnkp]
QMDs = [1.68, 5.22, 12.10, 25.00]
cdic = {
  'spring' : {"MEAS-Th" : [-0.097, 4.747],  # spring-like
        "ADJ-Th" : [-0.096, 4.6495],
        "NFDRS-Th" : [-0.120 / 1.4, 4.305]},
  'summer' : {"MEAS-Th" : [-0.108, 5.68],   # summer-like
        "ADJ-Th" : [-0.1251, 6.27],
        "NFDRS-Th" : [-0.150 / 1.4, 5.58]},
  'adj' : {"MEAS-Th" : 1.0,            # for the <0.5 adj
        "ADJ-Th" : 1.0,
        "NFDRS-Th" : 1.4}}

### WOODY FUEL CONSUMPTION ACTIVITY EQUATIONS ###
def pct_hun_hr_calc(windspeed, slope, fm_10hr, LD):
    """ Calculate % of 100-hour fuels consumed, p. 142, ln 4541 """

    # Eq. A: Default 100-hr load
    hun_hr_def = 4.8

    # Eq. B: Heat flux correction, ln 4557
    heat_flux_crx = ((LD['hun_hr_sound'] / hun_hr_def) *
                           (1.0 + ((slope - 20.0)/60.0) +
                           (windspeed / 4.0)))

    #"(%) 3.0% (amount of change in moisture content for each
    # doubling of flux [Rothermel 1972])
    fm_flux = 3.0

    # Eq. C: 10-hr fuel moisture correction
    fm_10hr_correction = np.where(
              np.equal(heat_flux_crx, 0.0),
              0.0,
              fm_flux * (np.log(heat_flux_crx) / math.log(2.0)))

    # Eq. D: Adjusted 10-hr fuel moisture content, p. 143, ln 4563
    adj_fm_10hr = fm_10hr - fm_10hr_correction

    # Eq. E: Percentage consumption of 100-hr fuels, ln 4564
    return np.clip(np.where(
            np.less(adj_fm_10hr, 26.7),   # if adj10hrFM < 26.7,
            0.9 - (adj_fm_10hr - 12.0) * 0.0535,       # true
            (-169.08 - (adj_fm_10hr * 18.393) -  # false
            (((adj_fm_10hr)**2) * 0.6646) +
            (((adj_fm_10hr)**3) * 0.00798)) *
            np.less_equal(adj_fm_10hr, 29.3)), # mask out > 29.3%
            0.0,1.0) # clip range to 0-1

def final1000hr(fm_1000hr, fm_type):
    """Eq. G: Evaluating if curing has occurred, p.146-7
    ln 5009 -> according to source code, this analysis is not
    included- a relic of Consume 2.1. """
   #uncured_FM = 119.64 * (math.e ** (-0.0069 * snow_free_days))
   # 'DRED_FM'='diameter reduction fuel moisture'
   #DRED_FM = np.where(np.greater(uncured_FM, fm_1000hr),
   #         uncured_FM,
   #         fm_1000hr)
    #return np.where(np.greater(DRED_FM, 60.0), uncured_FM, DRED_FM)
    return fm_1000hr * cdic['adj'][fm_type]

def spring_summer_adjustment(pct_hun_hr, adjfm_1000hr, fm_type):
    """ p. 148, ln 5063
     note: NFDRS #'s div by 1.4 in source code, NOT in doc.
     Eq. H: Evaluating spring-like burning conditions occurred
     Eq. I: Spring-like diameter reduction equation
     Eq. J: Summer-like diameter reduction equation
    """
    # make masks
    mask_spring = np.less_equal(pct_hun_hr, 0.75)
    mask_trans = np.logical_and(np.greater(pct_hun_hr, 0.75),
                                np.less(pct_hun_hr, 0.85))
    mask_summer = np.greater_equal(pct_hun_hr, 0.85)
    spring_ff = (pct_hun_hr - 0.75) / 0.1

    m = calc_mb(0, fm_type, mask_spring, mask_summer, mask_trans, spring_ff)
    b = calc_mb(1, fm_type, mask_spring, mask_summer, mask_trans, spring_ff)

    diam_reduction = (adjfm_1000hr * m) + b # ln 5129

    # ln 5130: not in doc, to keep DRED from reaching 0:
    diam_reduction = np.where(np.less(diam_reduction, 0.5),
       (adjfm_1000hr / cdic['adj'][fm_type] * (-0.005)) + 0.731,
        diam_reduction)


    # Eq. K: High fuel moisture diameter reduction p.149 ln 4594
    diam_reduction = np.where(np.logical_and(
                     np.greater(adjfm_1000hr, 44.0),
                     np.less(adjfm_1000hr, 60.0)),
                     (-0.0178 * adjfm_1000hr) + 1.499,
                     diam_reduction)

    return np.where(np.greater(adjfm_1000hr, 60.0),
                     (-0.005 * adjfm_1000hr) + 0.731,
                     diam_reduction)

def calc_mb(x, fm_type, mask_spring, mask_summer, mask_trans, spring_ff):
    """ create m & b masks  """
    sprg = cdic['spring'][fm_type][x]
    sumr = cdic['summer'][fm_type][x]
    # note: transitional equation NOT in documentation-
    # retrieved from source code
    return ((mask_spring * sprg) +
     (mask_summer * sumr) +
     (mask_trans * ((spring_ff + sprg) * (sumr - sprg))))

def calc_intensity_reduction_factor(area, lengthOfIgnition, fm_10hr, fm_1000hr):
    """ The intensity of fire can limit the consumption of large woody fuels.
        Mass ignition causes small fuels to be consumed more rapidly, thereby
        increasing the intensity of the fire.  This can shorten the fire duration,
        causing large fuels to absorb less energy and have less consumption.  Consume
        takes this into account by reducing the amount of diameter reduction of 1000-hr
        and 10,000-hr fuels as fires increase in intensity
        """
    extreme = 0 if 10 > area else area if area >=10 and area < 20 else (0.5 * area + 10)
    very_high = (2.0 * area) if area < 20 else (area + 20)
    high = (4 * area) if area < 20 else (2 * area + 40)

    irf = 1 # no reduction
    if fm_10hr <= 15 and fm_1000hr <= 40 and lengthOfIgnition <= extreme:
        irf = 2.0/3.0
    elif fm_10hr <= 15 and fm_1000hr <= 50 and lengthOfIgnition <= very_high:
        irf = 0.78
    elif fm_10hr <= 18 and fm_1000hr <= 50 and lengthOfIgnition <= high:
        irf = 0.89

    return irf

def high_intensity_adjustment(diam_reduction, area, lengthOfIgnition, fm_10hr, fm_1000hr):
    assert 1 == len(area) and 1 == len(lengthOfIgnition)
    assert 1 == len(fm_10hr) and 1 == len(fm_1000hr)
    reduxFactor = calc_intensity_reduction_factor(
            area[0], lengthOfIgnition[0], fm_10hr[0], fm_1000hr[0])
    return diam_reduction * reduxFactor

def diam_redux_calc(pct_hun_hr, fm_10hr, fm_1000hr, fm_type, area, lengthOfIgnition):
    """ Calculation of diameter reduction for woody fuels activity
        equations """
    # Execute calculations for diam reduction
    adjfm_1000hr = final1000hr(fm_1000hr, fm_type)
    diam_reduction = spring_summer_adjustment(pct_hun_hr, adjfm_1000hr, fm_type)
    diam_reduction = high_intensity_adjustment(
        diam_reduction, area, lengthOfIgnition, fm_10hr, fm_1000hr)

    return diam_reduction, adjfm_1000hr

def duff_redux_activity(
    diam_reduction, oneK_fsrt, tenK_fsrt, tnkp_fsrt, days_since_rain, LD):
    """Duff reduction calculation, activity
       p160 ln 4765"""

    # Eq. R: Y-intercept adjustment ln 4766-4770
    YADJ = np.minimum((diam_reduction / 1.68), 1.0)

    # Eq. S: Drying period equations - This equation requires
    # "days since significant rainfall" data: the # of days since
    # at least 0.25 inches fell...
    duff_depth = LD['duff_upper_depth'] + LD['duff_lower_depth']
    days_to_moist = 21.0 * ((duff_depth / 3.0)**1.18) # ln 4772
    days_to_dry = 57.0 * ((duff_depth / 3.0)**1.18) # ln 4773

    # Eq. T, U, V: Wet, moist, & dry duff redxu equation ln 4774
    wet_df_redux = ((0.537 * YADJ) + (0.057 *
           (oneK_fsrt[0][3] + tenK_fsrt[0][3] + tnkp_fsrt[0][3])))

    moist_df_redux = (0.323 * YADJ) + (1.034 *
                                      (diam_reduction ** 0.5))

    # p161 ln 4784
    # - this works correctly but still generates a warning, use the
    #   context manager to swallow the benign warning
    with np.errstate(divide='ignore'):
        nonzero_days = np.not_equal(days_to_moist, 0.0)
        quotient = np.where(nonzero_days, (days_since_rain / days_to_moist), 0.0)
    adj_wet_duff_redux = (wet_df_redux + (moist_df_redux - wet_df_redux) * quotient)


    # adjusted wet duff, to smooth the transition ln 4781
    dry_df_redux = (moist_df_redux +
                   ((days_since_rain - days_to_dry) / 27.0))

    # these conditionals illustrated on p.161 ln 4782-4800
    duff_reduction = np.where(
                   np.less(days_since_rain,days_to_moist),
                   adj_wet_duff_redux,
                     np.where(
                     np.greater_equal(days_since_rain, days_to_dry),
                     dry_df_redux, moist_df_redux))

    # Eq. W: Shallow duff adjustment p. 162, ln 4802-4811
    duff_reduction2 = np.where(
                     np.less_equal(duff_depth, 0.5),
                     duff_reduction * 0.5,
                     duff_reduction * ((0.25 * duff_depth) + 0.375))

    duff_reduction = np.where(
                     np.greater(duff_depth, 2.5),
                     duff_reduction,
                     duff_reduction2)

    # not in manual- but in source code, and common sense ln 4812-15
    duff_reduction = np.minimum(duff_reduction, duff_depth)

    return duff_reduction

def qmd_redux_calc(q, diam_reduction):
    """ Eq. N p. 152 ln 4611, 4616 Quadratic mean diameter reduction
    For 1000hr and 10khr fuels.
    p. 152 "Quadratic mean diameter is used to convert calculated
    inches of diameter reduction into % volume reduction."

    QMD, inches: "represents the diameter of a log in a woody size
                   class with average volume" """
    return (1.0 - ((q - diam_reduction) / q)**2.0)

def flaming_DRED_calc(hun_hr_total, diam_reduction):
    """ p. 155, ln 4655
    Flaming diameter reduction (inches)
    (%) this is a fixed value, from Ottmar 1983 """
    # stuck an 'abs' in there b/c of nan problems
    flaming_portion = (1.0 - math.e**-(abs((((20.0 - hun_hr_total)
                       / 20.0) - 1.0) / 0.2313)**2.260))
    return diam_reduction * flaming_portion, flaming_portion

def flamg_portion(q, tlc, tld, fDRED):
    """ ln 4683, 4693, 4702
        Calculates flaming portion of large woody fuels and
        ensures that flaming portion is not greater than total"""
    def check(t, tot):
        """ Check that flaming consumption does not exceed total """
        f = tld[t] * pct
        return np.where(np.greater(f, tot), tot, f)

    pct = (1.0 - (((q - fDRED)**2.0) / (q**2.0)))
    return np.array([check(t, tl) for t, tl in enumerate(tlc)])

def csdist_act(f, tots, rF):
    """ Distribute woody activity consumption by combustion stage
        f = flaming consumption
        tots = total consumption [snd, rot]
        rF = residual fractions [snd, rot]"""
    #print f, tots, rF
    #aprint f.shape, tots.shape, rF.shape
    dist = [f,                            # flaming
           (tots - f) * (1.0 - rF),       # smoldering
           (tots - f) * rF,               # residual
           tots]

    return np.array(list(zip(*dist)))

def ccon_one_act(LD):
    """ 1-hr (0 to 1/4") woody fuels consumption, activity """
    csd = [1.0, 0.0, 0.0]
    return util.csdist(LD['one_hr_sound'], csd)

def ccon_ten_act(LD):
    """ 10-hr (1/4" to 1") woody fuels consumption, activity
        ln 4537 """
    csd = [1.0, 0.0, 0.0]
    total = LD['ten_hr_sound']
    return util.csdist(total, csd)

def ccon_hun_act(pct_hun_hr, diam_reduction, QMDS, LD):
    """ Eq. F: Total 100-hr (1" - 3") fuel consumption, activity
        p.144 ln 4585"""
    resFrac = np.array([0.0])
    QMD_100hr = 1.68
    total = LD['hun_hr_sound'] * pct_hun_hr
    [flamgDRED, flaming_portion] = flaming_DRED_calc(total, diam_reduction)

    # Flaming consumption for 100-hr fuels... ln 4657
    flamg = np.where(np.greater_equal(flamgDRED, QMD_100hr),
            total,
            flamg_portion(QMDs[0], [total],
                          [LD['hun_hr_sound']], flamgDRED)[0]) # <<< confirm that this is correct- ln 4663

    # make sure flaming doesn't exceed total... ln 4665
    flamg = np.where(np.greater(flamg, total), total, flamg)
    return np.array([zip(*csdist_act(flamg, total, resFrac))]), flamgDRED, flaming_portion

def ccon_oneK_act(LD, QMDS, diam_reduction, flamgDRED):
    """ 1000-hr (3" - 9") woody fuels consumption, activity
        Eq. O, ln 4610-4613 """
    resFrac = np.array([[0.25], [0.63]]) # [snd, rot] non-flaming resid pct
    totld = np.array([LD['oneK_hr_sound'], LD['oneK_hr_rotten']])
    oneK_redux = qmd_redux_calc(QMDs[1], diam_reduction)
    total_snd = oneK_redux * totld[0]
    total_rot = oneK_redux * totld[1]
    flamg = flamg_portion(QMDs[1], [total_snd, total_rot], totld, flamgDRED)
    return csdist_act(flamg, np.array([total_snd, total_rot]), resFrac)

def ccon_tenK_act(LD, QMDS, diam_reduction, flamgDRED):
    """ 10K-hr (9 to 20") woody fuels consumption, activity
        Eq. O, ln 4615-4618 """
    resFrac = np.array([[0.33], [0.67]]) # [snd, rot] non-flaming resid pct
    totld = np.array([LD['tenK_hr_sound'], LD['tenK_hr_rotten']])
    tenK_redux = qmd_redux_calc(QMDs[2], diam_reduction)
    total_snd = tenK_redux * totld[0]
    total_rot = tenK_redux * totld[1]
    flamg = flamg_portion(QMDs[2], [total_snd, total_rot], totld, flamgDRED)
    return csdist_act(flamg, np.array([total_snd, total_rot]), resFrac)

def ccon_tnkp_act(adjfm_1000hr, flaming_portion, LD):
    """ >10,000-hr (20"+) woody fuel consumption, activity
     p. 153 Table P, ln 4619
     Documentation does not include the condition that where
     1000hr FM < 31%, redux is always 5%"""
    resFrac = np.array([[0.5], [0.67]]) # [snd, rot] non-flaming resid pct
    pct_redux = (np.less(adjfm_1000hr, 35.0) *  # mask out above 35%
           (np.where(np.less(adjfm_1000hr, 31.0),# where < 31%
              0.05,                                   # true
             (35.0 - adjfm_1000hr) / 100.0)))       # false - Table P.

    total_snd = pct_redux * LD['tnkp_hr_sound']
    total_rot = pct_redux * LD['tnkp_hr_rotten']
    # <<< DISCREPANCY b/t SOURCE and DOCUMENTATION here
    # corresponds to source code right now for testing-sake
    flamgsnd = LD['tnkp_hr_sound'] * flaming_portion
    flamgrot = LD['tnkp_hr_rotten'] * flaming_portion
    flamgsnd = np.where(np.greater(flamgsnd, total_snd),
                        total_snd, flamgsnd)
    flamgrot = np.where(np.greater(flamgrot, total_rot),
                        total_rot, flamgrot)
    return csdist_act(np.array([flamgsnd, flamgrot]), np.array([total_snd, total_rot]), resFrac)

def ccon_ffr_activity(diam_reduction, oneK_fsrt, tenK_fsrt, tnkp_fsrt, days_since_rain, LD):
    duff_redux = duff_redux_activity(diam_reduction,
        oneK_fsrt, tenK_fsrt, tnkp_fsrt, days_since_rain, LD)
    duff_depth = LD['duff_upper_depth'] + LD['duff_lower_depth']
    ffr_total_depth = (duff_depth + LD['lit_depth'] +
            LD['lch_depth'] + LD['moss_depth'])

    # - this works correctly but still generates a warning, use the
    #   context manager to swallow the benign warning
    with np.errstate(divide='ignore', invalid='ignore'):
        nonzero_depth = np.not_equal(duff_depth, 0.0)
        quotient = np.where(nonzero_depth, (duff_redux / duff_depth), 0.0)

    calculated_reduction = np.where(np.greater(duff_depth, 0.0),
        quotient * ffr_total_depth, 0.0)
    ffr_redux = np.where(
        np.less(ffr_total_depth, calculated_reduction),
        ffr_total_depth, calculated_reduction)
    return ffr_redux


def ccon_activity(fm_1000hr, fm_type, windspeed,
    slope, area, days_since_rain, fm_10hr, lengthOfIgnition, LD):
    """ Woody fuel activity equations, p. 142 """
    # execute calculations
    pct_hun_hr = pct_hun_hr_calc(windspeed, slope, fm_10hr, LD)
    [diam_reduction, adjfm_1000hr] = diam_redux_calc(
        pct_hun_hr, fm_10hr, fm_1000hr, fm_type, area, lengthOfIgnition)
    [[hun_hr_fsrt], flamgDRED, flaming_portion] = ccon_hun_act(
                                                    pct_hun_hr, diam_reduction, QMDs, LD)
    one_fsrt = ccon_one_act(LD)
    ten_fsrt = ccon_ten_act(LD)
    oneK_fsrt = ccon_oneK_act(LD, QMDs, diam_reduction, flamgDRED)
    tenK_fsrt = ccon_tenK_act(LD, QMDs, diam_reduction, flamgDRED)
    tnkp_fsrt = ccon_tnkp_act(adjfm_1000hr, flaming_portion, LD)

    # <<< below included to jive with source code- not in manual, tho
    woody = (oneK_fsrt[0][3] + oneK_fsrt[1][3] +
             tenK_fsrt[0][3] + tenK_fsrt[1][3] +
             tnkp_fsrt[0][3] + tnkp_fsrt[1][3])
    diam_reduction = np.where(np.equal(woody, 0.0), 0.0, diam_reduction)

    return (one_fsrt, ten_fsrt, hun_hr_fsrt,
           oneK_fsrt, tenK_fsrt, tnkp_fsrt,
           ccon_ffr_activity(diam_reduction, oneK_fsrt, tenK_fsrt, tnkp_fsrt, days_since_rain, LD))

