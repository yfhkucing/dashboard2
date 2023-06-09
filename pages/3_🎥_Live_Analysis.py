import pandas as pd
import re
import streamlit as st
import plotly.express as px
import glob

columns = ['Duration','Revenue (Rp)','Products',	
           'Different Products Sold','Orders Created','Orders Paid',
           'Unit Sales','Buyers','Average Price (Rp)','CO rate',
           'Viewers','Views','ACU','PCU','Avg. Viewing Duration',
           'Comments','Shares','Likes','New Followers','Product Impressions',
           'Product Clicks','CTR']

path = r'data/live_analysis'

def new_header(df):
    New_header = df.iloc[1] #grab the first row for the header
    df = df[2:] #take the data less the header row
    df = df.reset_index(drop=True)
    df.columns = New_header #set the header row as the df header
    return df

def numeric(df):
    for i in range(len(columns)):
        df[columns[i]]= pd.to_numeric(df[columns[i]])
    return df

def duration(df):
    for i in range(len(df)):
        s = df['Duration'][i]
        hm = re.findall("\d+", s) #returns list containing ['hr', 'min']
        hm = [int(x) for x in hm]
        duration = hm[0]*60+hm[1]
        df['Duration'][i] = int(duration)
        df['CO rate'][i] = float(df['CO rate'][i].replace("%", ""))
        df['CTR'][i] = float(df['CTR'][i].replace("%", "")) 
    return df

def show_timeline(df):

    df_norm = df.copy()
    for column in df_norm.columns:
        df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min()) 

    col1, col2, col3 = st.columns(3)

    with col1:
        option = st.selectbox(
            "Select KPI",
            (columns),
        )

    with col2:
        option2 = st.selectbox(
            "Select KPI 2",
            (columns),
        )

    with col3:
        option3 = st.selectbox(
            "Select KPI 3",
            (columns),
        )

    x = 'Launched Time'
    y = [option,option2,option3]

    fig = px.line(df,x=x ,y=option)
    fig2 = px.line(df_norm, y=y)
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

def table(df):
    df = new_header(df)
    df = df.drop(['Creator ID','Creator','Nickname'], axis=1)
    datetime = pd.to_datetime(df['Launched Time'])
    df['Launched Time'] = datetime
    df = duration(df)
    df = numeric(df)
    df['conversion'] = df['Unit Sales']/df['Viewers']
    df['conversion'] = df['conversion'].fillna(0)
    df.sort_values(by='Launched Time',inplace=True)
    df = df.reset_index(drop=True)
    return df

def show_table(df):
    st.dataframe(df)

def main(path):

    all_files = glob.glob(path + "/*.xlsx")
    li = []

    for filename in all_files:
        da = pd.read_excel(filename)
        da = table(da)
        li.append(da)
    df = pd.concat(li)
    df = df.drop_duplicates(df)
    df.sort_values(by='Launched Time',inplace=True)
    df = df.reset_index(drop=True)

    columns.append('conversion')
    option = st.selectbox('Data option',('table','timeline'))
    if option == 'table':
        show_table(df)  
    else:
        show_timeline(df)
    

main(path)