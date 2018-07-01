#!/usr/bin/env python3

###
### This script is meant to import some data to the `./data` directory in order to start
### predicting.
###


from MAST import *
import glob
import utils
import shutil

tmpDir = os.path.join(utils.realDir, 'tmp')
dataDir = os.path.join(utils.realDir, 'data')

def deleteTempFiles(kicId):
    kicId = str(kicId).zfill(9)

    shutil.rmtree(os.path.join(tmpDir, kicId))

# def processData(kicId, hasExoplanet):
#     kicId = str(kicId).zfill(9)
    
#     filePaths = glob.glob(os.path.join(tmpDir, kicId, '*.fits'))

#     for (idx, filePath) in enumerate(filePaths):
#         fileName = "%s_%i_%i"%(kicId, idx, hasExoplanet)
#         utils.fitsToImage(filePath, dataDir, fileName)

def dataExists(kicId):
    kicDir = os.path.join(dataDir, kicId)

    if os.path.exists(kicDir):
        print("Directory of KIC ID %s already exists\n"%(kicId))
        return True

    return False

def processData(kicId, hasExoplanet):
    kicDir = os.path.join(dataDir, kicId)
    os.makedirs(kicDir)
    
    filePaths = glob.glob(os.path.join(tmpDir, kicId, '*.fits'))

    for (idx, filePath) in enumerate(filePaths):
        fileName = os.path.splitext(os.path.basename(filePath))[0]
        utils.fitsToImage(filePath, kicDir, fileName)


# Make required directories if not exists
if not os.path.exists(tmpDir):
    os.makedirs(tmpDir)
if not os.path.exists(dataDir):
    os.makedirs(dataDir)

mast = MAST('kepler/data_search')

kicIds = mast.search({
    'max_records':      3000, # same amount of data without exoplanets
    'sci_data_quarter': 0, # avoid duplicate ids
})[2:,0]

## Use this to retrieve published/confirmed planets
# mast.setDataSet("kepler/published_planets")

# confirmedPlanetKicIds = np.unique(mast.search({
#     "max_records": 200
# })[2:,1])


for i in range(len(kicIds)):
    print("%i/%i"%(i + 1, len(kicIds)))
    kicId = str(kicIds[i]).zfill(9)

    if dataExists(kicId):
        continue
    
    utils.importData(tmpDir, kicId)
    processData(kicId, 0)
    deleteTempFiles(kicId)

print("Data import finished\n")