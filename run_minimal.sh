#!/bin/zsh

echo "Starting Profile Builder locally (minimal version)..."

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup_minimal.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service in the background..."
    ollama serve &
    # Wait for Ollama to start
    sleep 5
else
    echo "Ollama service is already running."
fi

# Start the Flask application (minimal version)
echo "Starting minimal Flask application on http://localhost:8080"
python3 app_minimal.py
