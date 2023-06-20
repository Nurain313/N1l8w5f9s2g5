import re

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def find_forex_pairs(file_paths):
    file_contents = [read_file(file_path) for file_path in file_paths]

    # Initialize forex_pairs with pairs from the first file
    forex_pairs = set(re.findall(r'[A-Z]{6}', file_contents[0]))

    # Iterate over the remaining files and find the intersection of forex_pairs with each file's pairs
    for content in file_contents[1:]:
        pairs = set(re.findall(r'[A-Z]{6}', content))
        forex_pairs = forex_pairs.intersection(pairs)

    return forex_pairs


def extract_signals(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    signals = {}
    for line in lines:
        pair, signal = re.findall(r'([A-Z]{6})\s*:\s*(\w+)', line)[0]
        signals[pair] = signal

    return signals


# List of file paths
file_paths = ['BB_signals.txt', 'MA_signals.txt', 'MACD_signals.txt', 'RSI_signals.txt']

# Finding forex pairs
forex_pairs = find_forex_pairs(file_paths)

# Extracting signals for each pair
signals = {}
for file_path in file_paths:
    file_signals = extract_signals(file_path)
    for pair, signal in file_signals.items():
        if pair in forex_pairs:
            if pair not in signals:
                signals[pair] = {'BB': '', 'MA': '', 'MACD': '', 'RSI': ''}
            signals[pair][file_path[:-4]] = signal

# Printing the forex pairs and their signals
print("Forex market pairs:")
for pair, signal_dict in signals.items():
    signal_list = [signal_dict['BB'], signal_dict['MA'], signal_dict['MACD'], signal_dict['RSI']]
    if signal_list.count('Hold') >= len(signal_list) / 2:
        decision = 'Hold'
    elif signal_list.count('Sell') > signal_list.count('Buy'):
        decision = 'Sell'
    elif signal_list.count('Buy') > signal_list.count('Sell'):
        decision = 'Buy'
    else:
        decision = 'Undecided'
    print(f"Pair: {pair}")
    print(f"Signals: {' | '.join(signal_list)}")
    print(f"Decision: {decision}")
    print()
