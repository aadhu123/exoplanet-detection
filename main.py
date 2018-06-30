#!/usr/bin/env python3

###
### This script does predictions for all the data available in the `./data` directory.
### The results will be put into a log file in the `./logs` directory with as name
### the date-timestamp of execution.
###

import sys
from MAST import *
import glob
import utils
import os.path
from nn import *
import datetime
import math
from utils import realDir

dataDir = os.path.join(realDir, "data")
logsDir = os.path.join(realDir, "logs")
logfile = os.path.join(logsDir, datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S.csv"))

modelName = "model.hdf5"

nn = NN()
nn.load(modelName)

def main():
    if not os.path.exists(logsDir):
        os.makedirs(logsDir)

    print("Predicting\n-----------------")
    
    utils.writeToLog(logfile, "KIC ID,surpassed threshold,total,ratio\n")
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
        utils.writeToLog(logfile, "%s,%s,%s,%s\n"%(kicId, surpassed, len(probabilities), surpassed/len(probabilities)))

if __name__ == '__main__':
    main()