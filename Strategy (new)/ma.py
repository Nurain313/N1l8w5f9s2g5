import json
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import pandas as pd
import numpy as np

# Read forex pairs from JSON file
with open('forex_pairs.json', 'r') as file:
    forex_pairs = json.load(file)
# Check if today is Saturday or Sunday
today = datetime.now().date()
if today.weekday() in [5, 6]:  # 5 represents Saturday and 6 represents Sunday
    print("Sorry the markets are closed today. Try again on Monday. Enjoy your weekend.")
else:
    # Define the time frame and time zone
    timeframe = '1h'
    timezone = 'Africa/Nairobi'
    period = 500
    # Get the current time in Kenya time zone
    kenya_tz = pytz.timezone(timezone)
    current_time = datetime.now(kenya_tz)
    # Define the start and end times for data retrieval
    end_time = current_time
    start_time = (current_time - timedelta(hours=period))

    print (f"start_time: {start_time.strftime('%Y-%m-%d')}\nEnd_time: {end_time.strftime('%Y-%m-%d')}")
    # Perform analysis for each forex pair
    for pair in forex_pairs:
        # Download historical data from Yahoo Finance
        symbol = pair + '=X'
        data = yf.download(pair, start=start_time.strftime('%Y-%m-%d'), end=end_time.strftime('%Y-%m-%d'), interval=timeframe)
        print (data)
        # Calculate the 20-period and 50-period moving averages
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['MA50'] = data['Close'].rolling(window=50).mean()
        # Check for potential buy or sell signal
        if not data.empty:
            last_row = data.tail(1)
            if not last_row.empty:
                ma20 = last_row['MA20'].values[0]
                ma50 = last_row['MA50'].values[0]
                close_price = last_row['Close'].values[0]
                # Rest of the code
            else:
                print("No data available for the specified time frame.")
        else:
            print("No data available for the specified forex pair.")


        if ma20 > ma50 and close_price > ma20:
            signal = "Buy"
        elif ma20 < ma50 and close_price < ma20:
            signal = "Sell"
        else:
            signal = "Hold"
        # Save the signals to a file
        filename = 'MA_signals.txt'
        with open(filename, 'w') as file:
            file.write(f"MA Signals for {pair} ({timeframe} timeframe):\n")
            file.write(signal)

        print(f"MA Signals for {pair}: {signal}")
