# Save the signals to a file
filename = 'macd_signals.txt'
with open(filename, 'w') as file:
    for pair, signals in all_signals.items():
        file.write(f"MACD Signals for {pair} (1h timeframe):\n")
        file.write(str(signals) + '\n')