# Question Answering System

## Table of Contents

- [Question Answering System](#question-answering-system)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Clone the repository:](#clone-the-repository)
    - [Manual Setup](#manual-setup)
  - [Docker Setup and Commands](#docker-setup-and-commands)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Manual Setup](#manual-setup-1)
    - [1. Command-Line Interface (CLI)](#1-command-line-interface-cli)
    - [2. Web Interface](#2-web-interface)
  - [Author:](#author)
  - [Acknowledgments](#acknowledgments)

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

- Docker & Docker Compose
- Python 3.10 (for manual setup)
- Elasticsearch (for manual setup)
- Required Python packages (specified in `requirements.txt`)

## Installation

### Clone the repository:

    git clone https://github.com/Kyei-frank/question_answering.git

### Manual Setup

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

## Docker Setup and Commands

To set up the system using Docker:

1. **Build the Docker Image**:

    ```
    docker build -t question_answering -f docker/Dockerfile .
 .
    ```

2. **Run the Docker Container**:

    ```
    docker run -d -p 5000:5000 question_answering
    ```

With these commands, your system will be up and running inside a Docker container, accessible via `http://localhost:5000`.

## Configuration

Set up environment variables for Elasticsearch Cloud:

    export ES_USERNAME=elastic
    export ES_PASSWORD=ElasticsearchPassword
    export ES_CLOUD_ENDPOINT=your-elasticsearch-url.com

You can configure other settings in `config.py` if necessary.

## Usage

### Manual Setup

Run all the required files in the following order to index and retrieve passages:

(Make sure to navigate to the files location "/app")

    python parsing.py
    python model.py
    python indexing.py
    python retrieval.py
    python app.py

### 1. Command-Line Interface (CLI)

Upload documents for indexing via cmd:

    curl -X POST -F "file=@path/to/your/file.csv" http://127.0.0.1:5000/upload

Submit query for response via cmd:

    curl -X POST -H "Content-Type: application/json" -d "{\"question\": \"What case defines what an offer is?\"}" http://localhost:5000/search

To generate a response with `search_script.py` via Terminal:

    python app/search_script.py "what is a case?"

### 2. Web Interface

To use the web interface, run the Flask app:

    python app.py

Then, access the application in your web browser at `http://localhost:5000`.

## Author:
[FK Baffour](https://www.linkedin.com/in/frank-kyei-baffour-403b60100/)

## Acknowledgments

- Kwame AI
- The Sentence Transformers library
- Elasticsearch community