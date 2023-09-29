import csv
import json
from sentence_transformers import SentenceTransformer
import numpy as np

# Define the path of the input CSV file containing passages and metadata
input_csv = "docs/passage_metadata.csv"

# Define the path of the output CSV file where passages, metadata, and corresponding embeddings will be stored
output_csv = "docs/passage_metadata_emb.csv"

# Load the SentenceTransformers model for generating embeddings
# 'paraphrase-MiniLM-L6-v2' is a lightweight model suitable for generating paraphrasic embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Open the input CSV file in read mode with UTF-8 encoding
with open(input_csv, mode='r', newline='', encoding='utf-8') as csv_input_file:
    reader = csv.DictReader(csv_input_file)
    
    # Open the output CSV file in write mode with UTF-8 encoding
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_output_file:
        # Define the fieldnames for the output CSV file
        fieldnames = ['Passage', 'Metadata', 'Embedding']
        writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames)
        
        # Write the header row to the output CSV file
        writer.writeheader()
        
        # Iterate through each row in the input CSV file
        for row in reader:
            # Extract the passage and metadata from the current row
            passage = row['Passage']
            metadata_str = row['Metadata']
            
            # Generate the embedding for the passage using the loaded model
            embedding = model.encode(passage)
            # Convert the numpy array to a comma-separated string for storing in CSV
            embedding_str = np.array2string(embedding, separator=',', max_line_width=np.inf)
            
            # Write the passage, metadata, and the generated embedding to the output CSV file
            writer.writerow({'Passage': passage, 'Metadata': metadata_str, 'Embedding': embedding_str})
            
            # Determine the number of dimensions in the generated embedding
            num_dimensions = len(embedding)
            
# Print the number of dimensions in the embedding and the path of the output CSV file
print("Number of dimensions in the embedding:", num_dimensions)
print(f"Passage, metadata, and embeddings have been written to {output_csv}")
