# Question Answering System

## Table of Contents

- [Question Answering System](#question-answering-system)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Clone the repository:](#clone-the-repository)
    - [Manual Setup](#manual-setup)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Manual Setup](#manual-setup-1)
    - [1. Command-Line Interface (CLI)](#1-command-line-interface-cli)
    - [2. Web Interface](#2-web-interface)
  - [Docker Setup](#docker-setup)
    - [Manual Docker Setup and Commands](#manual-docker-setup-and-commands)
    - [Pulling and Running from Docker Hub](#pulling-and-running-from-docker-hub)
  - [Troubleshooting](#troubleshooting)
  - [Versioning](#versioning)
  - [Author:](#author)
  - [Acknowledgments](#acknowledgments)

## Project Description

The Question Answering System is a Python application designed to streamline information retrieval and question-answering tasks. This system harnesses the power of Elasticsearch and Sentence Transformers, making it capable of retrieving precise answers from a vast repository of textual data.

Key Components:
- **Sentence Transformers**: Generates text embeddings.
- **Elasticsearch**: A reliable vector store for data retrieval.
- **Docker**: Ensures seamless containerization and deployment.
- **Flask**: Facilitates user-friendly API interaction.

The primary goal is to create a robust and user-friendly question-answering (QA) machine learning system. It's adept at interpreting user queries, sifting through a dataset for relevant information, and presenting accurate answers.

## Prerequisites

Ensure you have:

- Docker & Docker Compose
- Python 3.10 (for manual setup)
- Elasticsearch (for manual setup)
- Required Python packages (`requirements.txt`)

## Installation

### Clone the repository:

```
git clone https://github.com/Kyei-frank/question_answering.git
```

### Manual Setup

**Windows**:

```
python -m venv venv
venv\Scripts\activate
python -m pip install -q --upgrade pip
python -m pip install -qr requirement.txt
```

**Linux & macOS**:

```
python3 -m venv venv
source venv/bin/activate
python -m pip install -q --upgrade pip
python -m pip install -qr requirements.txt
```

> **Note**: macOS users might need Xcode for certain installations.

## Configuration

Set environment variables for Elasticsearch Cloud:

```
export ES_USERNAME=elastic
export ES_PASSWORD=YourElasticsearchPassword
export ES_CLOUD_ENDPOINT=your-elasticsearch-url.com
```

Further settings can be adjusted in `config.py`.

## Usage

### Manual Setup

Run the necessary files in sequence to index and retrieve passages. Ensure you're in the "/app" directory:

```
python parsing.py
python model.py
python indexing.py
python retrieval.py
python app.py
```

### 1. Command-Line Interface (CLI)

To upload documents for indexing:

```
curl -X POST -F "file=@path/to/your/file.csv" http://localhost:5000/upload
```
>**Note**: Make sure the '@' symbol comes before inserting your file path*


For responses to queries:

```
curl -X POST -H "Content-Type: application/json" -d "{\"question\": \"Your Question Here\"}" http://localhost:5000/search
```

To use `search_script.py`:

```
python app/search_script.py "Your Query Here"
```

### 2. Web Interface

Run the Flask app:

```
python app.py
```

Access it at: `http://localhost:5000`.

## Docker Setup

### Manual Docker Setup and Commands

1. **Build the Docker Image**:

```
docker build -t question_answering -f docker/Dockerfile .
```

2. **Run the Docker Container**:

```
docker run -d -p 5000:5000 question_answering
```

Your system should now be accessible at `http://localhost:5000`.

### Pulling and Running from Docker Hub 

1. **Pull the Docker Image**:

Pull the Docker image to obtain a pre-configured environment with all the necessary dependencies:

```
docker pull frankkyei/question_answering:latest
```

2. **Run a Docker Container**:

```
docker run -d -p 5000:5000 frankkyei/question_answering:latest
```
3. **Check Docker Status**: Ensure Docker is up and running with `docker ps`. If the desired container isn't listed, it's not running.
    Check troubleshooting section below to know what to do.
   
  

4. **Test the Endpoints**:

Test via `curl` or an API client:

For `/upload`:

```
curl -X POST -F "file=@path/to/your/file.csv" http://localhost:5000/upload

```
>**Note**: Make sure the '@' symbol comes before inserting your file path

For `/search`:

```
curl -X POST -H "Content-Type: application/json" -d "{\"question\": \"Your Question Here\"}" http://localhost:5000/search
```

5. **Run the `search_script.py`**:

Identify your container's ID or name:

```
docker ps
```

Execute the script within the container:

```
docker exec -it [CONTAINER_ID_OR_NAME] python app/search_script.py "Your Query Here"
```

Replace `[CONTAINER_ID_OR_NAME]` with the container ID/name.

## Troubleshooting

Should you encounter issues, consider these common fixes:

1. **Empty reply from server**:
   - **Description**: This happens when the server terminates the connection without sending a response.
   - **Fix**:
     - **Check Flask Logs**: Flask typically provides error messages and stack traces in its logs which can help identify the root cause.
     - **Docker Logs**: If running Flask within a Docker container, you can view the logs with:
       ```shell
       docker logs CONTAINER_ID_OR_NAME
       ```
     - **Retry**: Intermittent network issues or temporary server hiccups might cause this. Try sending the request again.

2. **Docker Container Not Running**:
   - **Description**: The Docker container hosting the Flask app isn't running.
   - **Fix**:
     - **Check Docker Status**: Use the following command to check running containers:
       ```shell
       docker ps
       ```
     - **Restart Container**: If your container isn't running, you can start it with:
       ```shell
       docker start CONTAINER_ID_OR_NAME
       ```

3. **Dependency Issues**:
   - **Description**: Missing or incompatible Python packages can cause runtime issues.
   - **Fix**:
     - **Install Dependencies**: Ensure all required packages are installed. If using Docker, the Dockerfile should handle the installations.
     - **Virtual Environment**: If not using Docker, consider setting up a Python virtual environment.

4. **API Errors**:
   - **Description**: Errors related to the request format, headers, or payload data.
   - **Fix**:
     - **Request Format**: Ensure the correct HTTP method and `Content-Type` header.
     - **Payload Data**: Ensure the data in the request is correctly formatted.



## Versioning

This documentation refers to version 1.0.0 of the Question Answering System. Future updates may alter functionalities or dependencies.

## Author:

[FK Baffour](https://www.linkedin.com/in/frank-kyei-baffour-403b60100/)

## Acknowledgments

- Kwame AI
- Sentence Transformers library
- Elasticsearch community