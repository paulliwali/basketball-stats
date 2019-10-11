import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from pathlib import Path

current_dir = Path.cwd() / "assist-vs-secondary-assist"
df = pd.read_csv(current_dir / "inputs" / "guard_stats.csv")
leagueAssistAverage = df['assist'].mean()
leagueSecondAssistAverage = df['secondary_assist'].mean()


ax = sns.scatterplot(data = df, x = "secondary_assist", y = "assist")
ax.axvline(x = leagueSecondAssistAverage, ls = "--", c = "green")
ax.text(leagueSecondAssistAverage + 0.05, 0, "Average Second Assist")
ax.axhline(y = leagueAssistAverage, ls = "--", c = "red")
ax.text(1.5, leagueAssistAverage + 0.5, "Average Assist")
ax.set(xlabel = "Secondary Assist", ylabel = "Assist", title="Guard Passing Stats as of 28/12/2017")
df[['secondary_assist','assist','guard_name']].apply(lambda x: ax.text(*x, size='small', color='grey'), axis=1);


fig = ax.get_figure()
fig.savefig(current_dir / "outputs" / "results.png")