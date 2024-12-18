# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
COPY . /usr/src/app
# update all python packages
RUN pip install --upgrade pip

# copy requirements.txt file
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container (optional, based on the project)
EXPOSE 5000

# Define environment variable
ENV NAME DockerApp

# Install gunicorn explicitly
RUN pip install gunicorn

# Run the command to start the app
# Start the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]








