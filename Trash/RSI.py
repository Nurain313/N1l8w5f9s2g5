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

# Define the time frame and time zone
timeframe = '1h'

# Define the start and end times for data retrieval
end_time = '2023-06-16'
start_time = '2023-06-12'

# Initialize dictionary to store signals for all pairs
all_signals = {}

# Generate MACD signals for each forex pair
for pair in forex_pairs:
    timeframe = '1h'
    symbol = pair + '=X'
    end_time = '2023-06-16'
    start_time = '2023-06-13'
    retry_count = 0
    success = False

    while retry_count < 5 and not success:
        try:
            # Download historical price data using yfinance
            data = yf.download(symbol, start=start_time, end=end_time, interval=timeframe)
            success = True
        except Exception as e:
            print(f"Error downloading data for {pair}: {str(e)}. Retrying... (Attempt {retry_count + 1})")
            retry_count += 1

        if retry_count == 5:
            print(f"Maximum retry limit reached for {pair}. Skipping...")
            break

    if data.empty:
        print(f"No price data found for {pair}")
        continue

    rsi = ta.momentum.RSIIndicator(data['Close']).rsi()
    last_rsi = rsi[len(rsi)-1]
    print(last_rsi)  # Last RSI value
    if last_rsi > 70:
        signal = 'Sell'
    elif last_rsi < 30:
        signal = 'Buy'
    else:
        signal = 'Hold'
    print(signal)
    all_signals[pair] = signal

# Save the signals to a file
filename = 'RSI_signals.txt'
with open(filename, 'w') as file:
    for pair, signal in all_signals.items():
        file.write(f"RSI Signals for {pair} ({timeframe} timeframe):\t")
        file.write(signal + '\n')
