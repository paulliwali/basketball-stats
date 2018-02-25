import os
import numpy as np 
import pandas as pd
import data_prep
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense

# Fix the random seed for testing
np.random.seed(7)

dir = os.path.dirname(__file__)

# Reading 2000 to 20015 data
filename = os.path.join(dir, '2000-2015-First-Round.csv')
dataset = pd.read_csv(filename, comment='#')
X = dataset.iloc[:,4:18]
Y = dataset.iloc[:,3]

print(X)

# # Reading 2004 data
# filename = os.path.join(dir, '2004_stats.csv')
# dataset2004 = pd.read_csv(filename, comment='#')
# X = X.append(dataset2004.iloc[:,2:19], ignore_index=True)
# Y = Y.append(dataset2004.iloc[:,1], ignore_index=True)

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
adam = optimizers.adam(lr=0.001)
sgd = optimizers.sgd(lr=0.001, momentum=0.01)
model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])

# Fit the model
model.fit(X.values, Y.values, epochs=500, batch_size=10)

# Make predictions with the model
predictions = model.predict(X.values)
rounded = [round(x[0]) for x in predictions]
print(rounded)
# With L0 - 8, L1 - 2 it produces okay results of accuracy of 0.8108

# Evaluate the model with test data
filename_test = os.path.join(dir, "test_stat.csv")
dataset_test = pd.read_csv(filename_test)
X_test = dataset_test.iloc[:,2:16]
Y_test = dataset_test.iloc[:,1]
scores = model.evaluate(X_test.values, Y_test.values)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))