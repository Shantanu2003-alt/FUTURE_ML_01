import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
from prophet import Prophet
import plotly.express as px
import streamlit as st

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(page_title="Rossmann Forecast Dashboard", layout="wide")
st.title("📈 Rossmann Sales Forecasting Dashboard")

# ============================
# STEP 1: Load ZIP Files
# ============================
@st.cache_data
def load_data_from_zip():
    with zipfile.ZipFile("train.zip") as z:
        with z.open("train.csv") as f:
            train = pd.read_csv(f)
    with zipfile.ZipFile("store.zip") as z:
        with z.open("store.csv") as f:
            store = pd.read_csv(f)
    
    data = pd.merge(train, store, on='Store')
    data['Date'] = pd.to_datetime(data['Date'])
    data = data[(data['Open'] == 1) & (data['Sales'] > 0)]
    data.fillna(method='ffill', inplace=True)
    data['Month'] = data['Date'].dt.month
    data['Year'] = data['Date'].dt.year
    data['DayOfWeek'] = data['Date'].dt.dayofweek
    return data

data = load_data_from_zip()

# ============================
# STEP 2: Forecast with Prophet
# ============================
st.subheader("🔮 Forecast: Total Sales (Actual vs Predicted)")
df_prophet = data.groupby('Date')['Sales'].sum().reset_index()
df_prophet.columns = ['ds', 'y']

model = Prophet()
model.fit(df_prophet)

future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

fig1 = model.plot(forecast)
st.pyplot(fig1)

# ============================
# STEP 3: Monthly & Yearly Comparisons
# ============================
st.subheader("📆 Monthly Sales Trend")
monthly = data.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
monthly['Year-Month'] = pd.to_datetime(monthly['Year'].astype(str) + '-' + monthly['Month'].astype(str))

plt.figure(figsize=(12,6))
sns.lineplot(data=monthly, x='Year-Month', y='Sales')
plt.title("Monthly Sales Trend")
plt.xticks(rotation=45)
plt.ylabel("Sales")
plt.xlabel("Date")
plt.grid(True)
st.pyplot(plt)

# ============================
# STEP 4: Filters & Breakdown
# ============================
st.subheader("📊 Sales by Category")

col1, col2, col3 = st.columns(3)

with col1:
    store_type_sales = data.groupby(['StoreType', 'Date'])['Sales'].mean().reset_index()
    fig = px.line(store_type_sales, x='Date', y='Sales', color='StoreType', title="🏪 Avg Sales by Store Type")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    assortment_sales = data.groupby(['Assortment', 'Date'])['Sales'].mean().reset_index()
    fig2 = px.line(assortment_sales, x='Date', y='Sales', color='Assortment', title="📦 Avg Sales by Assortment")
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    promo_sales = data.groupby(['Promo', 'Date'])['Sales'].mean().reset_index()
    fig3 = px.line(promo_sales, x='Date', y='Sales', color='Promo', title="🎯 Avg Sales: With vs. Without Promo")
    st.plotly_chart(fig3, use_container_width=True)

# ============================
# STEP 5: Top Stores & Low Seasons
# ============================
st.subheader("🏆 Top Performing & Low Season Insights")

top_stores = data.groupby('Store')['Sales'].sum().sort_values(ascending=False).head(10)
low_months = data.groupby('Month')['Sales'].mean().sort_values().head()

col4, col5 = st.columns(2)

with col4:
    st.markdown("**🏪 Top 10 Stores by Total Sales**")
    st.dataframe(top_stores)

with col5:
    st.markdown("**📉 Lowest Performing Months (Avg Sales)**")
    st.dataframe(low_months)

# ============================
# STEP 6: Insight Cards / KPIs
# ============================
st.subheader("📌 Business Insight Cards")

total_sales = data['Sales'].sum()
avg_daily_sales = data.groupby('Date')['Sales'].sum().mean()
best_month = data.groupby('Month')['Sales'].sum().idxmax()
top_store = data.groupby('Store')['Sales'].sum().idxmax()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("📈 Total Sales", f"{total_sales:,.0f}")
kpi2.metric("📅 Avg Daily Sales", f"{avg_daily_sales:,.2f}")
kpi3.metric("🏆 Best Sales Month", str(best_month))
kpi4.metric("🏪 Top Store ID", int(top_store))

# ============================
# STEP 7: Export Forecast CSV (Optional)
# ============================
forecast.to_csv('rossmann_forecast.csv', index=False)
st.success("✅ Forecast saved as 'rossmann_forecast.csv'")
