import os
import numpy as np 
import pandas as pd
import csv
import data_prep
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import CSVLogger, TensorBoard

def runNeuralNetwork(dataName, epochs, batch, learningRate):
    # Fix the random seed for testing
    np.random.seed(7)

    dir = os.path.dirname(__file__)

    # Reading data
    filename = os.path.join(dir, 'data', 'working', dataName)
    dataset = pd.read_csv(filename, comment='#')
    X = dataset.iloc[:,4:22]
    Y = dataset.iloc[:,3]

    # Reading test data
    filename_test = os.path.join(dir, 'data', 'working', '2010-2017-pace-working.csv')
    dataset_test = pd.read_csv(filename_test, comment='#')
    X_test = dataset_test.iloc[:,4:22]
    Y_test = dataset_test.iloc[:,3]

    # Rescale the X to between 0 and 1
    # Result - worse than normal setup
    # rescaledX = (data_prep.rescaleData(X, Y))

    # Stardardize the X to Gaussian Distribution
    # Result - worse than normal setup
    # standardX = (data_prep.stardardizeData(X, Y))

    # Building the model
    model = Sequential()
    model.add(Dense(12, input_dim=18, activation='relu'))
    model.add(Dense(9, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(6, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # Compile the model
    # Initialize two different optimizers, using adam at the moment
    adam = optimizers.adam(lr=learningRate)
    sgd = optimizers.sgd(lr=learningRate, momentum=0.01)
    model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])

    # Create tensorboard object
    tensorboard = TensorBoard(log_dir=os.path.join(dir, "results"), histogram_freq=10, write_graph=True,
                              write_images=False)

    # Fit the model and record to tensorboard
    model.fit(X.values, Y.values, epochs=epochs, batch_size=batch, validation_data=(X_test, Y_test), callbacks=[tensorboard])

if __name__ == "__main__":
    dataName = "2000-2009-pace-working.csv"
    epochs = 500
    batch = 10
    learningRate = 0.005
    exportCSV = True

    runNeuralNetwork(dataName, epochs, batch, learningRate)