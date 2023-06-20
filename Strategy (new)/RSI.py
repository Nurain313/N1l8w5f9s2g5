import json
import yfinance as yf
import ta
import pandas as pd
import pytz
from datetime import datetime, timedelta
import numpy as np
import datetime


# Read forex pairs from JSON file
with open('forex_pairs.json', 'r') as file:
    forex_pairs = json.load(file)
# Check if today is Saturday or Sunday
today = datetime.datetime.now().date()
if today.weekday() in [5, 6]:  # 5 represents Saturday and 6 represents Sunday
    print("Sorry the markets are closed today try again on Monday. Enjoy your weekend")
else:
    # Define the time frame and time zone
    timeframe = '1h'
    timezone = 'Africa/Nairobi'
    period = 50
        # Get the current time in Kenya time zone
    kenya_tz = pytz.timezone(timezone)
    current_time = datetime.now(kenya_tz)
    # Define the start and end times for data retrieval
    end_time = current_time
    start_time = (current_time - timedelta(hours=period))
    # Fetching data for each forex pair
    data = {}
    for pair in forex_pairs:
        pair_x = pair + '=X'
        data = yf.download(pair, start=start_time.strftime('%Y-%m-%d'), end=end_time.strftime('%Y-%m-%d'), interval=timeframe)


        rsi = ta.momentum.RSIIndicator(data['Close']).rsi()
        last_rsi = rsi[len(rsi)-1]  # Last RSI value
        if last_rsi > 70:
            signal = 'Sell'
        elif last_rsi < 30:
            signal = 'Buy'
        else:
            signal = 'Hold'
        # Save the signals to a file
        filename = 'RSI_signals.txt'
        with open(filename, 'w') as file:
            for pair, signals in all_signals.items():
                file.write(f"RSI Signals for {pair} ({timeframe} timeframe):\n")
                file.write(str(signals) + '\n')

        print(f"RSI Signals for {pair}: {signal}")

