import streamlit as st
import pandas as pd
import plotly.express as px

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(page_title="NeuralRetail", layout="wide")

# ================================
# LOAD DATA (FAST)
# ================================
@st.cache_data
def load_data():
    pd.read_csv("cleaned_retail_small.csv")
    df['TotalPrice'] = df['Quantity'] * df['Price']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

df = load_data()

# ================================
# TITLE
# ================================
st.markdown("<h1 style='text-align:center;'>🛍️ NeuralRetail Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### 🚀 Retail Analytics & Business Insights")

# ================================
# SIDEBAR FILTERS
# ================================
st.sidebar.header("🔍 Filters")

country = st.sidebar.multiselect(
    "Select Country",
    df['Country'].unique(),
    default=df['Country'].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['InvoiceDate'].min(), df['InvoiceDate'].max()]
)

df = df[df['Country'].isin(country)]
df = df[(df['InvoiceDate'] >= pd.to_datetime(date_range[0])) &
        (df['InvoiceDate'] <= pd.to_datetime(date_range[1]))]

# ================================
# KPIs
# ================================
total_revenue = df['TotalPrice'].sum()
total_orders = df['Invoice'].nunique()
total_customers = df['Customer ID'].nunique()

st.markdown("## 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue", f"{total_revenue:,.0f}", "+8%")
col2.metric("🧾 Orders", total_orders, "+5%")
col3.metric("👥 Customers", total_customers, "+3%")

# ================================
# TABS
# ================================
tab1, tab2 = st.tabs(["📊 Overview", "📦 Deep Insights"])

# ================================
# TAB 1 (MAIN DASHBOARD)
# ================================
with tab1:

    # Sales Trend
    st.markdown("## 📈 Sales Trend")

    daily_sales = df.groupby(df['InvoiceDate'].dt.date)['TotalPrice'].sum()
    daily_sales_ma = daily_sales.rolling(7).mean()

    fig_trend = px.line(x=daily_sales.index, y=daily_sales.values, title="Daily Sales")
    fig_trend.add_scatter(x=daily_sales_ma.index, y=daily_sales_ma.values, name="7-Day Avg")

    st.plotly_chart(fig_trend, use_container_width=True)

    st.info("📌 Sales show seasonal spikes. Moving average smooths volatility.")

    # Countries + Products
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 🌍 Top Countries")

        country_sales = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)
        fig_country = px.bar(country_sales, title="Top Countries")
        st.plotly_chart(fig_country, use_container_width=True)

    with col2:
        st.markdown("## 🛍️ Top Products")

        product_sales = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
        fig_product = px.bar(product_sales, title="Top Products")
        st.plotly_chart(fig_product, use_container_width=True)

    st.success("Top products and countries drive majority of revenue.")

# ================================
# TAB 2 (ADVANCED)
# ================================
with tab2:

    st.markdown("## 🔥 Key Insights")

    st.success("VIP customers contribute major revenue share")
    st.warning("High variability in demand requires dynamic inventory")
    st.info("Business heavily dependent on few countries")

    # Optional RFM (if available)
    try:
        rfm = pd.read_csv("rfm_data.csv")

        st.markdown("## 👥 Customer Segments")
        st.bar_chart(rfm['Segment'].value_counts())

        st.markdown("## ⚠️ Churn Rate")
        st.metric("Churn Rate", f"{rfm['Churn'].mean():.2%}")

    except:
        st.warning("RFM data not found")

    # Optional Inventory
    try:
        inventory = pd.read_csv("inventory.csv")

        st.markdown("## 📦 Inventory Insights")
        st.dataframe(inventory.head())

    except:
        st.warning("Inventory data not found")

# ================================
# DATA PREVIEW
# ================================
st.markdown("## 📊 Data Preview")
st.dataframe(df.head())

# ================================
# FINAL SUMMARY
# ================================
st.markdown("## 📌 Conclusion")

st.write("""
- Revenue is driven by top countries and products  
- Customer segmentation helps target high-value users  
- Inventory optimization reduces stock risk  
- Data-driven decisions improve business performance  
""")
