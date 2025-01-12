FROM bitnami/python:3.11.10-debian-12-r1

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update -y \
    && apt-get install -y \
    python3-dev \
    libpq-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app


# Copy only requirements.txt first to leverage Docker cache
COPY ../requirements.txt /app/requirements.txt
RUN pip3 install -r ./requirements.txt

# Copy the rest of the code
COPY .. /app/project/
WORKDIR /app/project
CMD ["sh", "-c", "if [ \"$SERVER_NAME\" = 'local_development' ]; then exec /bin/sh -c 'trap : TERM INT; (while true; do sleep 1000; done) & wait'; else exec python manage.py runserver 0.0.0.0:8000; fi"]
