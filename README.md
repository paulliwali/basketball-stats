# Basketball-Stats

## Effects of Stadiums

1. Scraped NBA game stats
2. Simple linear regression between DRtg and FG%
3. Calculated the difference between adjusted FG% and average FG% of an away team for a stadium
4. Averaged the difference for each stadium
5. Graphed the results

![results](https://github.com/paulliwali/Basketball-Stats/blob/master/effects-of-stadiums/outputs/results.png)

## Guards Assist vs Secondary Assist<sup>[1](#myfootnote1)</sup> in 17-18 Season so far

1. Collect the current 2017 to 2018 season data (as of Dec 29, 2018) for guards' assist and secondary assist from NBA.com
2. Filter through and remove the trivial stats. (Assists of less than 6.0 or Secondary Assists of less than 1.0)
3. Plot the results with an average of all guards
4. Label the stand outs
5. Bug: Overlapping names

![results](https://github.com/paulliwali/Basketball-Stats/blob/master/assist-vs-secondary-assist/outputs/results.png)

<a name="myfootnote1">1</a>: A player is awarded a secondary assist if they passed the ball to a player who recorded an assist within 1 second and without dribbling

## (planned) Correlation between a player's salary percentage and his stat

1. Look at the top 50 rated players in the season
2. Calculate the cap hit percentage of each 50 players with their team
3. Develop potential explaination with a certain stat and the cap hit
4. Graph the results

## Neural network to predict whether a college player will be a success or bust

### Defining a success or bust
- Limit the player pool to round 1
- A success is starter level (3 seasons of GS/G% > 75%) player for non-lottery first round picks OR all-NBA level (once) player for lottery picks
- Inputs for college players include:
    - personal physical stats
    - personal basketball related stats
    - team pace stats to adjust the basic personal stats

### Results (so-far)
|Pick Number | Player  | Probability of Success |
|------------| ------------- | ------------- |
| 1  | Deandre Ayton  | 27.2%  |
| 2  | Marvin Bagley | 27.1%  |
| 3  | Luka Doncic | N/A  |
| 4  | Jaren Jackson  | 29.1%  |
| 5  | Trae Young | 24.5%  |
| 6  | Mohamed Bamba  | 29.1%  |
| 7  | Wendell Carter | 28.1%  |
| 8  | Collin Sexton  | 27.4%  |
| 9  | Kevin Knox | 27.5%  |
| 10 | Mikal Bridges  | 21.6%  |
| 11  | Shai Gilgeous-Alexander  | 27.8%  |
| 12  | Miles Bridges | 23.6%  |
| 13  | Jerome Robinson | 19.8%  |
| 14  | Michael Porter  | 35.3%  |
| 15  | Troy Brown | 28.3%  |
| 16  | Zhaire Smith  | 29.0%  |
| 17  | Donte DiVincenzo | 24.1%  |
| 18  | Lonnie Walker | 29.0%  |
| 19  | Kevin Huerter | 24.9%  |
| 20 | Josh Okogie  | 24.1%  |
| 21  | Grayson Allen  | 16.5%  |
| 22  | Chandler Hutchison | 20.7%  |
| 23  | Aaron Holiday | 19.8%  |
| 24  | Anfernee Simons  | N/A  |
| 25  | Moritz Wagner | 23.6%  |
| 26  | Landry Shamet  | 24.1%  |
| 27  | Robert Williams | 26.7%  |
| 28  | Jacob Evans | 21.1%  |
| 29  | Dzanan Musa | N/A  |
| 30 | Omari Spellman | 28.2%  |
