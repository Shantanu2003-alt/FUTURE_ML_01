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
st.set_page_config(page_title="Rossmann Sales Forecasting", layout="wide")
st.title("📈 Rossmann Sales Forecasting Dashboard")

# ============================
# LOAD COMPRESSED DATA
# ============================
@st.cache_data
def load_data():
    with zipfile.ZipFile("train.zip") as z:
        with z.open("train.csv") as f:
            train = pd.read_csv(f)
    with zipfile.ZipFile("store.zip") as z:
        with z.open("store.csv") as f:
            store = pd.read_csv(f)

    data = pd.merge(train, store, on="Store")
    data["Date"] = pd.to_datetime(data["Date"])
    data = data[(data["Open"] == 1) & (data["Sales"] > 0)]
    data.fillna(method="ffill", inplace=True)
    data["Month"] = data["Date"].dt.month
    data["Year"] = data["Date"].dt.year
    data["DayOfWeek"] = data["Date"].dt.dayofweek
    return data

data = load_data()

# ============================
# FILTERS: Region / Store
# ============================
st.sidebar.header("🔍 Filter Data")
store_ids = st.sidebar.multiselect("Select Store IDs", options=sorted(data["Store"].unique()), default=sorted(data["Store"].unique())[:5])
states = st.sidebar.multiselect("Select Regions (StateHoliday)", options=data["StateHoliday"].unique(), default=data["StateHoliday"].unique())

filtered = data[data["Store"].isin(store_ids) & data["StateHoliday"].isin(states)]

st.write(f"✅ Showing data for {len(filtered)} records.")

# ============================
# EXPORT FILTERED DATA
# ============================
st.sidebar.download_button(
    label="📥 Download Filtered CSV",
    data=filtered.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ============================
# FORECAST WITH PROPHET
# ============================
st.subheader("🔮 Total Sales Forecast")

df_prophet = filtered.groupby("Date")["Sales"].sum().reset_index()
df_prophet.columns = ["ds", "y"]

model = Prophet()
model.fit(df_prophet)

future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

fig1 = model.plot(forecast)
plt.title("📈 Total Sales Forecast (Actual vs Predicted)")
plt.tight_layout()
plt.savefig("forecast_chart.png")
st.pyplot(fig1)

st.download_button(
    label="📤 Download Forecast Chart",
    data=open("forecast_chart.png", "rb"),
    file_name="forecast_chart.png",
    mime="image/png"
)

# ============================
# MONTHLY TRENDS
# ============================
st.subheader("📆 Monthly Sales Trend")
monthly = filtered.groupby(["Year", "Month"])["Sales"].sum().reset_index()
monthly["YearMonth"] = pd.to_datetime(monthly["Year"].astype(str) + "-" + monthly["Month"].astype(str))

plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly, x="YearMonth", y="Sales")
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend")
plt.tight_layout()
plt.savefig("monthly_trend.png")
st.pyplot(plt)

st.download_button(
    label="📤 Download Monthly Trend",
    data=open("monthly_trend.png", "rb"),
    file_name="monthly_trend.png",
    mime="image/png"
)

# ============================
# CATEGORY FILTERED GRAPHS
# ============================
st.subheader("📊 Category Comparisons")

col1, col2, col3 = st.columns(3)

with col1:
    fig = px.line(filtered.groupby(["StoreType", "Date"])["Sales"].mean().reset_index(), x="Date", y="Sales", color="StoreType", title="🏪 Avg Sales by Store Type")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.line(filtered.groupby(["Assortment", "Date"])["Sales"].mean().reset_index(), x="Date", y="Sales", color="Assortment", title="📦 Avg Sales by Assortment")
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    fig3 = px.line(filtered.groupby(["Promo", "Date"])["Sales"].mean().reset_index(), x="Date", y="Sales", color="Promo", title="🎯 Promo Impact on Sales")
    st.plotly_chart(fig3, use_container_width=True)

# ============================
# INSIGHT TABLES
# ============================
st.subheader("🏆 Performance Insights")

top_stores = filtered.groupby("Store")["Sales"].sum().sort_values(ascending=False).head(10)
low_months = filtered.groupby("Month")["Sales"].mean().sort_values().head()

col4, col5 = st.columns(2)

with col4:
    st.markdown("**Top 10 Stores by Sales**")
    st.dataframe(top_stores)

with col5:
    st.markdown("**Lowest Performing Months**")
    st.dataframe(low_months)

# ============================
# KPIs
# ============================
st.subheader("📌 KPI Dashboard")
total_sales = filtered["Sales"].sum()
avg_daily_sales = filtered.groupby("Date")["Sales"].sum().mean()
best_month = filtered.groupby("Month")["Sales"].sum().idxmax()
top_store = filtered.groupby("Store")["Sales"].sum().idxmax()

k1, k2, k3, k4 = st.columns(4)
k1.metric("📈 Total Sales", f"{total_sales:,.0f}")
k2.metric("📅 Avg Daily Sales", f"{avg_daily_sales:,.2f}")
k3.metric("🏆 Best Month", str(best_month))
k4.metric("🏪 Top Store ID", int(top_store))

# ============================
# EXPORT FORECAST CSV
# ============================
forecast.to_csv("rossmann_forecast.csv", index=False)
st.download_button(
    label="📁 Download Forecast CSV",
    data=open("rossmann_forecast.csv", "rb"),
    file_name="rossmann_forecast.csv",
    mime="text/csv"
)
