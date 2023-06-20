import json
import pandas as pd
import yfinance as yf
import pytz
from datetime import datetime, timedelta
import time


# Read forex pairs from JSON file
with open('forex_pairs.json', 'r') as file:
    forex_pairs = json.load(file)

# Define the time frame and time zone
timeframe = '1h'
timezone = 'Africa/Nairobi'

# Define the number of periods for Moving Average calculation
period = 500

# Get the current time in Kenya time zone
kenya_tz = pytz.timezone(timezone)
current_time = datetime.now(kenya_tz)

# Define the start and end times for data retrieval
end_time = current_time
start_time = current_time - timedelta(hours=period)

# Save the signals to a file
filename = 'MA_signals.txt'
with open(filename, 'w') as file:
    file.write(f"Today: {end_time}\n\n")

    # Generate MA signals for each forex pair
    for pair in forex_pairs:
        symbol = pair + '=X'
        retry_count = 0
        success = False
        data = None
        while data is None:
            try:
                # Download historical price data using yfinance
                data = yf.download(symbol, start=start_time, end=end_time, interval=timeframe)
            except Exception as e:
                print("Error occurred:", e)
                print("Retrying...")

        if not data.empty and len(data) >= 1:
            # Extract the 'Close' prices from the downloaded data
            close_prices = data['Close'].tolist()

            # Define the window sizes for the moving averages
            window_short = 20  # Short-term moving average window size
            window_long = 50  # Long-term moving average window size

            # Calculate the moving averages
            moving_avg_short = sum(close_prices[-window_short:]) / window_short
            moving_avg_long = sum(close_prices[-window_long:]) / window_long

            # Get the latest closing price
            latest_price = close_prices[-1]
            entry_price = latest_price  # Replace with your actual entry price
            lot_size = 0.01  # Replace with your actual lot size
            # Define risk-reward ratios
            take_profit_ratio = 0.002  # 0.2%
            stop_loss_ratio = 0.001  # 0.1%
            

            # Determine the buy, sell, or hold signal based on moving average crossovers and price relationship
            if moving_avg_short > moving_avg_long and latest_price > moving_avg_short:
                signal = "Buy"

            elif moving_avg_short < moving_avg_long and latest_price < moving_avg_short:
                signal = "Sell"

            else:
                signal = "Hold"

            if signal == "Sell":
                current_price = latest_price
                take_profit = current_price - (current_price * take_profit_ratio)
            elif signal == "Buy":
                current_price = latest_price
                take_profit = current_price + (current_price * take_profit_ratio)
            else:
                take_profit = 0.0

            rounded_number = round(take_profit, 6)


            file.write(f"MA Signals for {pair} ({timeframe} timeframe): {signal} take_profit: {rounded_number}\n")
        else:
            print("No data available to generate a signal.")
