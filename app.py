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


# sidebar
page = st.sidebar.radio("Choose", ["Home", "Cars Explorer", "Compare Cars"])

st.sidebar.markdown("---")

if page == "Home":
    st.title("🚗 Car Dashboard -- Home")
    st.markdown("This dashboard helps you explore the cars dataset and compare models side-by-side.")

    st.header("About the Data")
    st.markdown(f"**Rows:** {df.shape[0]}")