import argparse
from retrieval import Retrievals  # Import the Retrievals class from retrieval.py

def main():
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description="Search for relevant passages using the QA system")

    # Add a positional argument for the query
    parser.add_argument("query", type=str, help="The query to search for relevant passages")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Initialize the Retrievals class
    retrieval = Retrievals()

    # Send the query to the retrieval system and get the response
    query = args.query
    data = retrieval.retrieve_answers([query])  # Call the retrieve_answers method with the current query

    if data:
        # Print the "Top 5 Relevant Passages" heading
        print("Top 5 Relevant Passages:")

        for i, result in enumerate(data):
            passage = result['_source']['Passage']
            score = result['_score']
            metadata = result['_source']['Metadata']

            # Print each passage with its details
            print("\n" + "=" * 40)  # Add a separator before each passage
            print(f"Passage {i + 1}:")
            print(f"Passage Text: {passage}")
            print(f"Relevance Score: {score}")
            print(f"Metadata: {metadata}")
    else:
        print("Error occurred: The retrieval system did not return valid results")

if __name__ == "__main__":
    main()
