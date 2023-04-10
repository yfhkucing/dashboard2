import pandas as pd
import plotly.graph_objs as go
import re
import numpy as np
import streamlit as st
columns = ['Duration','Revenue (Rp)','Products',	
           'Different Products Sold','Orders Created','Orders Paid',
           'Unit Sales','Buyers','Average Price (Rp)','CO rate',
           'Viewers','Views','ACU','PCU','Avg. Viewing Duration',
           'Comments','Shares','Likes','New Followers','Product Impressions',
           'Product Clicks','CTR']

df = pd.read_excel('Live Analysis20230408061732 (live analysis last 7 days).xlsx',
                   sheet_name='Sheet2')

col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable selectbox widget", key="disabled")
    st.radio(
        "Set selectbox label visibility 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )

with col2:
    option = st.selectbox(
        "Select KPI",
        (columns),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )

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
fig = go.Figure([go.Scatter(x=df['Launched Time'], y=df[option])])

st.plotly_chart(fig)