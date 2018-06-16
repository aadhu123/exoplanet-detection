#!/usr/bin/env python3

###
### This script does predictions for all the data available in the `./data` directory.
### The results will be put into a log file in the `./logs` directory with as name
### the date-timestamp of execution.
###

import sys
from MAST_SDK import *
import glob
import utils
import os.path
from nn import *
import datetime
import math

realDir = os.path.dirname(os.path.realpath(__file__))

dataDir = os.path.join(realDir, "data")
logsDir = os.path.join(realDir, "logs")
logfile = os.path.join(logsDir, datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"))

modelName = "model.hdf5"

nn = NN()
nn.load(modelName)

def main():
    if not os.path.exists(logsDir):
        os.makedirs(logsDir)

    print("Predicting\n-----------------")
    
    utils.writeToLog(logfile, "KIC ID      images surpassed threshold/total\n")
    kicDirs = glob.glob(os.path.join(dataDir, "*"))

    print("Progress: [  0%] [{0}]".format('.' * 50), end='\r')

    for idx, kicDir in enumerate(kicDirs):
        predict(kicDir)
        percentage = math.ceil(100 * (idx + 1) / len(kicDirs))
        print("Progress: [{0}%] [{1}{2}]".format(
                                                "%3s"%percentage,
                                                '#' * math.ceil(percentage / 2), 
                                                '.' * (50 - math.ceil(percentage / 2))), 
                                                end='\r'
                                            )

    print("\n")

def processData(kicId):
    kicId = str(kicId).zfill(9)
    print("Processing KIC ID %s"%kicId)
    filePaths = glob.glob(os.path.join(dataDir, kicId, "*.fits"))

    imgDirKic = os.path.join(imgDir, kicId)
    if not os.path.exists(imgDirKic):
        os.makedirs(imgDirKic)

    for filePath in filePaths:
        utils.fitsToImage(filePath, imgDirKic, os.path.splitext(os.path.basename(filePath))[0])

def predict(kicDir):
    kicId = os.path.basename(kicDir)
    files = glob.glob(os.path.join(kicDir, "*"))
    
    imgs = []
    for f in files:
        imgs.append(imread(f)[:,:,0:1])

    probabilities = nn.predict(np.array(imgs)).flatten()
    threshold = 0.9
    surpassed = sum([p > threshold for p in probabilities])
    if surpassed != 0:
        utils.writeToLog(logfile, "%s   %s/%s\n"%(kicId, surpassed, len(probabilities)))

if __name__ == '__main__':
    main()