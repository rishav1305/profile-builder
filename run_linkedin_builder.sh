#!/bin/bash

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install requirements if needed
if [ ! -f ".requirements_installed" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
    touch .requirements_installed
fi

# Run the LinkedIn profile builder
echo "Starting LinkedIn Profile Builder..."
python linkedin_profile_builder.py $@

# Deactivate virtual environment
deactivate
