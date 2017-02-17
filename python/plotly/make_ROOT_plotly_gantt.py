# -*- coding: utf-8 -*-
"""
Make MOD Grant Gantt Chart - Madeline Steele for TriMet, 2017
"""

import os
import pandas as pd
import plotly
import datetime
from plotly import figure_factory as FF


def to_unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000

dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
gantt_csv = os.path.join(dir, 'csv/root_gantt.csv')
df = pd.read_csv(gantt_csv)

# This plotly function does most of the work but it not too
# flexible - I customize below by manipulating the object it creates

# Weirdly, the boxes get vertically flipped unless the "group_tasks" parameter
# is set to True. As of 2/10/2017, on Windows, pip or conda install plotly
# pulls an older version that does not include this essential parameter. I
# had to use this command to install the latest greatest:
# pip install git+https://github.com/plotly/plotly.py.git
# This was not an issue on my mac at home, forwhatever reason.

fig = FF.create_gantt(df, colors=['#a1dab4', '#253494'],
                      index_col='Complete',
                      show_colorbar=True,
                      bar_width=0.2,
                      showgrid_x=True,
                      showgrid_y=True,
                      height=500,
                      width=1188,
                      group_tasks=True
                      )

# Fixing the margins
margin_dict = {
      "r": 80,
      "b": 80,
      "pad": 5,
      "l": 320,
      "t": 0
    }

fig['layout']['margin'] = margin_dict
# fig['layout']['font'] = dict(family='Hind', size=14)

fig['data'][-1].items()[0][1]["colorbar"] = {"title": "Percent Complete"}

# I prefer fixed axes - not the default
fig['layout']['xaxis']['fixedrange'] = True
fig['layout']['yaxis']['fixedrange'] = True

# Removing the range selector buttons - not that helpful
del fig['layout']['xaxis']['rangeselector']

# Removing the default title, "Gantt Chart"
del fig['layout']['title']

# To modify setting at the Marker level, you can loop through the traces
# created by the create_gantt function
for i in range(0, len(df)):
    trace = fig['data'][i]
    trace['text'] = str(df['Complete'][i]) + '% complete'
    trace['hoverinfo'] = 'text'


plotly.offline.plot(fig)

plotly.plotly.iplot(fig,
                    filename='ROOT_gantt_chart',
                    world_readable=True)
