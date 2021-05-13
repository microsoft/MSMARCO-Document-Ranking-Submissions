# MS MARCO Document: Script for plotting leaderboard over time scatter plots

import pandas as pd
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
plt.switch_backend('agg')

# Solution to use Type 1 fonts:
# https://stackoverflow.com/questions/13132194/type-1-fonts-with-log-graphs

# If fonttype = 1 doesn't work with LaTeX, try fonttype 42.
plt.rc('pdf',fonttype = 42)
plt.rc('ps',fonttype = 42)

df = pd.read_csv('../leaderboard/leaderboard.csv', parse_dates=['date'])

# Plot all the runs
ax = df.plot(x='date',y='MRR@100 (Eval)',marker='o',linestyle='none',label='Submission')

# Overlay all SOTA runs, in red.
sota = df[df['Unnamed: 2'] == '🏆']
sota.plot(ax=ax, x='date',y='MRR@100 (Eval)',marker='o',color = 'red',linestyle='none',label='SOTA')

# Guide to formatting date ticks
# https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/date.html
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.set_xlim([datetime.date(2020, 8, 1), datetime.date(2021, 5, 1)])

plt.title('MS MARCO Document Leaderboard')
plt.xlabel('Date')
plt.ylabel('MRR@100')

plt.savefig('leaderboard.pdf', bbox_inches='tight', format='pdf')

