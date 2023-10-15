# Using an official Python runtime as a parent image
FROM python:3.10-slim

# Setting the working directory to /question_answering
WORKDIR /question_answering

# Copy all contents of the question_answering directory
COPY . /question_answering

# Install any needed packages specified in requirements.txt
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run your application when the container launches
CMD ["python", "app/app.py"]
