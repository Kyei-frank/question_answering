# Question Answering System

## Table of Contents

1. [Project Description](#project-description)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
    - [Command-Line Interface (CLI)](#command-line-interface-cli)
    - [Web Interface](#web-interface)

6. [Authors](#authors)
7. [Acknowledgments](#acknowledgments)

## Project Description

The Question Answering System is a Python application designed to streamline information retrieval and question-answering tasks. This system harnesses the power of Elasticsearch and Sentence Transformers, making it capable of retrieving precise answers from a vast repository of textual data.

Key Components:
- **Sentence Transformers**: Employs advanced models to generate text embeddings.
- **Elasticsearch**: Serves as a reliable vector store for efficient data retrieval.
- **Docker**: Provides seamless containerization and deployment capabilities.
- **Flask**: Powers the user-friendly API for effortless interaction.

The primary objective is to create a robust and user-friendly question-answering (QA) machine learning system. It excels at interpreting user queries, searching for pertinent information within a given dataset, and presenting accurate answers.




## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10
- Elasticsearch
- Required Python packages (specified in `requirements.txt`)

## Installation
For manual installation, you need to have [`Python3`](https://www.python.org/) on your system. Then you can clone this repo and being at the repo's `root : question_answering>`  follow the steps below:
### Clone the repository:

    git clone https://github.com/Kyei-frank/question_answering.git



Windows:

    python -m venv venv
    venv\Scripts\activate
    python -m pip install -q --upgrade pip
    python -m pip install -qr requirements.txt
    
Linux & macOS:

    python3 -m venv venv
    source venv/bin/activate
    python -m pip install -q --upgrade pip
    python -m pip install -qr requirements.txt
Note: macOS users may need to install Xcode if there are issues.


## Configuration
Set up environment variables for Elasticsearch Cloud:

    export ES_USERNAME=elastic
    export ES_PASSWORD=ElasticsearchPassword
    export ES_CLOUD_ENDPOINTyour-elasticsearch-url.com

You can configure other settings in config.py if necessary.

## Usage

Run all the required files in the following order to index and retrieve passages:

(Make sure to navigate to the the files location "/app")

    python parsing.py
    python model.py
    python indexing.py
    python retrrieval.py
    python app.py
You can test or run queries via:
### 1. Command-Line Interface (CLI)
To run the Question Answering System from the command line, use the following command:

Upload documents for indexing via cmd:

    curl -X POST -H "Content-Type: application/json" -d "{\"question\": \"What case defines what an offer is?\"}" http://localhost:5000/search

Submit query for response via cmd:

    curl -X POST -F "file=@path/to/your/file.txt" http://127.0.0.1:5000/upload

To generate response with search_script.py via Terminal:

    python app/search_script.py "what is a case?"

### 2. Web Interface
To use the web interface, run the Flask app:

    python app.py

Access the application in your web browser at 

    http://localhost:5000.


## Author:
[FK Baffour](https://www.linkedin.com/in/frank-kyei-baffour-403b60100/)

## Acknowledgments
The Sentence Transformers library

Elasticsearch community
