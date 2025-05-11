#!/bin/zsh

echo "Starting Profile Builder locally..."

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup_local.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    # Wait for Ollama to start
    sleep 5
else
    echo "Ollama service is already running."
fi

# Start the Flask application
echo "Starting Flask application on http://localhost:8080"
python3 app.py
