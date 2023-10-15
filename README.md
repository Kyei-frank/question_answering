## Table of Contents

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
- Elasticsearch (for manual setup, and ensure it is running and accessible)
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
python -m pip install -qr requirements.txt
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

For users utilizing Elasticsearch Cloud, set the environment variables:

```
export ES_USERNAME=elastic
export ES_PASSWORD=YourElasticsearchPassword
export ES_CLOUD_ENDPOINT=your-elasticsearch-url.com
```

If you're using a local Elasticsearch setup or a different configuration, adjust the environment variables accordingly.

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
>**Note**: Ensure the '@' symbol precedes your file path.

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

1. **Build the Application Docker Image**:

    Navigate to the project root and run:
    
    ```bash
    docker-compose -f docker/docker-compose.yml build
    ```

    This will build the Docker image for your application.

2. **Run the Application and Elasticsearch using Docker Compose**:

    From the project root, execute:

    ```bash
    docker-compose -f docker/docker-compose.yml up
    ```

    This command will start both your application and an Elasticsearch instance.

    Your app will be able to connect to Elasticsearch using the hostname `elasticsearch`, thanks to Docker Compose which sets up a network for your services.

3. **Accessing the Application**:

    Once everything is up and running, access your application at:
    
    ```
    http://localhost:5000
    ```

    Elasticsearch can be accessed (if needed) at:

    ```
    http://localhost:9200
    ```

4. **Stopping the Services**:

    To gracefully stop the services, navigate to the project root and run:

    ```
    docker-compose -f docker/docker-compose.yml down
    ```

### Pulling and Running from Docker Hub 

1. **Pull the Docker Image**:

    Pull the Docker image to obtain a pre-configured environment with all the necessary dependencies:

    ```
    docker pull frankkyei/question_answering_app:latest
    ```

2. **Run a Docker Container**:
  
    To run both the app and Elasticsearch containers in tandem, you'd need access to the `docker-compose.yml` file, which means you'd have to clone this repository or somehow download the  `docker-compose.yml` file in the `docker` folder to your computer and specify the path to the file in the codes below:

    ```
    docker-compose -f path/to/docker-compose.yml up
    ```

3. **Check Docker Status**: Use `docker ps` to ensure Docker is running properly. If your intended container isn't listed, it might not be running. Refer to the troubleshooting section below for potential issues and solutions.

4. **Test the Endpoints**:

    Test via `curl` or an API client:
    
    First run the indexing.py file to index the data into Elatic search so you can run some queries

    ```
    docker exec -it [CONTAINER_ID_OR_NAME] python app/indexing.py

    ```

    For `/upload`:

    ```
    curl -X POST -F "file=@path/to/your/file.csv" http://localhost:5000/upload

    ```
    >**Note**: Note: You can download the `passage_metadata_emb.csv` file from the docs folder and use it as sample documents for indexing. Ensure the '@' symbol precedes your file path. 

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
   - **Description**: This can occur if the server terminates the connection without sending a response, or the server might not be running or crashed.
   - **Fix**:
     - **Check Flask Logs**: Flask typically provides error messages and stack traces in its logs which can help identify the root cause.
     - **Docker Logs**: If running Flask within a Docker container, view the logs with:
       ```shell
       docker logs CONTAINER_ID_OR_NAME
       ```
     - **Retry**: Intermittent network issues or temporary server hiccups might

 resolve on their own. If the issue persists, consider the above.

## Versioning

This project uses [SemVer](http://semver.org/) for versioning.

## Author:

[FK Baffour](https://www.linkedin.com/in/frank-kyei-baffour-403b60100/)

## Acknowledgments

- Kwame AI
- Sentence Transformers library
- Elasticsearch
- Docker
- Flask