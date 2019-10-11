import pandas as pd
import numpy as np
from pathlib import Path

current_dir = Path.cwd() / 'effects-of-stadiums'
game_df = pd.read_csv(current_dir / 'cache' / 'games.csv', sep='\t', index_col=0)
team_misc_df = pd.read_csv(current_dir / 'inputs' / 'team_misc.csv', index_col=0)
team_df = pd.read_csv(current_dir / 'inputs' / 'team.csv', index_col=0)
opponent_df = pd.read_csv(current_dir / 'inputs' / 'team_opponent.csv', index_col=0)

# Add a new column to store the shooting % difference
team_misc_df['avgDiff'] = 0

# Adjust the FG% as if the home team is a team with average DRTG
# with the league average DRTG of 104.6
# The regression between DRTG and FG% is:
# FG% = 0.004*DRTG + 0.0281
def adjustFG(DRTG, FG):
    leagueAvgDRTG = 104.6
    adjFG = (0.004 * DRTG + 0.0281) - (0.004 * leagueAvgDRTG + 0.0281)
    return (FG-adjFG)

for homeTeamName in game_df['Home Team'].unique():
    homeTeamDiff = np.array([])
    df = game_df.loc[game_df['Home Team'] == homeTeamName]
    
    for awayTeamName in df['Away Team'].unique():
        df2 = df.loc[df['Away Team'] == awayTeamName]
        # This stores the average shooting percentage the away team
        # shoots at the home team stadium
        awayFG = df2['Away Shooting Percentage'].mean()
        
        # Adjust the FG% of away team against the defensive abilities
        # of the home team as if it is playing a league average team
        homeTeamStats = team_misc_df.loc[team_misc_df['Name'] == homeTeamName]
        DRTG = float(homeTeamStats['DRtg'])
        adjawayFG = adjustFG(DRTG, awayFG)
        
        awayTeamStats = team_df.loc[team_df['Name'] == awayTeamName]
        # This stores the average shooting percentage of the away team
        awayAverageFG = float(awayTeamStats['FG%'])
        
        # This stores the difference between adjusted average shooting percentage
        # and the shooting percentage at the stadium 
        # +ve means the team shoots better than average
        # -ve means the team shoots worse than average
        diff = adjawayFG - awayAverageFG
        homeTeamDiff = np.append(homeTeamDiff, diff)
    
    print(len(homeTeamDiff))
    avgDiff = np.mean(homeTeamDiff)
        
    # Add the avgDiff into the appropriate place in the team_misc_df
    team_misc_df.loc[team_misc_df['Name'] == homeTeamName, 'avgDiff'] = avgDiff
                      
team_misc_df.to_csv(current_dir / 'outputs' / 'analysis.csv', sep=',')                      