import pandas as pd
import matplotlib.pyplot as plt
from mpltools import style
from mpltools import layout

style.use('ggplot')

df = pd.read_csv("/Users/amelialy/Documents/Basketball-Stats/assist-vs-secondary-assist/input.csv")

ax1 = df.plot.scatter(y='assist', x='secondary_assist', figsize=(12,8), title="Guard Passing Stats as of 28/12/2017")
df[['secondary_assist','assist','guard_name']].apply(lambda x: ax1.text(*x),axis=1);

leagueAssistAverage = df['assist'].mean()
leagueSecondAssistAverage = df['secondary_assist'].mean()
ax2 = plt.scatter(leagueSecondAssistAverage, leagueAssistAverage)
plt.savefig('assist-vs-secondary-assist/results.png')