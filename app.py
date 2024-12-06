import pandas as pd
import plotly.express as px  
import streamlit as st 

st.set_page_config(page_title="Sales Data", page_icon=":bar_chart:", layout="wide")

# to read the sheet from the excel file 
df = pd.read_excel(
    io='SalesData.xls',
    engine='xlrd',          # file type 'xls' so used engine 'xlrd'
    sheet_name='SalesData',
    usecols='A:G',
    nrows=5001,
)

df2 = pd.read_excel(
    io='SalesData.xls',
    engine='xlrd',          
    sheet_name='MarketingCosts',
    usecols='A:D',
    nrows=37,
)

# for side bar
st.sidebar.header("Please Filter Here:")

Category = st.sidebar.multiselect(
    "Select the Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

ProductName = st.sidebar.multiselect(
    "Select the ProductName :",
    options=df["ProductName"].unique(),
    default=df["ProductName"].unique()
)


df_selection = df.query(
    "Category == @Category & ProductName ==@ProductName"
)

st.title(":bar_chart: Sales Data")
st.markdown("##")
st.dataframe(df_selection)

st.title(":bar_chart: MarketingCosts ")
st.markdown("##")
st.dataframe(df2)


st.title(":bar_chart: Sales Analysis")
st.markdown("##")

# calculations 
total_sales = int(df_selection["TotalSales"].sum())
total_unitSold  =  int(df_selection["QuantitySold"].sum())
average_order = round(df_selection["QuantitySold"].mean(), 2)
total_marketing_cost = round(df2["Cost"].sum())

Return_onMarketing_Spend = total_marketing_cost / total_sales


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f" ₹ {total_sales:,}")
with middle_column:
  st.subheader(" Return onMarketing Spend:")
  st.subheader(f" {Return_onMarketing_Spend}")
with right_column:
    st.subheader("Average  Order :")
    st.subheader(f" {average_order}")

st.markdown("""---""")

sales_by_productname= df_selection.groupby(by=["ProductName"])[["TotalSales"]].sum().sort_values(by="TotalSales")
fig_total_sales = px.bar(
    sales_by_productname,

    x="TotalSales",
    y=sales_by_productname.index,
    orientation="h",
    title="<b>Sales by Product Name</b>",
    color_discrete_sequence=["#b03217"] * len(sales_by_productname),
    template="plotly_white",
)
fig_total_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_total_sales)
