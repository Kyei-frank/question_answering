import os
import json
import csv
import re

# Define the directory containing the judgment and metadata files
corpus_dir = "../question_answering/corpus"

# Define the output CSV file
output_csv = "docs/passage_metadata.csv"

# Open the CSV file for writing
# Use encoding as utf-8 to support a wide range of characters and newline='' to avoid newline discrepancies across different platforms
with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
    # Define the fieldnames for the CSV file
    fieldnames = ['Passage', 'Metadata']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the CSV header
    writer.writeheader()

    # Loop through each file in the corpus directory
    for filename in os.listdir(corpus_dir):
        # Process only the files ending with "_Technical.txt"
        if filename.endswith("_Technical.txt"):
            # Extract the base filename to match with metadata file
            base_filename = filename.rsplit("_Technical.txt", 1)[0]
            
            # Read the content of the judgment file
            # Use utf-8 encoding to read the file
            with open(os.path.join(corpus_dir, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Extract passages within __paragraph__ markers using regular expressions
                passages = re.findall(r'__paragraph__\n(.*?)\n(?=__paragraph__|$)', content, re.DOTALL)
                
                # Combine all the extracted passages
                combined_passage = ' '.join(passages)
                
                # Split the combined passage into chunks of 5 sentences
                sentences = re.split(r'(?<=[.!?])\s+', combined_passage)
                chunks = [' '.join(sentences[i:i + 5]) for i in range(0, len(sentences), 5)]
                
            # Read the corresponding metadata file
            metadata_file = os.path.join(corpus_dir, f"{base_filename}_Metadata.json")
            with open(metadata_file, 'r', encoding='utf-8') as meta_file:
                metadata = json.load(meta_file)
                
                # Convert the metadata to a JSON string
                metadata_str = json.dumps(metadata)
                
                # Pair each chunk with metadata and write to CSV
                for chunk in chunks:
                    writer.writerow({'Passage': chunk, 'Metadata': metadata_str})

# Print the completion message with the output CSV file name
print(f"Passage and metadata pairings have been written to {output_csv}")
