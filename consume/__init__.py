from . emissions import Emissions
from . fuel_consumption import FuelConsumption
from . data_desc import list_valid_units
from . data_desc import list_valid_fm_types
from . data_desc import list_valid_burntypes
from . data_desc import list_valid_ecoregions
from . data_desc import list_valid_emissions_species
from . data_desc import list_valid_combustion_stages
from . data_desc import list_valid_consumption_strata
from . data_desc import perarea
from . util_consume import get_version

try:
    # Using consume in a non-install situation could uncover users without
    #  the pkg_resources module. As long as you are not building a package,
    #  this failure is harmless. ks todo
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except:
    pass

"""
Consume 4.1 release information

Consume 4.1 contains the most up-to-date version of Consume's consumption
and emissions algorithms for wildland fuels.  This is a recoded version
developed by Michigan Tech Research Institute (MTRI) in consultation
with the Fire and Environmental Applications Team (US Forest Service,
Pacific Northwest Research Station, Seattle, WA).  Consume 4.1 as
developed in 2010 for use in MTRI's Wildfire Emissions Information System (WFEIS)
(wfeis.mtri.org), but was also designed to include more user-friendly
shell-based analysis options and to be used as a calculation module within
multiple platforms, including BlueSky and IFT-DSS.  It is based on Consume 3.0 code,
which was originally written in Java by the FERA team and Gary Anderson, a private
consultant.

During the recoding process, several errors were identified in the original
Consume 3.0 source code, but were fixed (via consultation with original
developers Roger Ottmar and Susan Prichard) for this version. For this reason,
results from this version will not always align with results from the official
Consume 3.0 GUI version of the software.

Notable Consume 3.0 errors included:
    (1) incorrect calculation of 'duff' reduction (p. 182 in the Consume 3.0)
    (2) a bug that interchanged 'squirrel midden' density and radius when FCCS
        values are loaded
    (3) a typo that incorrectly calculated pm2.5 emissions from 'canopy'
        consumption (thus influencing total pm2.5 emissions values as well)

* For users familiar with the original Consume 3.0 GUI software, see the
   notes section below for functionality and operational differences between
   this version and the original.

Web references:
    CONSUME: http://www.fs.fed.us/pnw/fera/research/smoke/consume/index.shtml
    FCCS: http://www.fs.fed.us/pnw/fera/fccs/
    FERA: www.fs.fed.us/pnw/fera/F
    MTRI: www.mtri.org
    BlueSky: http://www.airfire.org/data/playground/
    IFT-DSS: http://iftdss.sonomatech.com/

Requirements:
    Python 2.7 or above (free from www.python.org)
    Additional modules required:
        numpy (http://www.numpy.org/)
        pandas (http://pandas.pydata.org/)
        lxml (http://lxml.de/)

For questions/comments, contact:
    Susan Prichard, Consume manager, sprich@uw.edu


##################################################
       Notes for users familiar with the
       original Consume 3.0 GUI software
##################################################

-This version relies entirely on FCCS fuelbed data and does NOT use SAF/SRM
 cover type data except in the background for selecting the correct emissions
 factor groups to use from a link table provided by FERA.

-'Heat release' output is coupled with consumption outputs.

-Instead of selecting a specific ecoregion from Bailey's set, this version only
 requires the user to specify whether the fuelbed is located in 'western',
 'boreal', or 'southern' regions if using the Consume natural fuel consumption equations.
 See the original Consume 3.0 User's Manual to view which Bailey's ecoregions
 fit into these broader categories.

"""