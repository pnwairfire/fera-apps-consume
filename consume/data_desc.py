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

# xml tag in the FCCS/FFA generated input file, internal consume tag, index
'''
Use to renumber structure below.
import sys
with open(sys.argv[1], 'r') as infile:
    counter = 0
    for line in infile:
        line = line.rstrip()
        chunks = line.split(',')
        chunks[2] = ' {})'.format(counter)
        out = ",".join(chunks)
        counter += 1
        print(out)
'''        
LoadDefs = (('fuelbed_number', 'fccs_id', 0),
            ('site_name', 'site_name', 1),
            ('site_description', 'site_desc', 2),
            ('ecoregion', 'ecoregion', 3),
            ('overstory_loading', 'overstory', 4),
            ('midstory_loading', 'midstory', 5),
            ('understory_loading', 'understory', 6),
            ('snags_c1_foliage_loading', 'snag1f', 7),
            ('snags_c1_wood_loading', 'snag1w', 8),
            ('snags_c1wo_foliage_loading', 'snag1nf', 9),
            ('snags_c2_loading', 'snag2', 10),
            ('snags_c3_loading', 'snag3', 11),
            ('ladderfuels_loading', 'ladder', 12),
            ('shrubs_primary_loading', 'shrub_prim', 13),
            ('shrubs_primary_perc_live', 'shrub_prim_pctlv', 14),
            ('shrubs_secondary_loading', 'shrub_seco', 15),
            ('shrubs_secondary_perc_live', 'shrub_seco_pctlv', 16),
            ('nw_primary_loading', 'nw_prim', 17),
            ('nw_primary_perc_live', 'nw_prim_pctlv', 18),
            ('nw_secondary_loading', 'nw_seco', 19),
            ('nw_secondary_perc_live', 'nw_seco_pctlv', 20),
            ('w_stump_sound_loading', 'stump_sound', 21),
            ('w_stump_rotten_loading', 'stump_rotten', 22),
            ('w_stump_lightered_loading', 'stump_lightered', 23),
            ('litter_depth', 'lit_depth', 24),
            ('litter_loading', 'litter_loading', 25),
            ('lichen_depth', 'lch_depth', 26),
            ('lichen_loading', 'lichen_loading', 27),
            ('moss_depth', 'moss_depth', 28),
            ('moss_loading', 'moss_loading', 29),
            ('duff_upper_depth', 'duff_upper_depth', 30),
            ('duff_upper_loading', 'duff_upper_loading', 31),
            ('duff_lower_depth', 'duff_lower_depth', 32),
            ('duff_lower_loading', 'duff_lower_loading', 33),
            ('basal_accum_loading', 'bas_loading', 34),
            ('squirrel_midden_loading', 'sqm_loading', 35),
            ('w_sound_0_quarter_loading', 'one_hr_sound', 36),
            ('w_sound_quarter_1_loading', 'ten_hr_sound', 37),
            ('w_sound_1_3_loading', 'hun_hr_sound', 38),
            ('w_sound_3_9_loading', 'oneK_hr_sound', 39),
            ('w_sound_9_20_loading', 'tenK_hr_sound', 40),
            ('w_sound_gt20_loading', 'tnkp_hr_sound', 41),
            ('w_rotten_3_9_loading', 'oneK_hr_rotten', 42),
            ('w_rotten_9_20_loading', 'tenK_hr_rotten', 43),
            ('w_rotten_gt20_loading', 'tnkp_hr_rotten', 44),
            ('efg_natural', 'efg_natural', 45),
            ('efg_activity', 'efg_activity', 46),
            ('srm_id', 'srm_id', 47),
            ('srm_description', 'srm_description', 48))

