FROM python:3.11-slim-buster

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy your API code
COPY . /app

# Set the working directory
WORKDIR /app

# Define the command to run your API
CMD ["python", "app.py"]