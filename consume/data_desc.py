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

# xml tag in the FCCS/FFA generated input file, internal consume tag
LoadDefs = (('fuelbed_number', 'fccs_id'),
            ('site_name', 'site_name'),
            ('site_description', 'site_desc'),
            ('ecoregion', 'ecoregion'),
            ('overstory_loading', 'overstory'),
            ('midstory_loading', 'midstory'),
            ('understory_loading', 'understory'),
            ('snags_c1_foliage_loading', 'snag1f'),
            ('snags_c1_wood_loading', 'snag1w'),
            ('snags_c1wo_foliage_loading', 'snag1nf'),
            ('snags_c2_loading', 'snag2'),
            ('snags_c3_loading', 'snag3'),
            ('ladderfuels_loading', 'ladder'),
            ('shrubs_primary_loading', 'shrub_prim'),
            ('shrubs_primary_perc_live', 'shrub_prim_pctlv'),
            ('shrubs_secondary_loading', 'shrub_seco'),
            ('shrubs_secondary_perc_live', 'shrub_seco_pctlv'),
            ('nw_primary_loading', 'nw_prim'),
            ('nw_primary_perc_live', 'nw_prim_pctlv'),
            ('nw_secondary_loading', 'nw_seco'),
            ('nw_secondary_perc_live', 'nw_seco_pctlv'),
            ('w_stump_sound_loading', 'stump_sound'),
            ('w_stump_rotten_loading', 'stump_rotten'),
            ('w_stump_lightered_loading', 'stump_lightered'),
            ('litter_depth', 'lit_depth'),
            ('litter_loading', 'litter_loading'),
            ('lichen_depth', 'lch_depth'),
            ('lichen_loading', 'lichen_loading'),
            ('moss_depth', 'moss_depth'),
            ('moss_loading', 'moss_loading'),
            ('duff_upper_depth', 'duff_upper_depth'),
            ('duff_upper_loading', 'duff_upper_loading'),
            ('duff_lower_depth', 'duff_lower_depth'),
            ('duff_lower_loading', 'duff_lower_loading'),
            ('basal_accum_loading', 'bas_loading'),
            ('squirrel_midden_loading', 'sqm_loading'),
            ('w_sound_0_quarter_loading', 'one_hr_sound'),
            ('w_sound_quarter_1_loading', 'ten_hr_sound'),
            ('w_sound_1_3_loading', 'hun_hr_sound'),
            ('w_sound_3_9_loading', 'oneK_hr_sound'),
            ('w_sound_9_20_loading', 'tenK_hr_sound'),
            ('w_sound_gt20_loading', 'tnkp_hr_sound'),
            ('w_rotten_3_9_loading', 'oneK_hr_rotten'),
            ('w_rotten_9_20_loading', 'tenK_hr_rotten'),
            ('w_rotten_gt20_loading', 'tnkp_hr_rotten'),
            ('efg_natural', 'efg_natural'),
            ('efg_activity', 'efg_activity'),
            ('srm_id', 'srm_id'),
            ('srm_description', 'srm_description'))

