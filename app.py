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
    st.markdown(f"**Columns:** {df.shape[1]}")
    st.header("Sample data")
    st.dataframe(df.head(10))

    st.header("Missing values summary")
    miss = (df.isna().sum() / len(df)).sort_values(ascending=False)
    miss = miss[miss > 0]
    if not miss.empty:
        st.table(miss)
    else:
        st.write("No missing values detected (in the filtered data).")

    st.header("Basic statistics for numeric columns")
    st.dataframe(df.select_dtypes(include=[np.number]).describe().T)

    st.header("Quick charts")
    col1, col2 = st.columns(2)
    with col1:
        if "Company" is not None :
            top_Company = df['Company'].value_counts().sort_values(ascending=False).head(10).reset_index()
            top_Company.columns = ['Company', 'Count']
            st.bar_chart(top_Company.set_index('Company'))
        else:
            st.write("No 'Company' column detected.")

    with col2:
        if 'Ex-Showroom_Price' in df.columns:
            fig = px.histogram(df, x='Ex-Showroom_Price', title="Price Distribution")
            st.plotly_chart(fig)

