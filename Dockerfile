# Pull python
FROM python:3.8-slim

# Create working dir
RUN mkdir /app

# Copy files over
COPY app.py /app
COPY src/ /app

# Make working dir test-app
WORKDIR /app

# Upgrade pip
RUN pip3 install --upgrade pip

# Install requirements
RUN pip3 install -r requirements.txt

# Environment vars
ENV FLASK_APP=app.py

# Expose working port
EXPOSE 5000