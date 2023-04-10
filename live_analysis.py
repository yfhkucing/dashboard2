import pandas as pd
import plotly.graph_objs as go
import re
import numpy as np

df = pd.read_excel('Live Analysis20230408061732 (live analysis last 7 days).xlsx',
                   sheet_name='Sheet2')

datetime = pd.to_datetime(df['Launched Time'])
df['Launched Time'] = datetime

for i in range(len(df)):
  s = df['Duration'][i]
  hm = re.findall("\d+", s) #returns list containing ['hr', 'min']
  hm = [int(x) for x in hm]
  duration = hm[0]*60+hm[1]
  df['Duration'][i] = int(duration)
  df['CO rate'][i] = float(df['CO rate'][i].replace("%", ""))
  df['CTR'][i] = float(df['CTR'][i].replace("%", ""))

df['Duration']= pd.to_numeric(df['Duration'])
df['CO rate'] = pd.to_numeric(df['CO rate'])
df['CTR'] = pd.to_numeric(df['CTR'])
df.sort_values(by='Launched Time',inplace=True)
fig = go.Figure([go.Scatter(x=df['Launched Time'], y=df['Duration'])])
fig.show()