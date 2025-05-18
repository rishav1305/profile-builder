import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from portfolio_extractor import PortfolioExtractor
from profile_builder import ProfileBuilder
from profile_logger import ProfileLogger

app = Flask(__name__)
profile_logger = ProfileLogger()

# Add custom template filter for datetime formatting
@app.template_filter('datetime')
def format_datetime(value):
    """Format a datetime string to a more readable format."""
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except:
        return value

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_portfolio():
    """Extract information from the portfolio website."""
    # Handle both JSON and form data for backward compatibility
    if request.is_json:
        data = request.json
        portfolio_url = data.get('portfolio_url')
        use_cache = data.get('use_cache', False)
        force_refresh = data.get('force_refresh', False)
    else:
        portfolio_url = request.form.get('portfolio_url')
        use_cache = False
        force_refresh = False
    
    if not portfolio_url:
        return jsonify({'error': 'Portfolio URL is required'}), 400
    
    try:
        # If force refresh is requested, explicitly set use_cache to False
        if force_refresh:
            use_cache = False
        
        # Create extractor with URL, cache settings, and reasonable cache duration
        extractor = PortfolioExtractor(
            url=portfolio_url,
            use_cache=use_cache,
            cache_duration_minutes=60  # Cache valid for 1 hour
        )
        
        portfolio_data = extractor.extract()
        
        # Add a message about data freshness
        response_message = "Fresh data extracted" if not use_cache else "Cached data retrieved"
        
        return jsonify({
            'success': True, 
            'data': portfolio_data,
            'message': response_message,
            'timestamp': portfolio_data.get('last_updated', datetime.now().isoformat())
        })
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

@app.route('/build_linkedin_profile', methods=['POST'])
def build_linkedin_profile():
    """Build a LinkedIn profile directly using the specialized LinkedIn builder."""
    from linkedin_profile_builder import LinkedInProfileBuilder
    
    data = request.json
    portfolio_data = data.get('portfolio_data')
    credentials = data.get('credentials', {})
    headless = data.get('headless', True)
    
    if not portfolio_data:
        return jsonify({'error': 'Portfolio data is required'}), 400
    
    try:
        # Use the specialized LinkedIn builder
        builder = LinkedInProfileBuilder(headless=headless, portfolio_url=None)
        builder.profile_data = portfolio_data  # Set the extracted data directly
        
        # Build the profile
        result = builder.build_linkedin_profile(credentials)
        
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

@app.route('/logs')
def view_logs():
    """View the profile update logs dashboard."""
    platform = request.args.get('platform')
    limit = int(request.args.get('limit', 10))
    
    logs = profile_logger.get_recent_logs(platform, limit)
    return render_template('logs.html', logs=logs)

@app.route('/api/logs')
def get_logs():
    """API endpoint to get profile update logs."""
    platform = request.args.get('platform')
    limit = int(request.args.get('limit', 10))
    
    logs = profile_logger.get_recent_logs(platform, limit)
    return jsonify({'logs': logs})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)