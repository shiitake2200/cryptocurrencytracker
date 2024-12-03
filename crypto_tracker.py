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
selected_section = st.sidebar.radio("Go to:", ["Overview", "Price Trends", "Global Crypto Exchange Map"])

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

        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(
            trend_data['Timestamp'], 
            trend_data['Price'], 
            label='Price', 
            marker='o', 
            markersize=5
        )
        ax.set_title(f"Price Trend for {selected_coin}", fontsize=14)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price (USD)", fontsize=12)
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.legend(fontsize=10)
        fig.tight_layout()
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(
            trend_data['Timestamp'], 
            trend_data['Market Cap'], 
            color='skyblue', 
            alpha=0.5
        )
        ax.set_title(f"Market Cap Trend for {selected_coin}", fontsize=14)
        ax.set_xlabel("Date", fontsize=12) 
        ax.set_ylabel("Market Cap (USD)", fontsize=12)
        ax.tick_params(axis='both', which='major', labelsize=10) 
        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected cryptocurrency.")

# Section 3: Global Crypto Exchange Map
elif selected_section == "Global Crypto Exchange Map":
    st.subheader("Global Crypto Exchange Map")

    # Fetch exchange data from CoinGecko
    @st.cache_data
    def fetch_exchanges():
        url = "https://api.coingecko.com/api/v3/exchanges"
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error("Failed to fetch exchange data from CoinGecko.")
            return pd.DataFrame()

    # Get exchange data
    exchanges = fetch_exchanges()

    # Prepare map data
    if not exchanges.empty:
        # Example country centroids for simplicity (use a geocoding API for precise lat/lon)
        country_coordinates = {
    "Cayman Islands": {"lat": 19.3133, "lon": -81.2546},
    "British Virgin Islands": {"lat": 18.4207, "lon": -64.6399},
    "United States": {"lat": 37.0902, "lon": -95.7129},
    "Seychelles": {"lat": -4.6796, "lon": 55.4920},
    "Hong Kong": {"lat": 22.3193, "lon": 114.1694},
    "Bermuda": {"lat": 32.3078, "lon": -64.7505},
    "Panama": {"lat": 8.5380, "lon": -80.7821}
}


        map_data = []
        for _, row in exchanges.iterrows():
            country = row.get("country")
            if country and country in country_coordinates:
                coords = country_coordinates[country]
                map_data.append({"lat": coords["lat"], "lon": coords["lon"], "name": row["name"]})

        # Convert to DataFrame for Streamlit map
        if map_data:
            map_df = pd.DataFrame(map_data)
            st.map(map_df[["lat", "lon"]])
            #st.write(map_df)
        else:
            st.warning("No valid location data available for exchanges.")
    else:
        st.warning("No exchange data available.")

    # Checkbox for detailed exchange data
    if st.checkbox("Show List of Best Global Exchangers"):
        st.write(exchanges[["name", "country", "year_established", "trust_score_rank"]])

# Widgets and Feedback Boxes
st.sidebar.success("App loaded successfully!")
st.sidebar.warning("Data may be outdated if not refreshed.")
