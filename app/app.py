from flask import Flask, request, jsonify, Response
from flask.logging import create_logger
import logging
import os
from retrieval import Retrievals
from indexing import ElasticSearchIndexer
from werkzeug.utils import secure_filename

# Initializing Flask application
app = Flask(__name__)
log = create_logger(app)

# Load configuration settings from environment variable, with a default for development purposes
app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))

# Define the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialization of Retrieval and Indexer instances
retrieval = Retrievals()
indexer = ElasticSearchIndexer()

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    :param filename: Name of the file to check
    :return: True if the file has an allowed extension, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/search', methods=['POST'])
def search():
    """
    Endpoint to handle user questions and return relevant passages.
    It retrieves answers based on the received question.
    """
    data = request.get_json()
    question = data.get('question')
        
    if not question:
        return jsonify({"error": "Question not provided"}), 400
        
    results = retrieval.retrieve_answers([question])
    return jsonify(results), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint to handle file uploads and index them.
    It saves the uploaded file and triggers the indexer.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Assuming the uploaded file contains embeddings, proceed to indexing
        indexer.csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        indexer.run()
        
        return jsonify({"success": "File uploaded and indexed"}), 200
    return jsonify({"error": "File type not allowed"}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    log.error(f"Server error: {e}")
    return jsonify({"error": "Internal server error"}), 500

# Run the Flask application when the script is executed
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
