import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

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
    st.markdown("""<div style='text-align: center; font-size: 50px; font-weight: bold; margin: 20px 0;'>
    🚗 Car Dashboard 
    """, unsafe_allow_html=True)
    st.markdown("""<div style = 'text-align: center;'> This dashboard helps you explore the cars dataset and compare models side-by-side.""", unsafe_allow_html=True)

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
    col1,col2= st.columns(2)
    with col1:
        if "Company" is not None :
            plt.figure(figsize=(6, 4))
            df['Company'].value_counts().sort_values(ascending=False).head(10).plot(kind='bar',color ='orange')
            plt.title("Top companies")
            st.pyplot(plt.gcf())
        else:
            st.write("No 'Company' column detected.")
   
    if 'Ex-Showroom_Price' in df.columns and 'Company' in df.columns:
     with col2:
        plt.figure(figsize=(6, 4))
        df.groupby('Company')['Ex-Showroom_Price'].mean().sort_values(ascending=False).head(10).plot(kind='bar', color='orange')
        plt.title("Avg Ex-Showroom Price")
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
    else:
     st.warning("Required columns 'Ex-Showroom_Price' or 'Company' not found in dataset.")

    st.markdown("---")
    st.markdown("**Tip:** Use the 'Cars Explorer' page to filter and find models. Then go to 'Compare Cars' to put two vehicles side-by-side.")






