FROM --platform=linux/amd64 python:3.10-slim-buster

RUN pip3 install --upgrade pip

RUN apt-get update && apt-get install -y \
    gnupg2 \
    curl \
    apt-transport-https \
    jq && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev


FROM --platform=linux/amd64 python:3.10-slim-buster

COPY requirements.txt .
COPY testing_requirements.txt .

# Upgrade pip
RUN pip3 install --upgrade pip

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gnupg2 \
    curl \
    apt-transport-https \
    jq && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r testing_requirements.txt

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*