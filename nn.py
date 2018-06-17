# Contains all the Neural Network code

import os
import tensorflow as tf
from utils import realDir
import numpy as np
import glob

from matplotlib.image import imread

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

np.random.seed(0)

class NN:
    modelDir = os.path.join(realDir, "models")
    model = []
    dimensions = (300, 300)

    def __init__(self):
        if not os.path.exists(self.modelDir):
            os.makedirs(self.modelDir)

        self.model = self.__setUpNN()

    def __setUpNN(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(5, (50, 50), activation = "relu", input_shape = (self.dimensions[0], self.dimensions[1], 1)),
            tf.keras.layers.MaxPooling2D(pool_size = (2, 2)),
            tf.keras.layers.Conv2D(10, (4, 4), activation = "relu"),
            tf.keras.layers.MaxPooling2D(pool_size = (2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation = 'relu'),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Dense(1, activation = 'sigmoid'),
        ])

        model.compile(optimizer = 'adam',
                      loss = 'binary_crossentropy',
                      metrics = ['accuracy'])

        return model

    def trainingData(self, dataDir):
        exoplanetData = glob.glob(os.path.join(dataDir, "*_1.png"))
        noExoplanetData = glob.glob(os.path.join(dataDir, "*_0.png"))

        files = np.append(
            noExoplanetData,
            exoplanetData
        )

        data = []
        for f in files:
            data.append(imread(f)[:,:,0:1])
        data = np.array(data)

        labels = np.append(
            np.zeros(len(noExoplanetData)),
            np.ones(len(exoplanetData))
        )

        randomize = np.random.randint(len(data), size = len(data))
        return data[randomize], labels[randomize]

    def train(self, dataDir, batch_size = 40, epochs = 8):
        data, labels = self.trainingData(dataDir)
        self.model.fit(data, labels, batch_size = batch_size, epochs = epochs, validation_split = 0.1)

    def predict(self, data):
        return self.model.predict(data)

    def load(self, modelName = 'model.hdf5'):
        self.model = tf.keras.models.load_model(os.path.join(self.modelDir, modelName))

    def save(self, modelName = 'model.hdf5'):
        return self.model.save(os.path.join(self.modelDir, modelName))