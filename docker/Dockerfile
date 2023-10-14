# Using an official Python runtime as a parent image
FROM python:3.10-slim

# Setting the working directory to /question_answering
WORKDIR /question_answering

# Copy the current directory contents into the container at /question_answering
COPY . /question_answering

# Install any needed packages specified in requirements.txt
RUN pip install --default-timeout=1000 -r ./docker/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run your application when the container launches
CMD ["python", "app/app.py"]
