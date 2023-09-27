import os
import csv
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
except Exception as e:
    print(f"Failed to connect to Elasticsearch: {e}")
    exit()

def compute_embedding(text):
    embedding = model.encode(text)
    return embedding.tolist()

def search_similar_documents(query_embedding):
    query = {
        "size": 3,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_embedding, 'Embedding') + 1.0",
                    "params": {"query_embedding": query_embedding}
                }
            }
        }
    }
    results = es.search(index=index_name, body=query)
    return results['hits']['hits']


# Sample list of questions
questions = ["What case defines what an offer is?",
             "What is a valid offer?",
             "What are the principles of an injunction",
             "What underpins res ipsa loquitor principle",
             "Can the liability of a subsidiary company be extended to a parent company",
             "can you repeat an injunction application in the same court",
             "battery and assault principles",
             "the effect of failure to correct an error apparent on the face of the record of appeal",
             "legal opinion on force majeure",
             "Terms to dissolve a company?"]

# Prepare the CSV file to save the results
with open('docs/questions_answers.csv', mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Question', 'Passage 1', 'Relevance Score 1', 'Passage 1 Metadata',
                         'Passage 2', 'Relevance Score 2', 'Passage 2 Metadata',
                         'Passage 3', 'Relevance Score 3', 'Passage 3 Metadata'])

    for question in questions:
        # Compute the embedding for the question
        question_embedding = compute_embedding(question)
        
        # Search for similar documents
        similar_docs = search_similar_documents(question_embedding)
        
        # Write the results to the CSV file
        row = [question]
        for doc in similar_docs:
            passage = doc['_source']['Passage']
            score = doc['_score']
            metadata = doc['_source']['Metadata']
            row.extend([passage, score, metadata])
        csv_writer.writerow(row)

print("Results have been saved to questions_answers.csv")
