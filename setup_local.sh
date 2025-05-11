#!/bin/zsh

echo "Setting up Profile Builder for local development..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing required Python packages..."
pip install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama is required but not found. Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama is already installed."
fi

# Pull the deepseek-r1 model
echo "Pulling the deepseek-r1 model (this may take some time)..."
ollama pull deepseek-r1:latest

echo "Setup complete! You can now run the application with: 'source venv/bin/activate && python3 app.py'"
