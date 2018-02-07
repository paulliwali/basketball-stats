# Basketball-Stats

## Effects of Stadiums

1. Scraped NBA game stats
2. Simple linear regression between DRtg and FG%
3. Calculated the difference between adjusted FG% and average FG% of an away team for a stadium
4. Averaged the difference for each stadium
5. Graphed the results

![results](https://github.com/paulliwali/Basketball-Stats/blob/master/effects-of-stadiums/results.png)

## Guards Assist vs Secondary Assist<sup>[1](#myfootnote1)</sup> in 17-18 Season so far

1. Collect the current 2017 to 2018 season data (as of Dec 29, 2018) for guards' assist and secondary assist from NBA.com
2. Filter through and remove the trivial stats. (Assists of less than 6.0 or Secondary Assists of less than 1.0)
3. Plot the results with an average of all guards
4. Label the stand outs
5. Bug: Overlapping names

![results](https://github.com/paulliwali/Basketball-Stats/blob/master/assist-vs-secondary-assist/results.png)

<a name="myfootnote1">1</a>: A player is awarded a secondary assist if they passed the ball to a player who recorded an assist within 1 second and without dribbling

## (planned) Correlation between a player's salary percentage and his stat

1. Look at the top 50 rated players in the season
2. Calculate the cap hit percentage of each 50 players with their team
3. Develop potential explaination with a certain stat and the cap hit
4. Graph the results

## (planned) Neural network for a player's basic stats (Ppg, rpg, apg) based on team stats

## (planned) Neural network to predict whether a college player will be a success or bust

#### Defining a success or bust
- Limit the player pool to round 1
- A success is starter level (3 seasons of GS/G% > 75%) player for non-lottery first round picks OR all-NBA level (once) player for lottery picks
- Inputs for college players include:
    - basic physical stats
    - basic basketball related stats
    - advanced offensive stats
    - advanced defensive stats
    - type of coaching/system
    - type of conference
- Output for players:
    - 0 for fail
    - 1 for success
- Assumptions:
    - Eras/decades will influence the weights on the different inputs, so use some years of the same era as test to predict other years of the same era
    - There might not be enough test data if the eras/decades are separated into cohorts
- Input data format:

|player_name|isSucessful|physical-stats|basic-stats|advanced-oStats|advanced-dStats|conference|
|=============================================================================================|
|Player A   |True       |###, ###, ### |###, ###, #|#, ###, ###, # |###, ###, ###  |100000000 |

[] Gather csv file with 1st round playeer's college data for 2005 to 2015
[] Create a rough NN with this
[] Test the hypothesis

