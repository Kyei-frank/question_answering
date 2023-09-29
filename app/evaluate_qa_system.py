import csv
from retrieval import Retrievals  # Import the Retrievals class from retrieval.py

# Initialize the Retrievals class
retrieval = Retrievals()

# Load queries from user_queries.txt
with open("user_queries.txt", "r") as file:
    queries = [line.strip() for line in file.readlines()]

print(f"Queries loaded: {len(queries)}")

# Open the CSV file for writing
with open('evaluation.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row to the CSV file
    writer.writerow(['Question',
                     'Passage 1', 'Relevance Score 1', 'Passage 1 Metadata', 'Is Passage 1 Relevant? (Yes/No)',
                     'Passage 2', 'Relevance Score 2', 'Passage 2 Metadata', 'Is Passage 2 Relevant? (Yes/No)',
                     'Passage 3', 'Relevance Score 3', 'Passage 3 Metadata', 'Is Passage 3 Relevant? (Yes/No)'])

    # Process each query
    for query in queries:
        print(f"Processing query: {query}")

        # Send the query to the server and get the response
        data = retrieval.retrieve_answers([query])  # Call the retrieve_answers method with the current query

        # Initialize manual ratings for the current question
        manual_ratings = [""] * 3

        # Process the data and write to CSV
        if data:
            row = [query]  # Initialize the row with the current question
            for i, result in enumerate(data):
                source = result.get('_source', {})
                row.extend([
                    source.get('Passage', ''),
                    result.get('_score', ''),
                    source.get('Metadata', ''),
                    manual_ratings[i],  # Manually rated field
                ])
            # Write the entire row (for 1 question) to the CSV file
            writer.writerow(row)
        else:
            print("Error occurred: The server response does not contain valid results")
            # Write an error row for the question if desired
            writer.writerow([query] + [""] * 12)  # Write empty values for manual ratings and passages

print("Evaluation CSV file has been generated.")