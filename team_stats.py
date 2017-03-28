# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 15:05:04 2017

@author: paull
"""

import pandas as pd
import numpy as np

gameDf = pd.read_csv('games.csv', sep='\t', index_col=0)
teamMiscDf = pd.read_csv('team_misc.csv', index_col=0)
teamDf = pd.read_csv('team.csv', index_col=0)
opponetDf = pd.read_csv('team_opponent.csv', index_col=0)
homeTeamDiff = np.array([])

# Add a new blank column to store the shooting % difference
teamMiscDf['avgDiff'] = pd.Series(np.zeros(31))

## Example of 1 team
#homeTeamName = "CHI"
#Df = gameDf.loc[gameDf['Home Team'] == homeTeamName]

for homeTeamName in gameDf['Home Team'].unique():
    Df = gameDf.loc[gameDf['Home Team'] == homeTeamName]
    for awayTeamName in Df['Away Team'].unique():
        Df2 = Df.loc[Df['Away Team'] == awayTeamName]
        # This stores the average shooting percentage the away team
        # shoots at the home team stadium
        awayFG = Df2['Away Shooting Percentage'].mean()
        
        awayTeamStats = teamDf.loc[teamDf['Name'] == awayTeamName]
        # This stores the average shooting percentage of the away team
        awayAverageFG = float(awayTeamStats['FG%'])
        
        # This stores the difference between average shooting percentage
        # and the shooting percentage at the stadium 
        diff = awayAverageFG - awayFG
        homeTeamDiff = np.append(homeTeamDiff, diff)
        avgDiff = np.mean(homeTeamDiff)
        
        # Add the avgDiff into the appropriate place in the teamMiscDf
        teamMiscDf.loc[teamMiscDf['Name'] == homeTeamName, 'avgDiff'] = avgDiff
                      
teamMiscDf.to_csv("analysis.csv", sep=',')                      