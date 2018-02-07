import numpy as np 
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense

# Fix the random seed for testing
np.random.seed(7)

dataset = pd.read_csv("/Users/amelialy/Documents/Basketball-Stats/college-predictor/2005_stats.csv", comment='#')
X = dataset.iloc[:,2:19]
Y = dataset.iloc[:,1]

# Building the model
model = Sequential()
model.add(Dense(12, input_dim=17, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X, Y, epochs=150, batch_size=10)

# Make predictions with the model
predictions = model.predict(X)
rounded = [round(x[0]) for x in predictions]
print(rounded)

# Evaluate the model
dataset_test = pd.read_csv("/Users/amelialy/Documents/Basketball-Stats/college-predictor/test_stat.csv")
X_test = dataset_test.iloc[:,2:19]
Y_test = dataset_test.iloc[:,1]
scores = model.evaluate(X_test, Y_test)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))