import os
import csv
from elasticsearch import Elasticsearch, exceptions
from sentence_transformers import SentenceTransformer

class Retrievals:
    """
    This class handles the retrieval of documents from Elasticsearch 
    based on the similarity of the questions and computes embeddings using Sentence Transformer.
    """

    def __init__(self):
        """
        Initializes the Retrieval class by loading the Sentence Transformer model
        and connecting to Elasticsearch Cloud.
        """
        
        # Load the Sentence Transformer model
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
        # Define Elasticsearch index name
        self.index_name = "passage_index"
        
        # Set environment variables (This should ideally be set through secure means, not hardcoded)
        os.environ['ES_USERNAME'] = 'elastic'
        os.environ['ES_PASSWORD'] = 'JjfCLFlTkozxrjoJI6rgsj2F'
        os.environ['ES_CLOUD_ENDPOINT'] = 'https://my-deployment-eac7ec.es.us-central1.gcp.cloud.es.io'
        
        # Retrieve Elasticsearch Cloud endpoint URL and credentials from environment variables
        es_cloud_endpoint = os.getenv('ES_CLOUD_ENDPOINT', "https://your-default-url.com")
        es_username = os.getenv('ES_USERNAME', "your-default-username")
        es_password = os.getenv('ES_PASSWORD', "your-default-password")

        # Connect to Elasticsearch Cloud
        try:
            self.es = Elasticsearch(es_cloud_endpoint, http_auth=(es_username, es_password))
        except Exception as e:
            print(f"Failed to connect to Elasticsearch: {e}")
            exit()

    def compute_embedding(self, text):
        """
        Computes the embedding for the given text.
        
        :param text: Text for which the embedding is to be computed.
        :return: The computed embedding.
        """
        embedding = self.model.encode(text)
        return embedding.tolist()

    def search_similar_documents(self, query_embedding):
        """
        Searches for documents similar to the given query embedding in Elasticsearch.
        
        :param query_embedding: The embedding of the query.
        :return: The search results.
        """
        
        # Clear the Elasticsearch cache before executing a new query
        # self.es.indices.clear_cache(index=self.index_name)

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
        results = self.es.search(index=self.index_name, body=query)
        return results['hits']['hits']

    def retrieve_answers(self, questions):
        """
        Retrieves answers for the given list of questions and writes the results to a CSV file.
        
        :param questions: List of questions.
        """
        # Prepare the CSV file to save the results
        with open('docs/questions_answers.csv', mode='w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Question', 'Passage 1', 'Relevance Score 1', 'Passage 1 Metadata',
                                 'Passage 2', 'Relevance Score 2', 'Passage 2 Metadata',
                                 'Passage 3', 'Relevance Score 3', 'Passage 3 Metadata'])

            for question in questions:
                # Compute the embedding for the question
                question_embedding = self.compute_embedding(question)
                
                # Search for similar documents
                similar_docs = self.search_similar_documents(question_embedding)
                
                # Write the results to the CSV file
                row = [question]
                for doc in similar_docs:
                    passage = doc['_source']['Passage']
                    score = doc['_score']
                    metadata = doc['_source']['Metadata']
                    row.extend([passage, score, metadata])
                
                # writting to a csv file
                csv_writer.writerow(row)
                
                # Print to the command line
                print(passage)
                
            print("Results have been saved to questions_answers.csv")
            return(similar_docs)
            

# Sample usage
if __name__ == "__main__":
    retriever = Retrievals()
    questions = ["What case defines what an offer is?", "What is a valid offer?", "What are the principles of an injunction"]
    retriever.retrieve_answers(questions)
