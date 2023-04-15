import streamlit as st
import pandas as pd
import plotly.express as px

columns = ['Income','initial checkout/add to cart','Awareness/impression',
           'Total order','Product sold','SKU sold (varian)','GPM'
           ,'Top Domicile', 'Fav Product','avg. spending per consumer']

columns_core = ['Revenue (Rp)','Shopping Center Revenue','Product Views ',
                'Product Reach','Buyers','Unit Sales','Orders','Refunds (Rp)',
                'Conversion Rate','Visitors','Negative Review Rate','Rate of Returns for Quality Reasons',
                'Complaint Rate','Affiliate revenue (Rp)','Owned media revenue (Rp)']

df = pd.read_excel('data/core_stats.xlsx')

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
    for i in range(len(columns_core)):
        df[columns_core[i]]= pd.to_numeric(df[columns_core[i]],errors='coerce')
    return df

def table(df):
    df = new_header(df)
    datetime = pd.to_datetime(df['Time'])
    df = numeric(df)
    df['Time'] = datetime
    
    df = df.drop(['Refunds (Rp)','Negative Review Rate','Rate of Returns for Quality Reasons',
                'Complaint Rate','Affiliate revenue (Rp)'], axis=1)
    
    df.sort_values(by='Time',inplace=True)
    df = df.reset_index(drop=True)
    st.dataframe(df)

def timeline(df):
    df = new_header(df)
    datetime = pd.to_datetime(df['Time'])
    df['Time'] = datetime
    df = numeric(df)

    df = df.drop(['Refunds (Rp)','Negative Review Rate','Rate of Returns for Quality Reasons',
                'Complaint Rate','Affiliate revenue (Rp)'], axis=1)
    
    df.sort_values(by='Time',inplace=True)
    df = df.reset_index(drop=True)

    df_norm = df.copy()
    for column in df_norm.columns:
        df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min()) 

    col1, col2, col3 = st.columns(3)

    with col1:
        option = st.selectbox(
            "Select KPI",
            (columns_core),
        )

    with col2:
        option2 = st.selectbox(
            "Select KPI 2",
            (columns_core),
        )

    with col3:
        option3 = st.selectbox(
            "Select KPI 3",
            (columns_core),
        )

    x = 'Time'
    y = [option,option2,option3]

    fig = px.line(df,x=x ,y=option)
    fig2 = px.line(df_norm, y=y)
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

def main(df):
 
    option = st.selectbox('Data option',('table','timeline'))
  
    if option == 'table':
        table(df)
    else:
        timeline(df)
    
main(df)