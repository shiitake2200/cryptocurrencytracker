import streamlit as st
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
@st.cache_data
def fetch_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 50}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Failed to fetch data from CoinGecko API")
        return pd.DataFrame()

# App Title and Description
st.title("Cryptocurrency Tracker")
st.info("Track real-time cryptocurrency prices, trends, and market insights.")

# Sidebar Navigation
st.sidebar.header("Navigation")
selected_section = st.sidebar.radio("Go to:", ["Overview", "Price Trends", "Global Market"])

# Fetch data
crypto_data = fetch_data()

# Section 1: Overview
if selected_section == "Overview":
    st.subheader("Cryptocurrency Overview")

    # Interactive Table
    search_coin = st.text_input("Search for a cryptocurrency:", "")
    if search_coin:
        filtered_data = crypto_data[crypto_data['name'].str.contains(search_coin, case=False)]
    else:
        filtered_data = crypto_data

    st.dataframe(filtered_data[['name', 'symbol', 'current_price', 'market_cap', 'total_volume']])

    # Button Widget
    if st.button("Refresh Data"):
        crypto_data = fetch_data()
        st.success("Data refreshed successfully!")

# Section 2: Price Trends
elif selected_section == "Price Trends":
    st.subheader("Price Trends")

    # Selectbox for Cryptocurrency
    selected_coin = st.selectbox("Choose a cryptocurrency:", crypto_data['name'])
    coin_data = crypto_data[crypto_data['name'] == selected_coin]

    if not coin_data.empty:
        # Simulated data for historical trends
        trend_data = pd.DataFrame({
            'Timestamp': pd.date_range(start='2023-12-01', periods=10, freq='D'),
            'Price': np.random.uniform(low=coin_data.iloc[0]['current_price'] * 0.9,
                                        high=coin_data.iloc[0]['current_price'] * 1.1, size=10),
            'Market Cap': np.random.uniform(low=coin_data.iloc[0]['market_cap'] * 0.9,
                                            high=coin_data.iloc[0]['market_cap'] * 1.1, size=10)
        })

        # Line Chart
        fig, ax = plt.subplots()
        ax.plot(trend_data['Timestamp'], trend_data['Price'], label='Price', marker='o')
        ax.set_title(f"Price Trend for {selected_coin}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        st.pyplot(fig)

        # Area Chart
        fig, ax = plt.subplots()
        ax.fill_between(trend_data['Timestamp'], trend_data['Market Cap'], color='skyblue', alpha=0.5)
        ax.set_title(f"Market Cap Trend for {selected_coin}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Market Cap (USD)")
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected cryptocurrency.")

# Section 3: Global Market
elif selected_section == "Global Market":
    st.subheader("Global Market Insights")

    # Map with random data
    map_data = pd.DataFrame({
        'lat': np.random.uniform(-90, 90, 10),
        'lon': np.random.uniform(-180, 180, 10)
    })
    st.map(map_data)

    # Checkbox
    if st.checkbox("Show Market Details"):
        st.write(crypto_data.describe())

# Widgets and Feedback Boxes
st.sidebar.success("App loaded successfully!")
st.sidebar.warning("Data may be outdated if not refreshed.")
