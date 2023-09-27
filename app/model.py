import csv
import json
from sentence_transformers import SentenceTransformer
import numpy as np

# Define the input CSV file
input_csv = "docs/passage_metadata.csv"

# Define the output CSV file
output_csv = "docs/passage_metadata_emb.csv"

# Load the SentenceTransformers model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Open the input CSV file for reading
with open(input_csv, mode='r', newline='', encoding='utf-8') as csv_input_file:
    reader = csv.DictReader(csv_input_file)
    
    # Open the output CSV file for writing
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_output_file:
        fieldnames = ['Passage', 'Metadata', 'Embedding']
        writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames)
        
        # Write the CSV header
        writer.writeheader()
        
        # Loop through each row in the input CSV
        for row in reader:
            # Read the passage and metadata from the input CSV
            passage = row['Passage']
            metadata_str = row['Metadata']
            
            # Generate embedding for the passage
            embedding = model.encode(passage)
            embedding_str = np.array2string(embedding, separator=',', max_line_width=np.inf)
            
            # Write the passage, metadata, and embedding to the output CSV
            writer.writerow({'Passage': passage, 'Metadata': metadata_str, 'Embedding': embedding_str})
            
            # Generating the number of dimensions in the embedding
            num_dimensions = len(embedding)
            
            
print("Number of dimensions in the embedding:", num_dimensions)
print(f"Passage, metadata, and embeddings have been written to {output_csv}")
