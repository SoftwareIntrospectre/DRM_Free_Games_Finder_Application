# Use official Ubuntu as a parent image
FROM ubuntu:22.04

# Set environment variables to ensure consistent behavior across Docker containers
ENV PYTHONUNBUFFERED=1 
ENV LOGGING_LEVEL=INFO
ENV FASTAPI_HOST=0.0.0.0
ENV FASTAPI_PORT=5000

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies, including Python 3, pip, Java (for PySpark), and required libraries for Airflow and FastAPI
RUN apt-get update && apt-get install -y \
    openjdk-11-jre-headless \  # Install OpenJDK 11 for Spark compatibility
    python3 \
    python3-pip \
    python3-dev \
    gcc \
    libsasl2-dev \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    curl \
    gnupg2 \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Java (required for PySpark)
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Python dependencies from requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Set up environment variables for email configuration (for notifications in the project)
ENV FROM_EMAIL=""
ENV TO_EMAIL=""
ENV EMAIL_PASSWORD=""
ENV SMTP_SERVER="smtp.gmail.com"
ENV SMTP_PORT="587"
ENV FERNET_KEY=""

# Expose the FastAPI port (default is 5000)
EXPOSE 5000

# Run the FastAPI application (entrypoint for the container)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]