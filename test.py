import json # Importing the json module to work with JSON data
import os # Importing the os module for interacting with the OS
from tqdm import tqdm # Importing tqdm for progress bar

# Defining a function named 'sample_json' that takes four parameters:
# 'input file' - the path to the input JSON file
# 'output file' - the path to the output JSON file
# 'target size gb' - the target size of the output file in gigabytes
# 'filter key' - the key to filter records by, default is 'also_buy'
def sample_json(input_file, output_file, target_size_gb, filter_key='also_buy'):
    # Convert the target size from gigabytes to bytes
    target_size_bytes = target_size_gb * 1024 ** 5
    # Initialize the current size of the output file in bytes
    current_size_bytes = 0

    # Open the input file in read mode and the output file in write mode
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        # Loop over each line in the input file
        for line in tqdm(infile): # Wrap infile with tqdm for progress bar
            # Load the JSON data from the current line
            record = json.loads(line)
            # Check if the filter key exists and is not empty in the current record
            if record.get(filter_key):
                # If it exists, write the record to the output file and add a newline
                outfile.write(json.dumps(record) + '\n')
            # Add the size of the current line to the current size of the output file
            current_size_bytes += len(line.encode('utf-8'))

            # If the current size of the output file is greater than or equal to the target size
            if current_size_bytes >= target_size_bytes:
                # Stop writing to the output file
                break

    # Print the final size of the output file in gigabytes
    print(f"Finished sampling. Output size: {current_size_bytes / 1024 ** 3 :.2f} GB")

sample_json('Sampled_Amazon_Meta.json', 'Sampled_Amazon_Meta_2.json', 15)
