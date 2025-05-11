#!/bin/zsh

echo "Setting up Profile Builder for local development (minimal version)..."

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

# Install core dependencies only
echo "Installing required Python packages (minimal set)..."
pip install flask==2.0.3 werkzeug==2.0.3 requests==2.28.2 beautifulsoup4==4.12.2 python-dotenv==1.0.0 selenium==4.9.0 webdriver-manager==3.8.6

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama is required but not found. Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama is already installed."
fi

# Create a simplified version of the app
echo "Creating a simplified version of the app..."
cat > app_minimal.py << 'EOF'
import os
from flask import Flask, render_template, request, jsonify
import subprocess
import requests
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_portfolio():
    """Extract information from the portfolio website."""
    portfolio_url = request.form.get('portfolio_url')
    if not portfolio_url:
        return jsonify({'error': 'Portfolio URL is required'}), 400
    
    try:
        # Simplified portfolio data for demo
        portfolio_data = {
            'basic_info': {
                'name': 'Rishav Chatterjee',
                'email': 'rishavchatterjee2024@gmail.com',
                'title': 'Technology Leader',
                'location': 'India'
            },
            'about': {
                'summary': 'Technology Leader with expertise in engineering scalable cloud-based solutions. Experience with AI to boost productivity and drive innovation. Specializes in designing scalable data solutions that align tech with business goals.'
            },
            'experience': [
                {
                    'title': 'Technology Lead',
                    'company': 'Bitwise Solutions Pvt Ltd',
                    'duration': 'Dec 2022 - Present',
                    'location': 'Pune, Maharashtra',
                    'achievements': [
                        'Initiated B2B analytics reporting with key insights through Funnel Analysis and Forecasting',
                        'Optimized Programmatic Advertisers pipeline, reducing processing time by 60%',
                        'Executed NetSuite invoice data integration with Salesforce'
                    ]
                },
                {
                    'title': 'Senior Data Engineer',
                    'company': 'Novartis Healthcare Pvt Ltd',
                    'duration': 'May 2020 - Dec 2022',
                    'location': 'Hyderabad, Telangana',
                    'achievements': [
                        'Migrated from HIVE to Snowflake, increasing pipeline performance by 60%',
                        'Orchestrated jobs using Apache Airflow and Alteryx, improving system speed by 40%'
                    ]
                }
            ],
            'education': [
                {
                    'degree': "Bachelor's Degree",
                    'institution': 'Delhi Technological University (DTU)',
                    'period': '2014 - 2018'
                }
            ],
            'skills': {
                'technical': [
                    'SQL', 'Python', 'Data Warehouse', 'ETL Tools', 'Cloud Services',
                    'Analytical Tools', 'Project Management', 'Big Data Tools',
                    'Snowflake', 'AWS', 'Azure', 'GCP', 'Apache Airflow',
                    'Kubernetes', 'Docker', 'CI/CD', 'Terraform', 'Git'
                ]
            }
        }
        return jsonify({'success': True, 'data': portfolio_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/build_profile', methods=['POST'])
def build_profile():
    """Build a profile on the selected platform."""
    data = request.json
    platform = data.get('platform')
    portfolio_data = data.get('portfolio_data')
    
    if not platform or not portfolio_data:
        return jsonify({'error': 'Platform and portfolio data are required'}), 400
    
    try:
        # Simplified profile content generation for demo
        if platform == 'linkedin':
            result = {
                'headline': 'Technology Leader | Data Engineering | Cloud Solutions | AI Innovation',
                'about': portfolio_data.get('about', {}).get('summary', ''),
                'skills': portfolio_data.get('skills', {}).get('technical', [])[:10],
                'status': 'content_generated'
            }
        elif platform == 'upwork':
            result = {
                'title': 'Senior Data Engineer & Cloud Solutions Architect',
                'overview': portfolio_data.get('about', {}).get('summary', ''),
                'skills': portfolio_data.get('skills', {}).get('technical', [])[:10],
                'hourly_rate': 65.0,
                'status': 'content_generated'
            }
        else:
            return jsonify({'error': f'Platform {platform} is not supported'}), 400
            
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/platforms')
def get_platforms():
    """Return the list of supported platforms."""
    return jsonify({
        'platforms': [
            {
                'id': 'upwork',
                'name': 'Upwork',
                'description': 'One of the largest freelancing platforms with opportunities across numerous fields',
                'supported': True
            },
            {
                'id': 'linkedin',
                'name': 'LinkedIn',
                'description': 'Professional networking platform ideal for job searching and professional branding',
                'supported': True
            }
        ]
    })

@app.route('/status')
def get_status():
    """Check the status of the Ollama model."""
    try:
        # Check if Ollama is running
        result = subprocess.run(['pgrep', '-f', 'ollama'], capture_output=True, text=True)
        if result.stdout:
            return jsonify({'status': 'ready', 'model': 'deepseek-r1 (demo mode)'})
        return jsonify({'status': 'model_not_found', 'message': 'Ollama process not found'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)
EOF

echo "Setup complete! You can now run the simplified application with: 'source venv/bin/activate && python3 app_minimal.py'"
