# Use a minimal Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy files to the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port for the API
EXPOSE 5000

# Start the Flask API
CMD ["python", "serve_model.py"]
