import pandas
import scipy
import numpy
import csv
import os
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

def commentHighSchoolPlayers(datafile):
    # Run through the input datafiles and comment lines where players have 0s in all the
    # statistical categories
    dir = os.path.dirname(__file__)
    datafilepath = os.path.join(dir, 'data', datafile)
    newdatafilepath = os.path.join(dir, 'data', 'working', datafile)

    r = csv.reader(open(datafilepath, 'r'))
    lines = list(r)
    for rows in lines:
        if rows.count('0') > 10:
            rows[0] = "#" + str(rows[0])
        elif "Did Not Attend College" in rows:
            rows[0] = '#' + str(rows[0])
        elif "College Not Found" in rows:
            rows[0] = '#' + str(rows[0])
        else:
            next
        print(rows)
    writer = csv.writer(open(newdatafilepath, 'w', newline=''))
    writer.writerows(lines)
    return
