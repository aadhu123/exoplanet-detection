#!/usr/bin/env python3
# Execute this script using `./main.py` and let the magic happen

import sys
from MAST_SDK import *
import glob
import utils
import os.path
from nn import *

realDir = os.path.dirname(os.path.realpath(__file__))

dataDir = os.path.join(realDir, "data")
imgDir = os.path.join(realDir, "img")
logsDir = os.path.join(realDir, "logs")

modelName = "model.hdf5"

nn = NN()
nn.load(modelName)

def main():
    kicIds = [
        11446443, # this one has an exoplanet
        757076,
        757099,
        757137,
        757231,
        757280,
    ]

    # Make required directories if not exists
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)
    if not os.path.exists(imgDir):
        os.makedirs(imgDir)
    if not os.path.exists(logsDir):
        os.makedirs(logsDir)
    

    # First fetch all data
    print("Importing data\n-----------------")

    for kicId in kicIds:
        utils.importData(dataDir, kicId)
    
    print("-- done --\n\nProcessing data\n-----------------")

    # Then start processing
    for kicId in kicIds:
        processData(kicId)

    print("-- done --\n\nAI magic, watch your logs directory\n-----------------")

    for kicId in kicIds:
        predict(kicId)

    print("-- done --\n")

def processData(kicId):
    kicId = str(kicId).zfill(9)
    print("Processing KIC ID %s"%kicId)
    filePaths = glob.glob(os.path.join(dataDir, kicId, "*.fits"))

    imgDirKic = os.path.join(imgDir, kicId)
    if not os.path.exists(imgDirKic):
        os.makedirs(imgDirKic)

    for filePath in filePaths:
        fitsToImage(filePath, imgDirKic)

def predict(kicId):
    kicId = str(kicId).zfill(9)
    imgDirKic = os.path.join(imgDir, kicId)
    files = glob.glob(os.path.join(imgDirKic, "*"))
    
    imgs = []
    for f in files:
        imgs.append(imread(f)[:,:,0:1])

    print(nn.predict(np.array(imgs)).flatten().mean())

if __name__ == '__main__':
    main()