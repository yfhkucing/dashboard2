import pandas as pd
import re
import streamlit as st
import plotly.express as px
columns = ['Duration','Revenue (Rp)','Products',	
           'Different Products Sold','Orders Created','Orders Paid',
           'Unit Sales','Buyers','Average Price (Rp)','CO rate',
           'Viewers','Views','ACU','PCU','Avg. Viewing Duration',
           'Comments','Shares','Likes','New Followers','Product Impressions',
           'Product Clicks','CTR','conversion']

df = pd.read_excel('data2.xlsx',
                   sheet_name='Sheet2')

col1, col2, col3 = st.columns(3)

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

with col3:
    option2 = st.selectbox(
        "Select KPI 2",
        (columns),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )

datetime = pd.to_datetime(df['Launched Time'])
#datetime = datetime.dt.hour
df['Launched Time'] = datetime
df = df.drop(['Creator ID','Creator','Nickname'], axis=1)

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
df['conversion'] = df['Unit Sales']/df['Viewers']
df['conversion'] = df['conversion'].fillna(0)
df.sort_values(by='Launched Time',inplace=True)
df = df.reset_index(drop=True)

df_norm = df.copy()
for column in df_norm.columns:
    df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min())    
  
x = 'Launched Time'
y = [option,option2]

fig = px.line(df,x=x ,y=option)
fig2 = px.line(df_norm, y=y)
st.plotly_chart(fig)
st.plotly_chart(fig2)