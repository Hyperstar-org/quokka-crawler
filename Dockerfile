# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies needed for lxml and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev libxslt1-dev zlib1g-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy poetry config files
COPY pyproject.toml poetry.lock* /app/

# Copy the rest of the project files
COPY . /app

# Install dependencies via Poetry (no virtualenv)
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root




# Default command to run main.py
CMD ["python", "main.py"]
