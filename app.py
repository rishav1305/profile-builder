import os
from flask import Flask, render_template, request, jsonify
from portfolio_extractor import PortfolioExtractor
from profile_builder import ProfileBuilder

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
        extractor = PortfolioExtractor(portfolio_url)
        portfolio_data = extractor.extract()
        return jsonify({'success': True, 'data': portfolio_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/build_profile', methods=['POST'])
def build_profile():
    """Build a profile on the selected platform."""
    data = request.json
    platform = data.get('platform')
    portfolio_data = data.get('portfolio_data')
    credentials = data.get('credentials', {})
    
    if not platform or not portfolio_data:
        return jsonify({'error': 'Platform and portfolio data are required'}), 400
    
    try:
        builder = ProfileBuilder(platform, portfolio_data, credentials)
        result = builder.build()
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/platforms')
def get_platforms():
    """Return the list of supported platforms."""
    # Updated to include both Upwork and LinkedIn
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
    import subprocess
    try:
        # Check if Ollama is running with the deepseek model
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if 'deepseek-r1' in result.stdout:
            return jsonify({'status': 'ready', 'model': 'deepseek-r1'})
        return jsonify({'status': 'model_not_found', 'message': 'deepseek-r1 model not found'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)