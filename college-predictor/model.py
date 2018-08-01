import os
import numpy as np 
import pandas as pd
import csv
import data_prep
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import TensorBoard
from keras.optimizers import Adam, SGD
from keras.losses import binary_crossentropy, mean_squared_error
from keras.activations import relu, elu, sigmoid
import talos as ta 

def runNeuralNetwork(x_train, y_train, x_val, y_val, params):
    # Rescale the X to between 0 and 1
    # Result - worse than normal setup
    # rescaledX = (data_prep.rescaleData(X, Y))

    # Stardardize the X to Gaussian Distribution
    # Result - worse than normal setup
    # standardX = (data_prep.stardardizeData(X, Y))

    # Building the model
    model = Sequential()
    model.add(Dense(params['first_neuron'], input_dim=x_train.shape[1], activation=params['activation']))
    model.add(Dropout(params['dropout']))
    model.add(Dense(input_dim=1, activation=params['last_activation']))

    # Compile the model
    # Initialize two different optimizers, using adam at the moment
    # adam = optimizers.adam(lr=learningRate)
    # sgd = optimizers.sgd(lr=learningRate, momentum=0.01)
    model.compile(loss=params['losses'], optimizer=params['optimizer'](), metrics=['acc'])

    # Create tensorboard object
    #tensorboard = TensorBoard(log_dir=os.path.join(dir, "results"), histogram_freq=10, write_graph=True,
    #                          write_images=False)

    # Fit the model and record to tensorboard
    history = model.fit(x_train, y_train,
                        validation_data=[x_val, y_val],
                        batch_size=params['batch_size'], 
                        epochs=params['epochs'],
                        verbose=0)

    return history, model

def readInputs(inputDataName, valDataName):
    dir = os.path.dirname(__file__)

    # Reading data
    filename = os.path.join(dir, 'data', 'working', inputDataName)
    dataset = pd.read_csv(filename, comment='#')
    X = dataset.iloc[:,4:22]
    Y = dataset.iloc[:,3]

    # Reading test data
    filename_test = os.path.join(dir, 'data', 'working', valDataName)
    dataset_test = pd.read_csv(filename_test, comment='#')
    X_test = dataset_test.iloc[:,4:22]
    Y_test = dataset_test.iloc[:,3]

    return X, Y, X_test, Y_test

if __name__ == "__main__":
    inputDataName = "2000-2009-pace-working.csv"
    valDataName = "2010-2017-pace-working.csv"

    p = {'lr': [0.001],
         'first_neuron':[4],
         'hidden_layers':[2],
         'batch_size': [10],
         'epochs': [500],
         'dropout': [0],
         'weight_regulizer': [None],
         'emb_output_dims': [None],
         'optimizer': [Adam],
         'losses': [binary_crossentropy],
         'activation':[relu],
         'last_activation': [sigmoid]}
    
    x, y, x_test, y_test = readInputs(inputDataName, valDataName)

    h = ta.Scan(x=x.values,
                y=y.values,
                model=runNeuralNetwork, 
                grid_downsample=1,
                params=p, 
                dataset_name='nba', 
                experiment_no='1')