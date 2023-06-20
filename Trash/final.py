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


# List of file paths
file_paths = ['BB_signals.txt', 'MA_signals.txt', 'MACD_signals.txt', 'RSI_signals.txt']

# Finding forex pairs
forex_pairs = find_forex_pairs(file_paths)

# Printing the forex pairs
print("Forex market pairs:")
for pair in forex_pairs:
    print(f"{pair}\t{signal}\t{from_.txt}\n")

