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
    if request.method == 'POST':
        question = request.form.get('question')
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
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Run the indexer to index the uploaded file
        indexer.run()
        return jsonify({"success": "File uploaded and indexed"}), 200
    return jsonify({"error": "File type not allowed"}), 400

# Run the Flask application when the script is executed
if __name__ == '__main__':
    app.run()
