# Exoplanet Detection using a convolutional neural network

This repository is linked to a bachelor thesis, which will be added at a later point in time. The main objective of the research paper is to create an automated pipeline for detecting exoplanets using the light curves obtained by the Kepler mission. These light curves can be found on [MAST](https://archive.stsci.edu/). The code first downloads light curve data into `.tmp/`, which it then casts into plots of equal width and height stored into `./data`. These images are then passed into a Convolutional Neural Network (CNN) made with TensorFlow (thanks Google). The CNN filters out the graphs with potential exoplanets in them and logs the Kepler IDs (KIC ID) in a log file generated in `./logs`. Now you have some KIC IDs, you can more closely investigate these star systems. Good luck hunting exoplanets!

This project requires Python3 and TensorFlow (install with `pip3 install tensorflow` or refer to https://www.tensorflow.org/install/)

## How to use
 - Fork the repo
 - Clone your forked repo
 - Run the command `./train.py` to train your model, it will be saved as `./models/model.hdf5`
 - Tweek the `./data_import.py` script to your likings (or not) and run it
 - Run the command `./main.py`
 - The exoplanet candidates' KIC IDs will be output in the file `./logs/{currentISOdate}`