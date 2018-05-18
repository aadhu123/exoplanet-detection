# Shared functions by the `main.py` and `train.py` scripts

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from MAST_SDK import *
from astropy.io import fits
import os.path

realDir = os.path.dirname(os.path.realpath(__file__))

myDPI = 50
pixels = 256

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
    # fileName = os.path.splitext(os.path.basename(filePath))[0]
    fig = plt.Figure(figsize=(pixels/50, pixels/50), dpi=50)
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    ax.scatter(data["TIME"], data["SAP_FLUX"], s = 1, c = "k")
    canvas = FigureCanvas(fig)
    canvas.print_figure(os.path.join(imgDir, fileName))