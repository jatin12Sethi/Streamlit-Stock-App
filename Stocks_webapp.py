import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date

# Title of the app
st.title('Stock Price Visualization')

# Input field for user name
name = st.text_input("Enter your name")

# Input field for stock ticker symbol
ticker_input = st.text_input("Enter the stock ticker symbol (e.g., AAPL for Apple)")

# Date inputs for selecting the start and end dates
start_date = st.date_input("Select the start date", value=date(2020, 5, 31))
end_date = st.date_input("Select the end date", value=date(2024, 2, 15))

# Display visualize button
if st.button("Visualize"):
    if name and ticker_input and start_date and end_date:
        
        if start_date < end_date:
            # Fetch the stock data
            tickerData = yf.Ticker(ticker_input)
            tickerDF = tickerData.history(start=start_date, end=end_date)

            
            st.write(f"Hello {name}, here are the stock closing prices and volumes for {ticker_input}!")

            # Plot the closing price
            st.write("""## Closing Price""")
            st.line_chart(tickerDF.Close)

            # Plot the volume
            st.write("""## Volume Price""")
            st.line_chart(tickerDF.Volume)
        else:
            st.write("Error: End date must be after start date.")
    else:
        st.write("Please enter your name, a valid stock ticker symbol, and select both start and end dates.")
