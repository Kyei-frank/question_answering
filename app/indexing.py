import os
import csv
import json
from elasticsearch import Elasticsearch, exceptions
from sentence_transformers import SentenceTransformer

# Load the Sentence Transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Define Elasticsearch index name
index_name = "passage_index"

# Set environment variables (This should ideally be set through secure means, not hardcoded)
os.environ['ES_USERNAME'] = 'elastic'
os.environ['ES_PASSWORD'] = 'M7JmMggiaAX76LulPu2OuQT3'
os.environ['ES_CLOUD_ENDPOINT'] = 'https://my-deployment-f4fc58.es.us-central1.gcp.cloud.es.io'

# Elasticsearch Cloud endpoint URL and credentials
es_cloud_endpoint = os.getenv("ES_CLOUD_ENDPOINT")
es_username = os.getenv("ES_USERNAME")
es_password = os.getenv("ES_PASSWORD")

# Connect to Elasticsearch Cloud
try:
    es = Elasticsearch(es_cloud_endpoint, http_auth=(es_username, es_password))
except exceptions.ConnectionError as e:
    print(f"Error connecting to Elasticsearch: {e}")
    exit()

# Define index settings and mappings
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

# Create or update the index with the specified mapping
if es.indices.exists(index=index_name):
    es.indices.put_mapping(index=index_name, body=mapping['mappings'])
else:
    # Use API parameters directly for index creation
    es.indices.create(index=index_name, settings=mapping['settings'])
    es.indices.put_mapping(index=index_name, body=mapping['mappings'])

# Specify the path to your CSV file
csv_file_path = "docs\passage_metadata_emb.csv"

# Index the data
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        document = {
            "Passage": row["Passage"],
            "Metadata": json.loads(row["Metadata"]),
            "Embedding": [float(x) for x in row["Embedding"].strip('[]').split(',')]
        }
        es.index(index=index_name, document=document)

# Get the count of documents in the index
doc_count = es.count(index=index_name)['count']
print(f"Indexing completed. Number of documents indexed: {doc_count}")
