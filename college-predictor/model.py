import os
import numpy as np 
import pandas as pd
import csv
import data_prep
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import CSVLogger, TensorBoard

def runNeuralNetwork(dataName, epochs, batch, learningRate, exportCSV):
    # Fix the random seed for testing
    np.random.seed(7)

    dir = os.path.dirname(__file__)

    # Export the results into a folder with appropriate
    if exportCSV:
        csvFilename = '%s_e%s_b%s_lr%s.csv' % (dataName, epochs, batch, learningRate)
        csvPathname = os.path.join(dir, 'results', csvFilename)

    # Reading 2000 to 2009 data
    filename = os.path.join(dir, 'data', dataName)
    dataset = pd.read_csv(filename, comment='#')
    X = dataset.iloc[:,4:18]
    Y = dataset.iloc[:,3]

    print(X)

    # Rescale the X to between 0 and 1
    # Result - worse than normal setup
    # rescaledX = (data_prep.rescaleData(X, Y))

    # Stardardize the X to Gaussian Distribution
    # Result - worse than normal setup
    # standardX = (data_prep.stardardizeData(X, Y))

    # Building the model
    model = Sequential()
    model.add(Dense(12, input_dim=14, activation='relu'))
    model.add(Dense(9, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(6, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # Compile the model
    adam = optimizers.adam(lr=learningRate)
    sgd = optimizers.sgd(lr=learningRate, momentum=0.01)
    model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])

    # Fit the model
    csv_logger = CSVLogger(csvPathname, separator=',', append=False)
    tensorboard = TensorBoard(log_dir=os.path.join(dir, "results"), histogram_freq=0, write_graph=True,
                                write_images=False)
    model.fit(X.values, Y.values, epochs=epochs, batch_size=batch, callbacks=[csv_logger, tensorboard])

    # Make predictions with the model
    predictions = model.predict(X.values)
    rounded = [round(x[0]) for x in predictions]
    print(rounded)
    # With L0 - 8, L1 - 2 it produces okay results of accuracy of 0.8108

    # Evaluate the model with test data
    filename_test = os.path.join(dir, 'data', "test_stat.csv")
    dataset_test = pd.read_csv(filename_test)
    X_test = dataset_test.iloc[:,2:16]
    Y_test = dataset_test.iloc[:,1]
    scores = model.evaluate(X_test.values, Y_test.values)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

if __name__ == "__main__":
    dataName = '2000-2009.csv'
    epochs = 500
    batch = 10
    learningRate = 0.001
    exportCSV = True

    runNeuralNetwork(dataName, epochs, batch, learningRate, exportCSV)