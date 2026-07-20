import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration (Sabse upar hona chahiye)
st.set_page_config(page_title="SalesX Pro Dashboard", page_icon="🚀", layout="wide")

# ---------------------------------------------------
# CUSTOM LOGO (HTML/CSS Magic in Sidebar) ✨
# ---------------------------------------------------
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #ff4b4b; margin-bottom: 0px;">🚀 SalesX Pro</h1>
        <p style="color: #b3b3b3; font-size: 14px; margin-top: 5px;">Advanced Analytics Dashboard</p>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Main Page Title
st.title("📊 Sales Performance Dashboard")
st.markdown("---")

# 2. Data Load Karna
@st.cache_data
def load_data():
    df = pd.read_csv('sales_data.csv')
    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR FILTERS ⚙️
# ---------------------------------------------------
st.sidebar.header("Dashboard Filters ⚙️")

region_filter = st.sidebar.multiselect(
    "Select Region", 
    options=df["Region"].unique(), 
    default=df["Region"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category", 
    options=df["Category"].unique(), 
    default=df["Category"].unique()
)

filtered_df = df[(df["Region"].isin(region_filter)) & (df["Category"].isin(category_filter))]

# ---------------------------------------------------
# DOWNLOAD BUTTON (Sidebar mein) 📥
# ---------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Export Data")

@st.cache_data
def convert_df(data):
    return data.to_csv(index=False).encode('utf-8')

csv_data = convert_df(filtered_df)

st.sidebar.download_button(
    label="Download Data (CSV)",
    data=csv_data,
    file_name='sales_report.csv',
    mime='text/csv',
)

# ---------------------------------------------------
# KPIs (Key Performance Indicators)
# ---------------------------------------------------
st.subheader("Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = len(filtered_df)
avg_sales = filtered_df['Sales'].mean() if total_orders > 0 else 0

with col1:
    st.metric(label="Total Sales", value=f"₹{total_sales:,.0f}")
with col2:
    st.metric(label="Total Profit", value=f"₹{total_profit:,.0f}")
with col3:
    st.metric(label="Total Orders", value=total_orders)
with col4:
    st.metric(label="Avg Order Value", value=f"₹{avg_sales:,.0f}")

st.markdown("---")

# ---------------------------------------------------
# CHARTS & VISUALIZATIONS 📈
# ---------------------------------------------------
st.subheader("📈 Sales Visualizations")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    sales_by_category = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_bar = px.bar(
        sales_by_category, 
        x="Category", 
        y="Sales", 
        title="Total Sales by Category", 
        color="Category",
        text_auto='.2s'
    )
    # Chart background transparent karne ke liye
    fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    sales_by_date = filtered_df.groupby("Date")["Sales"].sum().reset_index().sort_values("Date")
    fig_line = px.line(
        sales_by_date, 
        x="Date", 
        y="Sales", 
        title="Daily Sales Trend",
        markers=True
    )
    # Chart background transparent karne ke liye
    fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_line, use_container_width=True)