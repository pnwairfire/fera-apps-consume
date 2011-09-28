"""

### consume.py ###

Consume 3.0 was developed and designed originally in Java by US Forest
Service Fire and Environmental Research Applications (FERA) team.

This is a recoded version (2010) developed by Michigan Tech Research
Institute (MTRI) in consultation with FERA.  This version was developed
for use in MTRI's Wildfire Emissions Information System (WFEIS)
(wfeis.mtri.org), but was also designed to include more user-friendly
shell-based analysis options.

During the recoding process, several errors were identified in the original
Consume 3.0 source code, but were fixed (via consultation with original
developers Roger Ottmar and Susan Prichard) for this version. For this reason,
results from this version will not always align with results from the official
Consume 3.0 GUI version of the software. Notable errors include:

    (1) incorrect calculation of 'duff' reduction (p. 182 in the Consume 3.0
    (2) a bug that interchanges 'squirrel midden' density and radius when FCCS
        values are loaded
    (3) a typo that incorrectly calculates pm2.5 emissions from 'canopy'
        consumption (thus influencing total pm2.5 emissions values as well)

    * For users familiar with the original Consume 3.0 GUI software, see the
      notes section below for functionality and operational differences between
      this version and the original.

References:
    CONSUME: http://www.fs.fed.us/pnw/fera/research/smoke/consume/index.shtml
    FCCS: http://www.fs.fed.us/pnw/fera/fccs/
    FERA: www.fs.fed.us/pnw/fera/F
    MTRI: www.mtri.org

Requirements:
    Python 2.4 or above (free from www.python.org)
    w/ np extension (free from http://np.scipy.org/)

For questions/comments, contact:
    Michael G. Billmire mgbillmi@mtu.edu
    Tyler A. Erickson taericks@mtu.edu


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
 'boreal', or 'southern' regions. See the original Consume 3.0 User's Manual
 to view which Bailey's ecoregions fit into these broader categories.

"""

from emissions import *
from fuel_consumption import *
from data_desc import list_valid_units