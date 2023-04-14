import pandas as pd
import re
import streamlit as st
import plotly.express as px
columns = ['Duration','Revenue (Rp)','Products',	
           'Different Products Sold','Orders Created','Orders Paid',
           'Unit Sales','Buyers','Average Price (Rp)','CO rate',
           'Viewers','Views','ACU','PCU','Avg. Viewing Duration',
           'Comments','Shares','Likes','New Followers','Product Impressions',
           'Product Clicks','CTR']

df = pd.read_excel('data/analisis_live.xlsx',
                   sheet_name='Sheet1')
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

def main(df):
    df = new_header(df)
    datetime = pd.to_datetime(df['Launched Time'])
    df['Launched Time'] = datetime
    df = df.drop(['Creator ID','Creator','Nickname'], axis=1)
    df = duration(df)
    df = numeric(df)
    columns.append('conversion')
    df['conversion'] = df['Unit Sales']/df['Viewers']
    df['conversion'] = df['conversion'].fillna(0)
    df.sort_values(by='Launched Time',inplace=True)
    df = df.reset_index(drop=True)
    df['Revenue delta'] = df['Revenue (Rp)'].diff().shift(-1)
    st.dataframe(df)

main(df)