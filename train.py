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

def main():
    nn = NN()
    nn.train(dataDir)
    nn.save()

if __name__ == '__main__':
    main()