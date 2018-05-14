#!/usr/bin/env python3
# Execute this script using `./main.py` and let the magic happen

import sys
from astropy.io import fits
from MAST_SDK import *
import glob

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

realDir = os.path.dirname(os.path.realpath(__file__))

dataDir = os.path.join(realDir, "data")
imgDir = os.path.join(realDir, "img")
logsDir = os.path.join(realDir, "logs")
myDPI = 50
pixels = 250

def main():
    kicIds = [
        757076,
        # 757099,
        # 757137,
        # 757231,
        # 757280,
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
        importData(kicId)
    
    print("-- done --\n\nProcessing data\n-----------------")

    # Then start processing
    for kicId in kicIds:
        processData(kicId)

    print("-- done --\n\nAI magic, watch your logs directory\n-----------------")

    print("-- done --\n")


def importData(kicId):
    # KIC ID has 9 digits
    kicId = str(kicId).zfill(9)
    if os.path.exists(os.path.join(dataDir, kicId)):
        print("Data already available for KIC ID %s"%kicId)
    else:
        MAST.fetchLightCurve(kicId, dataDir)


def processData(kicId):
    kicId = str(kicId).zfill(9)
    print("Processing KIC ID %s"%kicId)
    filePaths = glob.glob(os.path.join(dataDir, kicId, "*.fits"))

    imgDirKic = os.path.join(imgDir, kicId)
    if not os.path.exists(imgDirKic):
        os.makedirs(imgDirKic)

    for filePath in filePaths:
        fitsToImage(filePath, imgDirKic)
    

def fitsToImage(filePath, imgDirKic):
    hdul = fits.open(filePath)
    data = hdul[1].data
    hdul.close()
    fileName = os.path.splitext(os.path.basename(filePath))[0]
    fig = plt.Figure(figsize=(pixels/50, pixels/50), dpi=50)
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    ax.scatter(data["TIME"], data["SAP_FLUX"], s = 1, c = "k")
    canvas = FigureCanvas(fig)
    canvas.print_figure(os.path.join(imgDirKic, fileName))

if __name__ == '__main__':
    main()