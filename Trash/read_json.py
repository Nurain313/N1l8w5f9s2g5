import json

# Read forex pairs from JSON file
with open('forex_pairs.json', 'r') as file:
    forex_pairs = json.load(file)

print(forex_pairs)

