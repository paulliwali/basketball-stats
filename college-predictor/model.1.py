import talos as ta
import wrangle as wr
from talos.metrics.keras_metrics import fmeasure
import pandas as pd
# this a locally modified version of the actual package
from livelossplot import PlotLossesKeras
from keras.models import Sequential
from keras.layers import Dropout, Dense
# Keras items
from keras.optimizers import Adam, Nadam
from keras.activations import relu, elu, sigmoid
from keras.losses import binary_crossentropy

x, y = ta.datasets.breast_cancer()

# and normalize every feature to mean 0, std 1
x = wr.mean_zero(pd.DataFrame(x)).values

def breast_cancer_model(x_train, y_train, x_val, y_val, params):

    model = Sequential()
    model.add(Dense(params['first_neuron'], input_dim=x_train.shape[1],
                    activation=params['activation'],
                    kernel_initializer=params['kernel_initializer']))
    
    model.add(Dropout(params['dropout']))

    model.add(Dense(1, activation=params['last_activation'],
                    kernel_initializer=params['kernel_initializer']))
    
    model.compile(loss=params['losses'],
                  optimizer=params['optimizer'](),
                  metrics=['acc', fmeasure])
    
    history = model.fit(x_train, y_train, 
                        validation_data=[x_val, y_val],
                        batch_size=params['batch_size'],
                        callbacks=[PlotLossesKeras()],
                        epochs=params['epochs'],
                        verbose=0)

    return history, model

# then we can go ahead and set the parameter space
p = {'first_neuron':[10],
     'hidden_layers':[0, 1, 2],
     'batch_size': [30],
     'epochs': [100],
     'dropout': [0],
     'kernel_initializer': ['uniform','normal'],
     'optimizer': [Adam],
     'losses': [binary_crossentropy],
     'activation':[relu, elu],
     'last_activation': [sigmoid]}

t = ta.Scan(x=x,
            y=y,
            model=breast_cancer_model,
            grid_downsample=1,
            params=p,
            dataset_name='breast_cancer',
            experiment_no='k')