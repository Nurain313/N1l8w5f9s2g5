import subprocess
import os
import time

file_paths = ['ma.py', 'bb.py']
start_time = time.time()

while True:
    print('Program running')

    for file_path in file_paths:
        # Specify the relative path to the file
        file_path = os.path.join(os.getcwd(), file_path)

        # Get the directory of the file
        file_dir = os.path.dirname(file_path)

        # Create the subprocess
        proc = subprocess.Popen(['python', file_path], cwd=file_dir, shell=True)

        # Wait for the subprocess to finish
        proc.communicate()

        # Continue with the rest of the loop
        print("Subprocess finished: ", file_path)

    elapsed_time = time.time() - start_time

    if elapsed_time >= 300:  # 5 minutes in seconds
        # Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')

        # Reset the start time
        start_time = time.time()

    print('Running again in 3 minutes')
    time.sleep(180)
