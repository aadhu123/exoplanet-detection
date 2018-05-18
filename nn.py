# Contains all the Neural Network code

import os
import tensorflow as tf
from utils import realDir
import numpy as np
import glob

from matplotlib.image import imread

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class NN:
    modelDir = os.path.join(realDir, "models")
    model = []
    dimensions = (256, 256)

    def __init__(self):
        if not os.path.exists(self.modelDir):
            os.makedirs(self.modelDir)

        self.model = self.__setUpNN()

    def __setUpNN(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(128, (3, 3), activation = "relu", input_shape = (self.dimensions[0], self.dimensions[1], 1)),
            tf.keras.layers.MaxPooling2D(pool_size = (2, 2)),
            tf.keras.layers.Conv2D(128, (3, 3), activation = "relu"),
            tf.keras.layers.MaxPooling2D(pool_size = (2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation = 'relu'),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Dense(1, activation = 'sigmoid'),
        ])

        # sgd = tf.keras.optimizers.SGD(lr=0., decay=1e-6, momentum=0.9, nesterov=True)

        model.compile(optimizer = 'adam',
                      loss = 'binary_crossentropy',
                      metrics = ['accuracy'])

        return model

    def trainingData(self, dataDir, batch_size):
        exoplanetData = glob.glob(os.path.join(dataDir, "*_1.png"))
        noExoplanetData = glob.glob(os.path.join(dataDir, "*_1.png"))

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

        randomize = np.random.randint(len(data), size = batch_size)
        return data[randomize], labels[randomize]

    def train(self, dataDir, batch_size = 400, epochs = 20):
        # self.model.fit_generator(generator(dataDir, batch_size), samples_per_epoch = 100, nb_epoch = 2, verbose = 2, show_accuracy = True, callbacks = [], validation_data = None, class_weight = None, nb_worker = 1)
        data, labels = self.trainingData(dataDir, batch_size)
        self.model.fit(data, labels, batch_size = round(batch_size / 4), epochs = epochs)

    def predict(self, data):
        return self.model.predict(data)

    def load(self, modelName):
        self.model = tf.keras.models.load_model(os.path.join(self.modelDir, modelName))

    def save(self, modelName):
        return self.model.save(os.path.join(self.modelDir, modelName))