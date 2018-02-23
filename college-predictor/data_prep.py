import pandas
import scipy
import numpy
import sklearn.preprocessing

def rescaleData(X, Y):
    # Rescale the input data to a range between 0 to 1
    scaler = sklearn.preprocessing.MinMaxScaler(feature_range=(0,1))
    rescaledX = scaler.fit_transform(X)
    return rescaledX

def stardardizeData(X, Y):
    # Stardardize the input data to a Gaussian distribution with mean of 0
    # and std.dev of 1
    scaler = sklearn.preprocessing.StandardScaler().fit(X)
    standardX = scaler.transform(X)
    return standardX