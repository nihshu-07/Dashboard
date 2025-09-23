import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Cars Dashboard", layout='wide')

DATA_PATH = "car_cleaned.csv"  

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

df = load_data()
st.write(df.head())

# sidebar
page = st.sidebar.radio("Choose", ["Home", "Cars Explorer", "Compare Cars"])