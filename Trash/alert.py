import os
import re
import winsound

# Path to the BB_signals.txt file
file_path = "BB_signals.txt"

# Read the file
with open(file_path, "r") as file:
    signals = file.readlines()

# Extract the last signal
last_signal = signals[-1].strip()

# Check if the last signal is not "Hold"
if last_signal != "Hold":
    # Extract the forex pair from the last signal
    forex_pair = re.findall(r'[A-Z]{6}', last_signal)
    if forex_pair:
        forex_pair = forex_pair[0]
        # Generate a notification alert with the forex pair
        print(f"New signal alert for {forex_pair}!")
        # Play a sound file for the notification
        winsound.PlaySound("path/to/sound/file.wav", winsound.SND_FILENAME)

# Print the last signal
print("Last Signal:", last_signal)
