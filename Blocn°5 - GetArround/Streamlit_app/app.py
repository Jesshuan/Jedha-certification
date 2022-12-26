import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

### Config
st.set_page_config(
    page_title="New Feature for delay",
    page_icon=" ",
    layout="wide"
)

DATA_PATH = ('./src/get_around_delay_analysis.xlsx')

### App
st.title("Get Around : study for New Feature")

### usual functions
def import_data():
    data = pd.read_excel(DATA_PATH)
    return data



st.markdown("""
    Here we perform some analysis to explore the impact of the new feature. A new feature in the Get Arround application will not display the future location if it is too close to the previous location, because the previous user is late for checkout. Two parameters:

    the scope: will this new feature be used for the mobile type of check-in? Or only for the connected type?
    the threshold: how long for the minimum time between two rentals?
""")

st.subheader("Load and showcase data")


if st.checkbox('Show raw data'):
    data_load_state = st.text('Loading data...')
    data = import_data()
    data_load_state.text("Data loaded")
    st.subheader('Raw data')
    st.write(import_data())  

st.markdown("""
    ------------------------
""")


