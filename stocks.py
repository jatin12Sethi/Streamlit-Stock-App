import pandas as pd
import requests
import matplotlib.pyplot as plt
import mplcursors

def fetch_and_visualize_equity_data(equity_symbol):
    # Replace 'demo' with your own API key from Alpha Vantage
    api_key = '9C5U3UWV75IMQ28R'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={equity_symbol}&apikey={api_key}'
    
    print(f"Fetching data for {equity_symbol}...")
    r = requests.get(url)
    data = r.json()
    
    if "Time Series (Daily)" not in data:
        print("Error: Unable to fetch data. Please check the equity symbol or API key.")
        return
    
    time_series_data = data.get('Time Series (Daily)', {})

    # Create an empty list to store the processed data
    formatted_data = []

    # Iterate through each date and extract relevant details
    for date, values in time_series_data.items():
        formatted_data.append({
            'date': date,
            'open': float(values['1. open']),
            'high': float(values['2. high']),
            'low': float(values['3. low']),
            'close': float(values['4. close']),
            'volume': int(values['5. volume'])
        })

    # Create a DataFrame from the formatted data
    df = pd.DataFrame(formatted_data)
    
    # Optionally, set the 'date' column as the index
    df.set_index('date', inplace=True)
    
    # Convert date index to datetime format
    df.index = pd.to_datetime(df.index)
    
    print(f"Data for {equity_symbol} fetched successfully. Visualizing...")

    # Plotting the data
    plt.figure(figsize=(14, 7))

    # Plotting the opening and closing prices with markers
    ax1 = plt.subplot(2, 1, 1)
    line1, = plt.plot(df.index, df['open'], label='Opening Price', color='green', marker='o', markevery=7, markersize=5)
    line2, = plt.plot(df.index, df['close'], label='Closing Price', color='blue', marker='o', markevery=7, markersize=5)
    plt.title(f'{equity_symbol} Opening and Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.grid(True)
    plt.legend()

    # Add interactive cursor to the line plot for opening prices
    cursor1 = mplcursors.cursor(line1, hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(f"{df.index[sel.target.index].date()}\nOpen: ${df['open'][sel.target.index]:.2f}"))

    # Add interactive cursor to the line plot for closing prices
    cursor2 = mplcursors.cursor(line2, hover=True)
    cursor2.connect("add", lambda sel: sel.annotation.set_text(f"{df.index[sel.target.index].date()}\nClose: ${df['close'][sel.target.index]:.2f}"))

    # Plotting the volume
    ax2 = plt.subplot(2, 1, 2)
    bars = plt.bar(df.index, df['volume'], label='Volume', color='orange')
    plt.title(f'{equity_symbol} Trading Volume')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.grid(True)
    plt.legend()

    # Add interactive cursor to the bar plot
    cursor3 = mplcursors.cursor(bars, hover=True)
    cursor3.connect("add", lambda sel: sel.annotation.set_text(f"{df.index[sel.target.index].date()}\nVolume: {df['volume'][sel.target.index]}"))

    plt.tight_layout()
    plt.show()

# Get the equity symbol from the user
equity_symbol = input("Enter the equity symbol: ")
fetch_and_visualize_equity_data(equity_symbol)
