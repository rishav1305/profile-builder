# LinkedIn Profile Builder

Part of the Profile Builder AI Agent project, this module automatically optimizes your LinkedIn profile using the Ollama deepseek-r1 model.

## Features

- **Extract Portfolio Data**: Pulls your professional information from your portfolio website
- **Intelligent Content Generation**: Uses Ollama with the deepseek-r1 model for LinkedIn-optimized content
- **Profile Analysis**: Compares your current LinkedIn profile with portfolio data to suggest improvements
- **Automated Updates**: Can automatically update your LinkedIn profile with optimized content
- **Change Tracking**: Logs all changes for later review in the dashboard

## How It Works

The LinkedIn Profile Builder follows this process:

1. **Extract Data**: Pulls your professional information from your portfolio website
2. **Analyze Current Profile**: If credentials are provided, scrapes and analyzes your current LinkedIn profile
3. **Generate Optimized Content**: Uses the Ollama deepseek-r1 model to generate LinkedIn-optimized:
   - Headline
   - About section
   - Skill recommendations
4. **Apply Changes**: If credentials are provided, automatically updates your LinkedIn profile
5. **Log Changes**: Records all changes to a log file viewable in the dashboard

## Usage

You can run the LinkedIn Profile Builder in two ways:

### Via Command Line

```bash
# Run the LinkedIn profile builder with UI
./run_linkedin_builder.sh

# Run in headless mode
./run_linkedin_builder.sh --headless

# Specify a different portfolio URL
./run_linkedin_builder.sh --portfolio https://yourportfolio.com
```

### Via Web Interface

1. Start the web application: `./run_local.sh`
2. Open in your browser: `http://localhost:8080`
3. Extract your portfolio data
4. Select LinkedIn as the platform
5. Optionally provide your LinkedIn credentials
6. Click "Generate & Build Profile"

## Security Note

Your LinkedIn credentials are used only for the current session and are not stored.
All processing happens locally using Ollama - no data is sent to external APIs.

## Dashboard

A dashboard of all profile updates is available at `http://localhost:8080/logs`
This shows:
- What changes were made to your profile
- When changes were made
- Links to your updated profiles

## Requirements

- Python 3.8+
- Ollama with deepseek-r1 model installed
- Playwright for web automation
- Flask for web interface

See requirements.txt for a complete list of dependencies.
