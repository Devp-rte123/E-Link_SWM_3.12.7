FROM python:3.14-slim

# Work directory inside the container
WORKDIR /code

# System dependencies for psycopg and PostgreSQL client
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code into container
COPY . .
