import json
import ta as talib
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import pytz
from ta.volatility import BollingerBands

# Check if today is Saturday or Sunday
today = datetime.now().date()
if today.weekday() in [5, 6]:  # 5 represents Saturday and 6 represents Sunday
    print("Sorry, the markets are closed today. Try again on Monday. Enjoy your weekend")
else:
    # Read forex pairs from JSON file
    with open('forex_pairs.json', 'r') as file:
        forex_pairs = json.load(file)

    # Define the time frame and time zone
    timeframe = '1h'
    timezone = 'Africa/Nairobi'

    # Define the number of periods for Moving Average calculation
    period = 500

    # Define the number of standard deviations for Bollinger Bands calculation
    bb_period = 20
    bb_dev = 2

    # Get the current time in Kenya time zone
    kenya_tz = pytz.timezone(timezone)
    current_time = datetime.now(kenya_tz)

    # Define the start and end times for data retrieval
    end_time = current_time
    start_time = current_time - timedelta(hours=period)
    print(f"start_time: {start_time.strftime('%Y-%m-%d')}\nEnd_time: {end_time}")

    # Save the signals to a file
    filename = 'BB_signals.txt'
    with open(filename, 'w') as file:
        file.write(f"Today: {end_time}\n\n")

        # Generate MACD signals for each forex pair
        for pair in forex_pairs:
            timeframe = '1h'
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

            # Get the closing prices for the pair
            prices = data['Close'].values

            # Convert prices array to a Pandas DataFrame
            df = pd.DataFrame(prices, columns=['Close'])

            # Check if the DataFrame has data
            if not df.empty and len(df) >= 1:
                # Calculate the middle band (SMA) and standard deviation
                n = 20  # Number of periods for calculations
                k = 2   # Number of standard deviations
                middle_band = df['Close'].rolling(window=n).mean()
                standard_deviation = df['Close'].rolling(window=n).std()

                # Calculate the upper and lower bands
                upper_band = middle_band + (k * standard_deviation)
                lower_band = middle_band - (k * standard_deviation)

                # Determine the buy, sell, or hold signal
                last_price = df['Close'].iloc[-1]
                last_upper_band = upper_band.iloc[-1]
                last_lower_band = lower_band.iloc[-1]

                # Declare and assign initial value to rounded_number
                entry_price = last_price  # Replace with your actual entry price
                lot_size = 0.01  # Replace with your actual lot size
                # Define risk-reward ratios
                take_profit_ratio = 0.002  # 0.2%
                stop_loss_ratio = 0.001  # 0.1%
                if last_price > last_upper_band:
                    signal = "Sell"
                elif last_price < last_lower_band:
                    signal = "Buy"
                else:
                    signal = "Hold"

                if signal == "Sell":
                    current_price = last_price
                    take_profit = current_price - (current_price * take_profit_ratio)
                elif signal == "Buy":
                    current_price = last_price
                    take_profit = current_price + (current_price * take_profit_ratio)
                else:
                    take_profit = 0.0

                rounded_number = round(take_profit, 6)

                # Save the signals to a file
                if rounded_number is not None:
                    file.write(f"BB Signals for {pair} ({timeframe} timeframe): {signal} Take Profit at: {rounded_number}\n")
                else:
                    file.write(f"BB Signals for {pair} ({timeframe} timeframe): {signal}\n")

            else:
                print("No data available to generate a signal.")