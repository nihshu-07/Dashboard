import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(page_title="Cars Dashboard", layout='wide')

DATA_PATH = "car_cleaned1.csv"  

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

df = load_data()


# sidebar
page = st.sidebar.radio("Choose", ["Home", "Cars Explorer"])

st.sidebar.markdown("---")

if page == "Home":
    st.markdown("""<div style='text-align: center; font-size: 45px; font-weight: bold; margin: 20px 0;font-family: Arial, Helvetica, sans-serif;'>
    🚗 Car Dashboard 
    """, unsafe_allow_html=True)
    st.markdown("""<div style = 'text-align: center;'> This dashboard helps you explore the cars dataset and compare models side-by-side.""", unsafe_allow_html=True)
    

    st.markdown("""<h3>About the Data""",unsafe_allow_html=True)
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
        if "Company" != None :
            fig, ax = plt.subplots(figsize=(8, 8))
            fuel_dist = df['Fuel_Type'].value_counts()
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
            explode = [0.05] * len(fuel_dist)
            wedges, texts, autotexts = ax.pie(fuel_dist.values, labels=fuel_dist.index, autopct='%1.1f%%',
                                                startangle=90, colors=colors, explode=explode,
                                                textprops={'fontsize': 11, 'weight': 'bold'})
            ax.set_title('Fuel Type Distribution', fontsize=14, fontweight='bold', pad=20)
            # Make percentage text white and bold
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_weight('bold')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        else:
            st.write("No 'Company' column detected.")
   
    if 'Ex-Showroom_Price' in df.columns and 'Company' in df.columns:
     with col2:
            fig, ax = plt.subplots(figsize=(10, 9))
            price_by_company = df.groupby('Company')['Ex-Showroom_Price'].mean().sort_values(ascending=False)
            bars = ax.bar(price_by_company.index, price_by_company.values/1000, color='skyblue', edgecolor='white', linewidth=1.5)
            ax.set_xlabel('Company', fontsize=12, fontweight='bold')
            ax.set_ylabel('Average Price (₹ in thousands)', fontsize=12, fontweight='bold')
            ax.set_title('Average Ex-Showroom Price by Company', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
    else:
     st.warning("Required columns 'Ex-Showroom_Price' or 'Company' not found in dataset.")

    st.markdown("---")
    st.markdown("**Tip:** Use the 'Cars Explorer' page to filter and find models. Then go to 'Compare Cars' to put two vehicles side-by-side.")

elif page == "Cars Explorer":
    st.markdown("""<div style='text-align: center; font-size: 45px; font-weight: bold; margin: 20px 0;font-family: Arial, Helvetica, sans-serif;'>
    🔍 Car Explorer 
    """, unsafe_allow_html=True)
    makes = ["All"] + sorted(df["Company"].dropna().unique().tolist())
    sel_makes = st.sidebar.selectbox("Company", makes)

    if sel_makes != "All":
        models = ["All"] + sorted(df[df["Company"] == sel_makes]["Model"].dropna().unique().tolist())
    else:
        models = ["All"] + sorted(df["Model"].dropna().unique().tolist())
    sel_models = st.sidebar.selectbox("Model", models)

        
    apply_filters = st.sidebar.button("Select")

    if apply_filters:
        filtered = df.copy()
        if sel_makes:
            filtered = filtered[filtered["Company"]== sel_makes]
        if sel_models:
            filtered = filtered[filtered["Model"] == sel_models]
        if filtered.empty:
            st.warning("No cars match the selected filters.")
        else:

            st.markdown("""<div style='text-align: center; font-size: 45px; font-weight: bold; margin: 20px 0;font-family: Arial, Helvetica, sans-serif;'>
             📊 Key Metrics
    """, unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                avg_price = filtered['Ex-Showroom_Price'].mean()
                st.metric("Average Price", f"₹{avg_price/1000:.1f}K")

            with col2:
                avg_mileage = filtered['Torque_Value'].mean()
                st.metric("Average Torque", f"{avg_mileage:.1f} NM")

            with col3:
                avg_power = filtered['Power_Value'].mean()
                st.metric("Average Power", f"{avg_power:.0f} HP")

            with col4:
                total_variants = len(filtered)
                st.metric("Total Variants", total_variants)

            st.markdown("---")

            st.subheader("1. Number of Variants per Model")
            st.bar_chart(filtered["Variant"].value_counts())

            st.subheader("2. Drivetrain Distribution")

            drivetrain_counts = filtered["Drivetrain"].value_counts()
            fig, ax = plt.subplots()
            drivetrain_counts.sort_values().plot(kind="barh", color="skyblue", ax=ax)
            ax.set_xlabel("Number of Cars")
            ax.set_ylabel("Drivetrain")
            st.pyplot(fig)

            st.header("3. Price Comparison by Variant")
            if 'Variant' in filtered.columns and len(filtered) > 1:
                fig, ax = plt.subplots(figsize=(12, 5))
                
                # Sort by price
                price_data = filtered.sort_values('Ex-Showroom_Price', ascending=False)
                variants = price_data['Variant'].head(15)  # Top 15 variants
                prices = price_data['Ex-Showroom_Price'].head(15) / 1000
                
                bars = ax.barh(variants, prices, color='skyblue', edgecolor='white', linewidth=1.5)
                ax.set_xlabel('Price (₹ in thousands)', fontsize=12, fontweight='bold')
                ax.set_ylabel('Variant', fontsize=12, fontweight='bold')
                ax.set_title(f'Price Comparison', 
                            fontsize=14, fontweight='bold')
                ax.grid(axis='x', alpha=0.3)
                
                # Add value labels
                for i, (bar, price) in enumerate(zip(bars, prices)):
                    ax.text(price + 1, i, f'₹{price:.1f}K', va='center', fontsize=9)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            else:
                st.info("Not enough variants to compare")

            st.header("4. Torque Comparison by Variant")
            if 'Variant' in filtered.columns and len(filtered) > 1:
                fig, ax = plt.subplots(figsize=(12, 5))
                
                # Sort by mileage
                mileage_data = filtered.sort_values('Torque_Value', ascending=False)
                variants = mileage_data['Variant'].head(15)
                mileages = mileage_data['Torque_Value'].head(15)
                
                bars = ax.barh(variants, mileages, color='limegreen', edgecolor='white', linewidth=1.5)
                ax.set_xlabel('Torque (km/l)', fontsize=12, fontweight='bold')
                ax.set_ylabel('Variant', fontsize=12, fontweight='bold')
                ax.set_title(f'Torque Comparison', 
                            fontsize=14, fontweight='bold')
                ax.grid(axis='x', alpha=0.3)
                
                # Add value labels
                for i, (bar, mileage) in enumerate(zip(bars, mileages)):
                    ax.text(mileage + 0.3, i, f'{mileage:.1f}', va='center', fontsize=9)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            else:
                st.info("Not enough variants to compare")

            st.header("5. Fuel Type Distribution")
            if len(filtered['Fuel_Type'].unique()) > 1:
                fig, ax = plt.subplots(figsize=(8, 8))
                fuel_dist = filtered['Fuel_Type'].value_counts()
                colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
                explode = [0.05] * len(fuel_dist)
                
                wedges, texts, autotexts = ax.pie(fuel_dist.values, labels=fuel_dist.index, 
                                                    autopct='%1.1f%%', startangle=90, 
                                                    colors=colors[:len(fuel_dist)], explode=explode,
                                                    textprops={'fontsize': 11, 'weight': 'bold'})
                ax.set_title(f'Fuel Type Distribution ', 
                            fontsize=14, fontweight='bold', pad=20)
                
                for autotext in autotexts:
                    autotext.set_color('black')
                    autotext.set_weight('bold')
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            else:
                st.info(f"Only one fuel type available: {filtered['Fuel_Type'].iloc[0]}")

            st.header("6. Power vs Torque Analysis")
            if len(filtered) > 1:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                ax.scatter(filtered['Power_Value'], filtered['Torque_Value'],
                        alpha=0.7, s=150, edgecolors='white', linewidth=1.5, 
                        color='#ff69b4')
                
                ax.set_xlabel('Power (HP)', fontsize=12, fontweight='bold')
                ax.set_ylabel('Torque (Nm)', fontsize=12, fontweight='bold')
                ax.set_title(f'Engine Performance ', 
                            fontsize=14, fontweight='bold')
                ax.grid(alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            else:
                st.info("Not enough variants to compare")
            
            st.header("7. Key Features Comparison")
            if 'Variant' in filtered.columns and len(filtered) >= 2:
                fig, ax = plt.subplots(figsize=(12, 6))
                
                # Select top 10 variants by price
                top_variants = filtered.nlargest(10, 'Ex-Showroom_Price')
                
                x = np.arange(len(top_variants))
                width = 0.25
                
                # Normalize values for better visualization
                power_norm = top_variants['Power_Value'] / top_variants['Power_Value'].max() * 100
                torque_norm = top_variants['Torque_Value'] / top_variants['Torque_Value'].max() * 100
                
                bars1 = ax.bar(x - width, power_norm, width, label='Power', 
                            color='#3498db', edgecolor='white', linewidth=1)
                bars2 = ax.bar(x, torque_norm, width, label='Torque', 
                            color='#e74c3c', edgecolor='white', linewidth=1)
                ax.set_xlabel('Variant', fontsize=12, fontweight='bold')
                ax.set_ylabel('Normalized Score (0-100)', fontsize=12, fontweight='bold')
                ax.set_title(f'Normalized Feature Comparison', 
                            fontsize=14, fontweight='bold')
                ax.set_xticks(x)
                ax.set_xticklabels(top_variants['Variant'], rotation=45, ha='right')
                ax.legend()
                ax.grid(axis='y', alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            else:
                st.info("Not enough variants to compare")

            st.header("8. Seating Capacity Distribution")
            if len(filtered['Seating_Capacity'].unique()) > 1:
                fig, ax = plt.subplots(figsize=(8, 5))
                
                seating_dist = filtered['Seating_Capacity'].value_counts().sort_index()
                bars = ax.bar(seating_dist.index, seating_dist.values, 
                            color='purple', edgecolor='white', linewidth=1.5, alpha=0.8)
                
                ax.set_xlabel('Seating Capacity', fontsize=12, fontweight='bold')
                ax.set_ylabel('Count', fontsize=12, fontweight='bold')
                ax.set_title(f'Seating Options ', 
                            fontsize=14, fontweight='bold')
                ax.grid(axis='y', alpha=0.3)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            else:
                st.info(f"All variants have {filtered['Seating_Capacity'].iloc[0]} seats")

            st.header("10. Detailed Data Table")
            st.dataframe(filtered, use_container_width=True, height=400)

            # Download button
            csv = filtered.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name='filtered_data.csv',
                mime='text/csv',
            )

            st.success(f"✅ Showing {len(filtered)} results for your selection!")
                        
    else:
        st.info("Apply filters by clicking the **Select** button on the left.")
