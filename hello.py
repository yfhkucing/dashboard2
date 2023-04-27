import streamlit as st
import pandas as pd 
import os

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Feyrely dashboard! 👋")

st.sidebar.success("Select a menu above.")

st.markdown(
    """
    still under construction, updates are underway
    
    """ )

#path2 = 'data/core_stats'
#def save_uploadedfile(uploadedfile,path):
#     with open(os.path.join(path,uploadedfile.name),"wb") as f:
#         f.write(uploadedfile.getbuffer())
#     return st.success("Saved File:{} to core_stats".format(uploadedfile.name))

#datafile = st.file_uploader("Upload core statistic",type=['xlsx'])
#if datafile is not None:
#   file_details = {"FileName":datafile.name,"FileType":datafile.type}
#   df  = pd.read_excel(datafile)
#   st.dataframe(df)
#   save_uploadedfile(datafile,path2)