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
