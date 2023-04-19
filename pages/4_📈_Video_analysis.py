import pandas as pd
import re
import streamlit as st
import plotly.express as px
columns = ['Video Revenue (Rp)','Unit Sales','Orders','Buyers','Est. commission (Rp)',
           'Refunds (Rp)','Product refunds','CO rate','VV','Likes','Comments','Shares',
           'Product Impressions', 'Product Clicks', 'New followers','CTR']

df = pd.read_excel('data/analisis_konten.xlsx',
                   sheet_name='Sheet1')

def date_range(df):
    df = pd.DataFrame(df.columns)
    df = df.iloc[0]
    return df

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

def dataframe(df):
    df = new_header(df)
    df = df.drop(['Video Info','Video ID'], axis=1)
    return df

def product(df):
    products = df['Products'].dropna()
    products = pd.DataFrame(products.value_counts())
    products = products.rename(columns={"Products": "unit sold"})
    return products

def creator(df):
    creators = pd.DataFrame(df['Creator name'].value_counts())
    return creators.index

def numeric(df):
    for i in range(len(columns)):
        df[columns[i]]= pd.to_numeric(df[columns[i]],errors='coerce')
    return df

def query(df):
    c = creator(df)
    option = st.selectbox('creator',c)
    df = df[df['Creator name'] == option]
    return(df)

def creator_sum(df):
    df = query(df)
    df = numeric(df)
    df = df.drop(['Creator name','Creator ID','Products','CTR',
                      'CO rate','Est. commission (Rp)',
                      'Refunds (Rp)','Product refunds'], axis=1)
    df = df.sum()
    return df

def creator_sum_table(df):
    df = numeric(df)
    df = df.groupby('Creator name').sum().reset_index()
    return(df)

def main(df):
    a = date_range(df)
    date = st.selectbox('Date',a)
    option = st.selectbox('Data option',('raw data','Products sold','creator','creator table'))
    df = dataframe(df)
    products = product(df)
    
    if option == 'raw data':
        st.dataframe(df,use_container_width=True)
    elif option == 'Products sold':
        st.dataframe(products,use_container_width=True)
    elif option == 'creator table':
        st.dataframe(query(df))
    else:
        df = creator_sum_table(df)
        df = df.drop(['CTR','CO rate','Est. commission (Rp)',
                      'Refunds (Rp)','Product refunds'], axis=1)
        df = df.sort_values(by=['Video Revenue (Rp)'],ascending=False)
        df = df.reset_index(drop=True)
        st.dataframe(df)

main(df)