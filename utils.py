# Shared functions by the `main.py` and `train.py` scripts

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate
import numpy as np

plt.style.use('dark_background')
np.set_printoptions(threshold = np.inf)

from MAST_SDK import *
from astropy.io import fits
import os.path

realDir = os.path.dirname(os.path.realpath(__file__))

pixels = 300

def importData(dataDir, kicId):
    # KIC ID has 9 digits
    kicId = str(kicId).zfill(9)
    if os.path.exists(os.path.join(dataDir, kicId)):
        print("Data already available for KIC ID %s"%kicId)
    else:
        MAST.fetchLightCurve(kicId, dataDir)

def fitsToImage(filePath, imgDir, fileName):
    hdul = fits.open(filePath)
    data = hdul[1].data
    hdul.close()
    
    nans = np.isnan(data['SAP_FLUX'])

    time = data['TIME'][~nans]
    flux = data['SAP_FLUX'][~nans]

    # fit = interpolate.interp1d(time, flux)
    # # fileName = os.path.splitext(os.path.basename(filePath))[0]
    winlen = round(len(flux) / 50)
    if not winlen % 2:
        winlen += 1
    # flux /= fit(time)

    fig = plt.Figure(figsize=(pixels / 50, pixels / 50), dpi = 50)
    ax = fig.add_subplot(111)

    ax.scatter(time, flux, s = 1, c = 'w')
    ax.set_xlim(min(time), max(time))
    ax.set_ylim(min(flux), max(flux))

    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)

    ax.set_axis_off()

    fig.set_tight_layout(True)

    canvas = FigureCanvas(fig)
    canvas.print_figure(os.path.join(imgDir, fileName))


def writeToLog(file, text):
    f = open(file, 'a')
    f.write(text)
    f.close()