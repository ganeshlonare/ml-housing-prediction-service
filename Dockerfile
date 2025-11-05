# Start with an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
# This is done first to leverage Docker's layer caching
COPY requirements.txt requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install kaggle 
# Copy your application code into the container
COPY ./app /app/app
# Copy your trained model file into the container
COPY ./model /app/model

# Command to run the Uvicorn server
# The host 0.0.0.0 makes the app accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]