from MAST import *

mast = MAST('kepler/confirmed_planets')

confirmedPlanetKicIds = np.unique(mast.search({
    'max_records': 100
})[2:,1])

mast.setDataSet('kepler/data_search')

kicIds = mast.search({
    'max_records':      confirmedPlanetKicIds.size, # same amount of data without exoplanets
    'sci_data_quarter': 0, # avoid duplicate ids
    'condition_flag':   '' # make sure that there are no anomalies in system
})[2:,0]

print(confirmedPlanetKicIds)
print(kicIds)