import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title(" Global Superstore Interactive Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('Global_Superstore.csv', encoding="latin1")
    return df

df = load_data()
df = df.dropna()

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
st.sidebar.header("🔍 Filters")
region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique())

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique())

sub_category = st.sidebar.multiselect(
    "Select Sub-Category",
    options=df["Sub-Category"].unique(),
    default=df["Sub-Category"].unique())
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(sub_category))]
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

col1, col2, col3 = st.columns(3)

col1.metric(" Total Sales", f"${total_sales:,.2f}")
col2.metric(" Total Profit", f"${total_profit:,.2f}")
col3.metric(" Orders", filtered_df.shape[0])

st.divider()
st.subheader("🌍 Sales by Region")

sales_region = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig1 = px.bar(
    sales_region,
    x="Region",
    y="Sales",
    color="Region",
    title="Total Sales by Region"
)
st.plotly_chart(fig1, use_container_width=True)
st.subheader("📊 Profit by Category")

profit_cat = filtered_df.groupby("Category")["Profit"].sum().reset_index()

fig2 = px.pie(
    profit_cat,
    names="Category",
    values="Profit",
    title="Profit Distribution by Category"
)
st.plotly_chart(fig2, use_container_width=True)
st.subheader(" Top 5 Customers by Sales")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)
fig3 = px.bar(
    top_customers,
    x="Customer Name",
    y="Sales",
    color="Sales",
    title="Top 5 Customers")
st.plotly_chart(fig3, use_container_width=True)
with st.expander(" View Raw Data"):
    st.dataframe(filtered_df)