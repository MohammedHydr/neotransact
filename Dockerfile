# Step 1: Use the official Python image
FROM python:3.10-slim

# Step 2: Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && apt-get clean

# Step 3: Install Poetry
RUN pip install poetry

# Copy project files to the container
COPY . .

# Step 4: Copy necessary files for dependency installation
COPY pyproject.toml poetry.lock ./

# Step 5: Install dependencies (no dev dependencies in production)
RUN poetry config virtualenvs.create false && poetry install --only main

# Step 6: Copy the entire application code
COPY . .

# Step 7: Expose the application port
EXPOSE 8000

# Step 8: Set environment variables
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONUNBUFFERED=1

# Step 9: Run the entrypoint script
ENTRYPOINT ["sh", "./entrypoint.sh"]
