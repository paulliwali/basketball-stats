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


# Add a new blank column to store the shooting % difference
teamMiscDf['avgDiff'] = pd.Series(np.zeros(31))

# Adjust the FG% as if the home team is an team with average DRtg
# with the league averge DRtg of 104.6
# The regression between DRtg and FG% is:
# FG% = 0.004*DRtg + 0.0281
def adjustFG(DRtg, FG):
    leagueAvgDRtg = 104.6
    adjFG = (0.004*(DRtg) + 0.0281) - (0.004*(leagueAvgDRtg) + 0.0281)
    return (FG-adjFG)

for homeTeamName in gameDf['Home Team'].unique():
    homeTeamDiff = np.array([])
    Df = gameDf.loc[gameDf['Home Team'] == homeTeamName]
    
    for awayTeamName in Df['Away Team'].unique():
        Df2 = Df.loc[Df['Away Team'] == awayTeamName]
        # This stores the average shooting percentage the away team
        # shoots at the home team stadium
        awayFG = Df2['Away Shooting Percentage'].mean()
        
        # Adjust the FG% of away team against the defensive abilities
        # of the home team as if it is playing a league average team
        homeTeamStats = teamMiscDf.loc[teamMiscDf['Name'] == homeTeamName]
        DRtg = float(homeTeamStats['DRtg'])
        adjawayFG = adjustFG(DRtg, awayFG)
        
        awayTeamStats = teamDf.loc[teamDf['Name'] == awayTeamName]
        # This stores the average shooting percentage of the away team
        awayAverageFG = float(awayTeamStats['FG%'])
        
        # This stores the difference between adjusted average shooting percentage
        # and the shooting percentage at the stadium 
        # +ve means the team shoots better than average
        # -ve means the team shoots worse than average
        diff = adjawayFG - awayAverageFG
        homeTeamDiff = np.append(homeTeamDiff, diff)
    
    print len(homeTeamDiff)
    avgDiff = np.mean(homeTeamDiff)
        
    # Add the avgDiff into the appropriate place in the teamMiscDf
    teamMiscDf.loc[teamMiscDf['Name'] == homeTeamName, 'avgDiff'] = avgDiff
                      
teamMiscDf.to_csv("analysis.csv", sep=',')                      