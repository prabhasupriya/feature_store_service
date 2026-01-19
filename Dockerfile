# Use a modern slim Python base image (Bullseye is more stable than Buster)
FROM python:3.9-slim-bullseye

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and scripts
COPY ./app /app/app
COPY ./scripts /app/scripts

COPY ./tests /app/tests
# Expose the port the API runs on
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]