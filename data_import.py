#!/usr/bin/env python3

from MAST_SDK import *
import glob
import utils
import shutil


tmpDir = os.path.join(utils.realDir, "tmp")
dataDir = os.path.join(utils.realDir, "data")

def deleteTempFiles(kicId):
    kicId = str(kicId).zfill(9)

    shutil.rmtree(os.path.join(tmpDir, kicId))

def processData(kicId, hasExoplanet):
    kicId = str(kicId).zfill(9)
    
    filePaths = glob.glob(os.path.join(tmpDir, kicId, "*.fits"))

    for (idx, filePath) in enumerate(filePaths):
        fileName = "%s_%i_%i"%(kicId, idx, hasExoplanet)
        utils.fitsToImage(filePath, dataDir, fileName)

# Make required directories if not exists
if not os.path.exists(tmpDir):
    os.makedirs(tmpDir)
if not os.path.exists(dataDir):
    os.makedirs(dataDir)

mast = MAST("kepler/confirmed_planets")

confirmedPlanetKicIds = np.unique(mast.search({
    "max_records": 20
})[2:,1])

mast.setDataSet("kepler/data_search")

kicIds = mast.search({
    "max_records": confirmedPlanetKicIds.size, # same amount of data without exoplanets
    "sci_data_quarter": 0, # avoid duplicate ids
    "condition_flag": "" # make sure that there are no anomalies in system
})[2:,0]


for kicId in confirmedPlanetKicIds:
    utils.importData(tmpDir, kicId)
    processData(kicId, 1)
    deleteTempFiles(kicId)

for kicId in kicIds:
    utils.importData(tmpDir, kicId)
    processData(kicId, 0)
    deleteTempFiles(kicId)

print("Data import finished\n")