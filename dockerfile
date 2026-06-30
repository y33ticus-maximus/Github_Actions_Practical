# Use a lightweight Python base image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files 
# and to ensure output is sent straight to terminal (useful for Docker logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required by PyMuPDF (the engine behind pymupdf4llm)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker's cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user for security (best practice for your students to learn!)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Command to run the extractor
# Use the --file argument so it's easy to override when running the container
ENTRYPOINT ["python", "extractor.py"]
CMD ["--file", "sample.pdf"]