FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    gnupg \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for web interface
EXPOSE 8080

# Create a startup script that will start Ollama and pull the model
RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 5\n\
ollama pull deepseek-r1:latest\n\
python app.py' > /app/start.sh && chmod +x /app/start.sh

# Command to start the application
CMD ["/app/start.sh"]