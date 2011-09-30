def list_valid_fm_types():
    """Returns a list of valid 1000hr fuel moisture types for activity burn
       calculations"""
    return ['MEAS-Th', 'ADJ-Th', 'NFDRS-Th']

def list_valid_burntypes():
    """Returns a list of valid burn types"""
    return ['natural', 'activity'] #, 'piles']

def list_valid_units():
    """Returns a list of valid output units for consumption/emissions data."""
    return ['lbs', 'lbs_ac', 'tons', 'tons_ac', 'kg', 'kg_m^2',
            'kg_ha', 'kg_km^2', 'tonnes', 'tonnes_ha', 'tonnes_km^2']

def list_valid_ecoregions():
    """Returns a list of valid ecoregions used by consume"""
    return ['western', 'southern', 'boreal']

def list_valid_emissions_species():
    """Returns a list of valid emissions species (pollutants) for emissions data
    """
    return ["pm", "pm10", "pm25", "co", "co2", "ch4", "nmhc"]

def list_valid_combustion_stages():
    """Returns a list of valid combustion stages for consumption/emissions data
    """
    return ["flaming", "smoldering", "residual", "total"]

def list_valid_consumption_strata():
    """Returns a list of valid 1st-order consumption strata for consumption data
    """
    return ["summary", "canopy", "woody fuels", "shrub", "nonwoody",
            "ground fuels", "litter-lichen-moss"]

def perarea():
    """ Returns list of valid output units that are area weighted """
    return ['tons_ac', 'lbs_ac', 'kg_ha', 'kg_m^2', 'tonnes_ha', 'kg_km^2',
                   'tonnes_km^2']

# xml tag, internal tag, index
LoadDefs = (('fuelbed_number', 'fccs_id', 0),
            ('ecoregion', 'ecoregion', 1),
            ('cover_type', 'cover_type', 2),
            ('overstory', 'overstory', 3),
            ('midstory', 'midstory', 4),
            ('understory', 'understory', 5),
            ('snags_C1Foliage', 'snag1f', 6),
            ('snags_C1Wood', 'snag1w', 7),
            ('snags_C1woFoliage', 'snag1nf', 8),
            ('snags_C2', 'snag2', 9),
            ('snags_C3', 'snag3', 10),
            ('ladderFuels', 'ladder', 11),
            ('shrubs_Primary', 'shrub_prim', 12),
            ('shrubs_Primary_perc_live', 'shrub_prim_pctlv', 13),
            ('shrubs_Secondary', 'shrub_seco', 14),
            ('shrubs_Secondary_perc_live', 'shrub_seco_pctlv', 15),
            ('nw_Primary', 'nw_prim', 16),
            ('nw_Primary_perc_live', 'nw_prim_pctlv', 17),
            ('nw_Secondary', 'nw_seco', 18),
            ('nw_Secondary_perc_live', 'nw_seco_pctlv', 19),
            ('w_Stump_Sound', 'stump_sound', 20),
            ('w_Stump_Rotten', 'stump_rotten', 21),
            ('w_Stump_Lightered', 'stump_lightered', 22),
            ('litterDep', 'lit_depth', 23),
            ('litterDep_perc', 'lit_pctcv', 24),
            ('lichenDep', 'lch_depth', 25),
            ('lichenDep_perc', 'lch_pctcv', 26),
            ('mossDep', 'moss_depth', 27),
            ('mossDep_perc', 'moss_pctcv', 28),
            ('mossType', 'moss_type', 29),
            ('litterShortNeedle_perc', 'lit_s_ndl_pct', 30),
            ('litterLongNeedle_perc', 'lit_l_ndl_pct', 31),
            ('litterOtherConf_perc', 'lit_o_ndl_pct', 32),
            ('litterBroadleafDecid_perc', 'lit_blf_d_pct', 33),
            ('litterBroadleafEver_perc', 'lit_blf_e_pct', 34),
            ('litterPalmFrond_perc', 'lit_palm_pct', 35),
            ('litterGrass_perc', 'lit_grass_pct', 36),
            ('g_DuffDep_Upper', 'duff_upper_depth', 37),
            ('g_DuffDep_Upper_perc', 'duff_upper_pctcv', 38),
            ('g_DuffDerivation_Upper', 'duff_upper_deriv', 39),
            ('g_DuffDep_Lower', 'duff_lower_depth', 40),
            ('g_DuffDep_Lower_perc', 'duff_lower_pctcv', 41),
            ('g_DuffDerivation_Lower', 'duff_lower_deriv', 42),
            ('g_BasDep', 'bas_depth', 43),
            ('g_BasPercent', 'bas_pct', 44),
            ('g_BasRadius', 'bas_rad', 45),
            ('g_SMDepth', 'sqm_depth', 46),
            ('g_SMDensity', 'sqm_density', 47), #<<< source code flip-flops
            ('g_SMRadius', 'sqm_radius', 48),   # these two
            ('w_Sound_Sml_0_25', 'one_hr_sound', 49),
            ('w_Sound_Sml', 'ten_hr_sound', 50),
            ('w_Sound_1_3', 'hun_hr_sound', 51),
            ('w_Sound_3_9', 'oneK_hr_sound', 52),
            ('w_Sound_9_20', 'tenK_hr_sound', 53),
            ('w_Sound_GT20', 'tnkp_hr_sound', 54),
            ('w_Rotten_3_9', 'oneK_hr_rotten', 55),
            ('w_Rotten_9_20', 'tenK_hr_rotten', 56),
            ('w_Rotten_GT20', 'tnkp_hr_rotten', 57),
            ('w_Jackpots', 'pl_jackpots', 58),
            ('site_name', 'site_name', 59),
            ('site_description', 'site_desc', 60))
