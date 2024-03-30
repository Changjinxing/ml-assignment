# Use the official Python 3.9 slim image as base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt


# Run the Python application when the container starts
CMD ["python", "./api.py"]
