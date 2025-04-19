import pandas as pd
import requests
from bs4 import BeautifulSoup

teams = pd.read_csv("team.csv")


# helper function using requests and bf4
def getSoupFromURL(url, suppressedOutput=True):
    if not suppressedOutput:
        print(url)
    try:
        r = requests.get(url)
    except:
        return None

    return BeautifulSoup(r.text)


url = "http://www.basketball-reference.com/teams/ATL/2012.html"

soup = getSoupFromURL(url)
