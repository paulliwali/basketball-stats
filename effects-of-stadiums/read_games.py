from bs4 import BeautifulSoup
import requests
import pandas as pd
from pathlib import Path

current_dir = Path.cwd() / 'effects-of-stadiums'
crs = open(current_dir / "inputs" / "gamelist20120510040.txt", "r")
rows = ( row.strip().split() for row in crs )
gamelist = zip(*rows)

# list of boxscore url is in element 4
boxscore_url = gamelist[4]

# helper function using requests and bf4
def getSoupFromURL(url, suppressedOutput = True):
    if not suppressedOutput:
        print(url)
    try:
        r = requests.get(url)
    except:
        return None
    
    return BeautifulSoup(r.text)

gameDf = pd.DataFrame()
# loop through all the links and save in dataframe
for i in range(len(boxscore_url)):
    if i == 0:
        continue
    original_url = boxscore_url[i][:-13]
    old_suffix = 'boxscore.html'
    oldSoup = getSoupFromURL(original_url + old_suffix)
    meta = oldSoup.find_all('meta')[0]
    meta_content = meta.attrs.get('content')
    new_suffix = meta.attrs.get('content')[6:]
    new_url = original_url + new_suffix
    soup = getSoupFromURL(new_url)
    
    awayTeamName = boxscore_url[i][34:37]
    homeTeamName = boxscore_url[i][37:40]
    totals = soup.findAll('td',attrs={'class':'nbaGIScrTot'})
    if len(totals) == 0:
        continue
    awayPctValue = totals[2].text.split('\n')[0]
    awayPct = float(awayPctValue.split('-')[0])/float(awayPctValue.split('-')[1])
    homePctValue = totals[17].text.split('\n')[0]
    homePct = float(homePctValue.split('-')[0])/float(homePctValue.split('-')[1])
    
    df = pd.DataFrame({'Away Team' : [awayTeamName],
                   'Away Shooting Percentage': [awayPct],
                   'Home Team': [homeTeamName],
                   'Home Shooting Percentage': [homePct]
                   })
    
    gameDf = gameDf.append(df, ignore_index = True)
    
gameDf.to_csv(current_dir / "outputs" / "games.csv", sep='\t')