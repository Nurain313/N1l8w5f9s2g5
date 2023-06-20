import json
import yfinance as yf
import ta
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import pytz
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

    # Generate MACD signals for each forex pair
    for pair in forex_pairs:
        timeframe = '1h'
        symbol = pair + '=X'
        end_time = '2023-06-16'
        start_time = '2023-06-13'
        data = yf.download(pair, start=start_time.strftime('%Y-%m-%d'), end=end_time.strftime('%Y-%m-%d'), interval=timeframe)

        # Calculate MACD values
        macd_indicator = ta.trend.MACD(data['Close'])
        macd = macd_indicator.macd()

        # Generate signals
        signals = []
        for i in range(len(macd)):
            if macd[i] > 0 and macd[i -1] <= 0:
                signal = 'Buy'
            elif macd[i] < 0 and macd[i -1] >= 0:
                signal = 'Sell'
            else:
                signal = 'Hold'
        # Save the signals to a file
        filename = 'MACD_signals.txt'
        with open(filename, 'w') as file:
            for pair, signals in all_signals.items():
                file.write(f"MACD Signals for {pair} ({timeframe} timeframe):\n")
                file.write(str(signals) + '\n')
        # Output signals
        print(f"MACD Signals for {pair}: {signal}")

