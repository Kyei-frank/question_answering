import os
import csv
import json
from elasticsearch import Elasticsearch, exceptions
from sentence_transformers import SentenceTransformer

class ElasticSearchIndexer:
    def __init__(self):
        # Load the SentenceTransformer model for generating embeddings
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        # Define the name of the Elasticsearch index
        self.index_name = "passage_index"
        
        # Initialize Elasticsearch connection and setup
        self.setup_elasticsearch()

        # Specify the path to the CSV file containing passage, metadata, and embeddings
        self.csv_file_path = "docs\passage_metadata_emb.csv"

    def setup_elasticsearch(self):
        """Establish connection with Elasticsearch and set up the index."""
        # Set environment variables for Elasticsearch credentials and endpoint
        # Note: It is recommended to use secure means such as environment variables or config files to store credentials
        os.environ['ES_USERNAME'] = 'elastic'
        os.environ['ES_PASSWORD'] = 'M7JmMggiaAX76LulPu2OuQT3'
        os.environ['ES_CLOUD_ENDPOINT'] = 'https://my-deployment-f4fc58.es.us-central1.gcp.cloud.es.io'
        
        # Retrieve Elasticsearch credentials and endpoint from environment variables
        es_cloud_endpoint = os.getenv("ES_CLOUD_ENDPOINT")
        es_username = os.getenv("ES_USERNAME")
        es_password = os.getenv("ES_PASSWORD")
        
        # Attempt to establish a connection to Elasticsearch Cloud
        try:
            self.es = Elasticsearch(es_cloud_endpoint, http_auth=(es_username, es_password))
        except exceptions.ConnectionError as e:
            print(f"Error connecting to Elasticsearch: {e}")
            exit()

    def create_update_index(self):
        """Create or update the Elasticsearch index with the specified mapping."""
        # Define the settings and mappings for the Elasticsearch index
        mapping = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "Passage": {"type": "text"},
                    "Metadata": {"type": "nested"},
                    "Embedding": {"type": "dense_vector", "dims": 384}
                }
            }
        }
        
        # Check if the index already exists
        if self.es.indices.exists(index=self.index_name):
            # Update the mapping of the existing index
            self.es.indices.put_mapping(index=self.index_name, body=mapping['mappings'])
        else:
            # Create a new index with the specified settings and mappings
            self.es.indices.create(index=self.index_name, settings=mapping['settings'])
            self.es.indices.put_mapping(index=self.index_name, body=mapping['mappings'])

    def index_data(self):
        """Index data from the specified CSV file into Elasticsearch."""
        # Open the CSV file and read the content
        with open(self.csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # Iterate through each row in the CSV and index it to Elasticsearch
            for row in csv_reader:
                document = {
                    "Passage": row["Passage"],
                    "Metadata": json.loads(row["Metadata"]),
                    "Embedding": [float(x) for x in row["Embedding"].strip('[]').split(',')]
                }
                self.es.index(index=self.index_name, document=document)

        # Retrieve and print the count of documents in the index
        doc_count = self.es.count(index=self.index_name)['count']
        print(f"Indexing completed. Number of documents indexed: {doc_count}")

    def run(self):
        """Execute the indexing process."""
        self.create_update_index()
        self.index_data()


# Main execution
if __name__ == "__main__":
    # Instantiate the ElasticSearchIndexer class and run the indexer
    indexer = ElasticSearchIndexer()
    indexer.run()
