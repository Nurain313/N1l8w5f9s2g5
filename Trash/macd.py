import json
import yfinance as yf
import ta
import pandas as pd

# Read forex pairs from JSON file
with open('forex_pairs.json', 'r') as file:
    forex_pairs = json.load(file)

# Define the timeframe, start time, and end time for data retrieval
timeframe = '1h'
end_time = '2023-06-16'
start_time = '2023-06-12'

# Initialize dictionary to store signals for all pairs
all_signals = {}

# Generate MACD signals for each forex pair
for pair in forex_pairs:
    symbol = pair + '=X'

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

    if not success:
        continue

    if data.empty:
        print(f"No price data found for {pair}")
        continue

    # Calculate MACD values
    macd_indicator = ta.trend.MACD(data['Close'])
    macd = macd_indicator.macd()

    # Generate signals
    #signals = []
    for i in range(1, len(macd)):
        if macd[i] > 0 and macd[i-1] <= 0:
            signal = 'Buy'
        elif macd[i] < 0 and macd[i-1] >= 0:
            signal = 'Sell'
        else:
            signal = 'Hold'

    # Store signals for the pair in the dictionary
    all_signals[pair] = signal
    print(f"MACD Signals for {pair}: {signal}")
# Save all signals to a file
filename = 'MACD_signals.txt'
with open(filename, 'w') as file:
    for pair, signal in all_signals.items():
        file.write(f"MACD Signals for {pair} ({timeframe} timeframe): \t")
        file.write(f"{signal} \n")


