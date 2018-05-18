#!/usr/bin/env python3
# This script fetches training data and trains the neural network stored in `./models`

import sys
import glob
import utils
import os
import shutil
from nn import *
import numpy as np
import datetime

realDir = os.path.dirname(os.path.realpath(__file__))

dataDir = os.path.join(realDir, "train/data")
logsDir = os.path.join(realDir, "train/logs")

modelName = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + ".hdf5"

nn = NN()

np.random.seed(0)

def main():
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)

    if not os.path.exists(logsDir):
        os.makedirs(logsDir)

    nn.train(dataDir)

    return

    totalKicIds = confirmedPlanetKicIds.size + kicIds.size
    iteration = 1
    while (confirmedPlanetKicIds.size + kicIds.size != 0):
        pickedId = 0
        hasExoplanet = False
        # Logic to choose a light curve with or without exoplanet randomly
        if (confirmedPlanetKicIds.size == 0):
            pickedId = kicIds[0]
            kicIds = np.delete(kicIds, 0)
        else:
            if (np.random.random() > 0.5):
                hasExoplanet = True
                pickedId = confirmedPlanetKicIds[0]
                confirmedPlanetKicIds = np.delete(confirmedPlanetKicIds, 0)
            else:
                hasExoplanet = False
                pickedId = kicIds[0]
                kicIds = np.delete(kicIds, 0)

        print("Processing KIC ID %s, %i/%i\n-----------------"%(pickedId, iteration, totalKicIds))
        
        # train(pickedId, hasExoplanet)
        iteration += 1
        print("-- done --\n")

    print("FINISHED\n")

def processData(kicId, hasExoplanet):
    kicId = str(kicId).zfill(9)
    
    filePaths = glob.glob(os.path.join(dataDir, kicId, "*.fits"))

    for (idx, filePath) in enumerate(filePaths):
        fileName = "%s_%i_%i"%(kicId, idx, hasExoplanet)
        utils.fitsToImage(filePath, imgDir, fileName)

def train(kicId):
    print("- training -")
    kicId = str(kicId).zfill(9)
    imgDirKic = os.path.join(imgDir, kicId)
    files = glob.glob(os.path.join(imgDirKic, "*"))
    
    imgs = []
    for f in files:
        imgs.append(imread(f)[:,:,0:1])

    if hasExoplanet:
        labels = np.ones(len(imgs))
    else: 
        labels = np.zeros(len(imgs))
    
    nn.train(np.array(imgs), labels)
    nn.save(modelName)

def deleteFiles(kicId):
    kicId = str(kicId).zfill(9)
    shutil.rmtree(os.path.join(dataDir, kicId))
    # shutil.rmtree(os.path.join(imgDir, kicId))
    # shutil.rmtree(os.path.join(logsDir, kicId))


if __name__ == '__main__':
    main()