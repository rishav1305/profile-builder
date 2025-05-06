# Profile Builder AI Agent

An AI-powered tool that automatically fills in your professional profiles across various remote work platforms and job boards using your portfolio data and the Ollama deepseek model.

## Project Overview

This project creates a Docker container with Python, Git, and Ollama to run a local AI agent. The agent extracts information from your portfolio and automatically fills out profiles on remote work platforms like Upwork, Fiverr, and other job boards.

## Features

- **Docker Environment**: Containerized setup with Python, Git, and Ollama
- **Local LLM**: Uses Ollama with the deepseek model for AI tasks without sending data to external APIs
- **Profile Automation**: Automatic form filling for remote work platforms
- **Data Extraction**: Uses your existing portfolio as the source of professional information
- **First Platform Support**: Initially targets Upwork (with more platforms to be added)

## Prerequisites

- Docker installed on your system
- Internet connection for initial setup (downloading Docker images and the Ollama model)

## Quick Start

1. Clone this repository:
   ```
   git clone [repository-url]
   cd profile-builder
   ```

2. Build the Docker image:
   ```
   docker build -t profile-builder .
   ```

3. Run the container:
   ```
   docker run -p 8080:8080 profile-builder
   ```

4. Access the web interface:
   ```
   http://localhost:8080
   ```

## Technical Details

### Docker Container

The Docker container includes:
- Python 3.10+
- Git
- Ollama with the deepseek model
- Required Python libraries for web scraping and form automation

### AI Agent Architecture

The agent follows this workflow:
1. Extracts your professional information from your portfolio website
2. Uses Ollama (deepseek model) to format the content appropriately for each platform
3. Automates browser interactions to fill out forms on target platforms

### Currently Supported Platforms

- **Upwork** (POC): Automatic profile creation using your professional data

## Implementation Details

The implementation leverages:
- **Python Selenium**: For web automation and form filling
- **BeautifulSoup**: For parsing website content
- **Ollama**: For running the deepseek LLM locally
- **Flask**: For the web interface

## Portfolio Data Extraction

The agent extracts the following information from your portfolio:

- **Professional Experience**:
  - Technology Lead at Bitwise Solutions (Dec 2022 - Present)
  - Senior Data Engineer at Novartis Healthcare (May 2020 - Dec 2022)
  - Data Engineer at Polestar Solutions (Jun 2018 - Apr 2020)

- **Education**:
  - Bachelor's Degree from Delhi Technological University (DTU)

- **Technical Skills**:
  - SQL, Python, Data Warehouse, ETL Tools, Cloud Services, Analytical Tools, Project Management, Big Data Tools

- **About**:
  - Technology Leader with expertise in engineering scalable cloud-based solutions
  - Experience with AI to boost productivity and drive innovation
  - Specializes in designing scalable data solutions that align tech with business goals

## Future Enhancements

- Support for additional remote work platforms (Fiverr, Freelancer.com, etc.)
- Enhanced customization of profiles per platform
- Automated profile updating from portfolio changes
- Support for multiple portfolio sources

## License

MIT License

## Contact

rishavchatterjee2024@gmail.com