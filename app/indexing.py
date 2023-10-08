import os
import csv
import json
from elasticsearch import Elasticsearch, exceptions, helpers
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
        # Retrieve Elasticsearch credentials and endpoint from environment variables
        es_cloud_endpoint = os.getenv("ES_CLOUD_ENDPOINT", 'https://my-deployment-f4fc58.es.us-central1.gcp.cloud.es.io')
        es_username = os.getenv("ES_USERNAME", 'elastic')
        es_password = os.getenv("ES_PASSWORD", 'M7JmMggiaAX76LulPu2OuQT3')
        
        # Attempt to establish a connection to Elasticsearch Cloud
        try:
            self.es = Elasticsearch(es_cloud_endpoint, http_auth=(es_username, es_password))
        except exceptions.ConnectionError as e:
            print(f"Error connecting to Elasticsearch: {e}")
            exit()

    def create_update_index(self):
        """Create or update the Elasticsearch index with the specified mapping."""
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

    def generate_actions(self):
        """Generate bulk actions for indexing."""
        with open(self.csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if all(key in row for key in ["Passage", "Metadata", "Embedding"]): # Check if the expected columns are present
                    document = {
                        "_index": self.index_name,
                        "_source": {
                            "Passage": row["Passage"],
                            "Metadata": json.loads(row["Metadata"]),
                            "Embedding": [float(x) for x in row["Embedding"].strip('[]').split(',')]
                        }
                    }
                    yield document

    def index_data(self):
        """Index data using the bulk API."""
        try:
            helpers.bulk(self.es, self.generate_actions())
            doc_count = self.es.count(index=self.index_name)['count']
            print(f"Indexing completed. Number of documents indexed: {doc_count}")
        except Exception as e:
            print(f"Error during indexing: {e}")

    def run(self):
        """Execute the indexing process."""
        self.create_update_index()
        self.index_data()

if __name__ == "__main__":
    indexer = ElasticSearchIndexer()
    indexer.run()