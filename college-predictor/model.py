import os
import talos as ta 
from talos.model.layers import hidden_layers
import numpy as np 
import pandas as pd
import csv
import data_prep
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import TensorBoard
from keras.optimizers import Adam, SGD
from keras.losses import binary_crossentropy, mean_squared_error
from keras.activations import relu, elu, sigmoid

def readInputs(inputDataName):
    dir = os.path.dirname(__file__)

    # Reading data
    filename = os.path.join(dir, 'data', 'working', inputDataName)
    dataset = pd.read_csv(filename, comment='#')
    X = dataset.iloc[:,4:22]
    Y = dataset.iloc[:,3]

    return X, Y

def scan_hyperparameter(x_train, y_train, x_val, y_val, params):
    '''
    Using talos library to scan for the best hyperparameter settings for the 
    Neural Network setup
    '''
    # Building the model
    model = Sequential()
    model.add(Dense(params['first_neuron'], input_dim=x_train.shape[1],
                    activation=params['activation'],
                    kernel_initializer=params['kernel_initializer']))
    
    model.add(Dropout(params['dropout']))
    hidden_layers(model, params, 1)
    model.add(Dense(1, activation=params['last_activation'],
                    kernel_initializer=params['kernel_initializer']))

    model.compile(loss=params['losses'],
                  optimizer=params['optimizer'](),
                  metrics=['acc'])

    # # Create tensorboard object
    # tensorboard = TensorBoard(log_dir=os.path.join(dir, "results"), histogram_freq=10, write_graph=True,
    #                          write_images=False)

    # Fit the model and record to tensorboard
    history = model.fit(x_train, y_train,
                        validation_data=[x_val, y_val],
                        batch_size=params['batch_size'], 
                        epochs=params['epochs'],
                        verbose=0)

    return history, model


def main():
    inputDataName = "2000-2017-pace.csv"
    x, y = readInputs(inputDataName)

    p = {'lr': (0.001, 1, 10),
     'first_neuron':[12, 6],
     'hidden_layers':(0, 10, 10),
     'batch_size': [5, 10, 20, 50],
     'epochs': [100, 200],
     'dropout': [0, 2, 4, 8],
     'kernel_initializer': ['uniform', 'normal'],
     'optimizer': [Adam, SGD],
     'losses': [binary_crossentropy, mean_squared_error],
     'activation':[relu, elu],
     'last_activation': [sigmoid]}

    # t = ta.Scan(x=x.values,
    #         y=y.values,
    #         model=scan_hyperparameter, 
    #         grid_downsample=1,
    #         params=p, 
    #         dataset_name='nba', 
    #         experiment_no='k')

if __name__ == "__main__": main()