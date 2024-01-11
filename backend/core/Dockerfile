# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /core

# Copy the requirements file to the working directory
COPY ./requirements.txt /core/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r /core/requirements.txt

# Copy the application code to the working directory
COPY . .

# Copy the .env file to the working directory
# COPY .env .

# Run the start.py script
CMD ["python", "start.py"]
