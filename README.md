# FUTURE_ML_01
A Streamlit-powered application for retail sales forecasting, built on historical data. It leverages Prophet for predictions and provides interactive visualizations of sales trends and key insights. Deploys and analyzes your sales data with ease.

📈 Rossmann Sales Forecasting Dashboard:
This interactive dashboard helps visualize, analyze, and forecast sales data from the Rossmann drugstore chain using Streamlit and Facebook's Prophet model.
It includes filter options, key performance indicators (KPIs), category-based insights, and sales forecasts for better decision-making.

🔧 Technologies Used:
Python (Pandas, NumPy)
Streamlit – Interactive dashboard
Prophet – Time series forecasting
Matplotlib, Seaborn – Static visualizations
Plotly – Interactive charts
pandas – Data manipulation
zipfile – Handling zipped input files

📁 Project Structure:
├── train.zip                # Contains train.csv (main sales data)
├── store.zip                # Contains store.csv (store-related info)
├── dashboard.py            # Streamlit app file
├── forecast_chart.png      # (Generated) Sales forecast chart
├── monthly_trend.png       # (Generated) Monthly trend plot
├── rossmann_forecast.csv   # (Generated) Forecasted sales data
└── README.md               # Project overview and instructions

Datasets Used
📂 1. train.csv (within train.zip)
Daily sales data per store
Promo campaigns
Store open/close status
Dates and holidays

📂 2. store.csv (within store.zip)
Store type
Assortment
Competition and promo details
The datasets are automatically loaded, merged, cleaned, and filtered inside the dashboard application.

📊 Features:
Data Filtering: Filter data by store ID and holiday region.
Forecasting: Forecasts total sales for the next 90 days using Prophet.
Download Options: Export filtered data, forecast charts, and forecast CSVs.
Monthly Trends: View historical trends in sales over months and years.

Category-Based Comparisons:
Store Type vs Sales
Assortment vs Sales
Promotion Impact

Performance Insights:
Top performing stores
Lowest performing months

KPIs:
Total Sales
Average Daily Sales
Best Month
Top Performing Store

Implementation Details:
Multi-select options for Store ID and StateHoliday categories.

🔮 Sales Forecasting:
Facebook Prophet used to forecast total sales for the next 90 days.
Line chart comparing historical vs predicted sales.

📆 Monthly Trends:
Trend line of total monthly sales across years using Seaborn.

📊 Category Analysis
Comparison plots are based on:
Store Type
Assortment
Promotion impact

🏆 Performance Insights:
Top 10 performing stores
Lowest performing months

📌 KPIs Displayed:
Total Sales
Average Daily Sales
Best Month (based on sales)
Top Performing Store

📤 Downloads:
Users can download:
Filtered CSV data
Forecast chart (PNG)
Monthly trend chart (PNG)
Forecast data as CSV

Results and Observations:
Stores with StoreType = a showed consistently higher average sales.
Promotional periods significantly boosted sales across multiple stores.
Prophet's forecasts captured seasonal patterns and general sales growth.
The dashboard made it easy to identify top-performing stores and underperforming time periods quickly.

📥 Downloads:
From within the app, you can download:
Filtered data (filtered_data.csv)
Forecast chart (forecast_chart.png)
Monthly trend chart (monthly_trend.png)
Forecasted sales data (rossmann_forecast.csv)

Results and Observations:
Stores with StoreType = a showed consistently higher average sales.
Promotional periods significantly boosted sales across multiple stores.
Prophet's forecasts captured seasonal patterns and general sales growth.
The dashboard made it easy to identify top-performing stores and underperforming time periods quickly.
