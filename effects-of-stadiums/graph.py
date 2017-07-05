# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 21:28:13 2017

@author: paull
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# using ggplot styles
plt.style.use('ggplot')

# reading the analysis dataframe from csv
analysisDf = pd.read_csv('analysis.csv', index_col=0)
teams = analysisDf['Name']
diff = analysisDf['avgDiff']

# plot
figure = plt.figure(figsize=(20,10))
plt.plot(range(len(diff)), diff*100, 'o')
plt.axhline(y=0)
plt.xticks(range(len(diff)), teams, size='small')
plt.rcParams['xtick.major.pad'] = 6
            
# yticks
locs, labels = plt.yticks()
plt.ylabel('FG% Difference')
plt.title('Effects of Stadiums')
            
# moving the x-axis to the center
ax = figure.add_subplot(1,1,1)

def pct(x, pos):
    return "{0:.3f}%".format(float(x))
ax.yaxis.set_major_formatter(plt.FuncFormatter(pct))

plt.savefig('results.png')