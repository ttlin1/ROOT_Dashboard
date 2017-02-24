import os
import pandas as pd
import plotly
import plotly.graph_objs as go
import textwrap

dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
budget_csv = os.path.join(dir, 'csv/Root_budget_for_pie.csv')

df = pd.read_csv(budget_csv)


# Reverse sorting makes the categories draw in correct order
df.sort_index(ascending=False, inplace=True)

df['pct'] = df['USD'] / df['USD'].sum()
df['pct'] = df['pct'].apply(lambda x: '{0:.1f}%'.format(x*100))

# Create task list with html line breaks
tasks = df['Task'].apply(lambda x: x.split(": ")[-1])
tasks = tasks.apply(lambda x: "<br>".join(textwrap.wrap(x, width=20)))
money_text = df['USD'].apply(lambda x: '${:,}'.format(x))

trace1 = {
  "direction": "clockwise",
  "hoverinfo": "label+text+percent",
  "labels": tasks,
  "textfont": {
    "family": "Arial",
    "size": 16
  },
  "marker": {
    "colors": ["#0D4C6A", "#327291", "#15954D"]
  },
  "showlegend": False,
  "sort": False,
  "text": money_text,
  "textinfo": "label+percent",
  "textposition": "outside",  # "inside" | "outside" | "auto" | "none"
  "type": "pie",
  "values": df['USD']
}
data = go.Data([trace1])
layout = {"margin": {
                    "r": 120,
                    "l": 145,
                    "t": 160
                    },
          # "title": "MOD Grant Budget"
          }
fig = go.Figure(data=data, layout=layout)


plotly.offline.plot(fig)
plotly.plotly.iplot(fig, filename='root-budget-pie')
