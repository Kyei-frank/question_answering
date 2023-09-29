# Using an official Python runtime as a parent image
FROM python:3.10-slim

# Setting the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --default-timeout=1000 -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables
ENV ES_USERNAME elastic
ENV ES_PASSWORD JjfCLFlTkozxrjoJI6rgsj2F
ENV ES_CLOUD_ENDPOINT https://my-deployment-eac7ec.es.us-central1.gcp.cloud.es.io


# Run your application when the container launches
CMD ["python", "/app.py"]
