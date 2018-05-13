from MAST_SDK import *

# mast = MAST("kepler/data_search")

# data = mast.search({
#     "ktc_kepler_id": "757076"
# })

data = MAST.fetchLightCurve("000757076", "/Users/philippe/Dev/exoplanet-detection/data")