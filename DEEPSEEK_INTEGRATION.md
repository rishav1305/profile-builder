# Integrating deepseek-r1 Model with Profile Builder

This guide documents how to integrate the deepseek-r1 model via Ollama into the Profile Builder project for generating professional profiles on remote work platforms.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setting Up Ollama with deepseek-r1](#setting-up-ollama-with-deepseek-r1)
3. [Using OllamaClient in Profile Builder](#using-ollamaclient-in-profile-builder)
4. [Sample Use Cases](#sample-use-cases)
5. [Performance Considerations](#performance-considerations)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

- Ollama installed on your system
- At least 8GB of RAM and 5GB of free disk space
- Python 3.7 or higher
- Required Python packages: `requests`

## Setting Up Ollama with deepseek-r1

### Install Ollama (if not already installed)

Follow the instructions at [ollama.ai](https://ollama.ai) to install Ollama for your operating system.

### Pull the deepseek-r1 Model

Pull the deepseek-r1 model using the following command:

```bash
ollama pull deepseek-r1
```

This will download the 4.7GB model which may take some time depending on your internet connection. Once downloaded, you can verify the installation with:

```bash
ollama list
```

You should see `deepseek-r1` in the list of available models.

## Using OllamaClient in Profile Builder

The `OllamaClient` class in `ollama_integration.py` provides integration with Ollama's API for generating text with the deepseek-r1 model.

### Basic Usage

```python
from ollama_integration import OllamaClient

# Initialize the client (automatically verifies Ollama is running and loads model)
client = OllamaClient(model="deepseek-r1")

# Generate text
response = client.generate(
    "Create a professional title for a Python developer with ML experience",
    max_tokens=50,
    temperature=0.7
)
print(response)

# Use the chat interface
chat_response = client.chat([
    {"role": "user", "content": "How can I improve my LinkedIn profile?"}
])
print(chat_response)
```

### Integration with ProfileBuilder Class

The `ProfileBuilder` class initializes an `OllamaClient` that can be used throughout the profile building process:

```python
class ProfileBuilder:
    def __init__(self, platform, portfolio_data, credentials=None):
        self.platform = platform.lower()
        self.portfolio_data = portfolio_data
        self.credentials = credentials or {}
        self.ollama_client = OllamaClient(model="deepseek-r1")
        
    # Methods that use self.ollama_client for content generation
    # ...
```

## Sample Use Cases

The deepseek-r1 model can be used for various profile building tasks:

1. **Generating Professional Titles**
   - Creating concise, impactful titles based on skills and experience

2. **Writing Profile Overviews**
   - Crafting compelling summaries highlighting key expertise and achievements

3. **Creating Project Descriptions**
   - Developing detailed descriptions of past projects with focus on achievements

4. **Optimizing Skill Lists**
   - Prioritizing skills based on the target platform

5. **Generating Responses to Client Messages**
   - Creating professional responses to potential client inquiries

See the `deepseek_r1_integration_example.py` file for implementation examples of these use cases.

## Performance Considerations

- **Response Time**: The deepseek-r1 model typically takes 2-10 seconds for generation depending on the length and complexity of the prompt
- **Memory Usage**: Ensure your system has sufficient memory when running multiple generations
- **Concurrent Requests**: The client is not designed for high-volume concurrent requests

## Troubleshooting

### Common Issues

1. **Ollama Not Running**
   - The `OllamaClient` should automatically start Ollama if not running
   - If issues persist, try starting Ollama manually: `ollama serve`

2. **Model Not Found**
   - If you see "Model not found" errors, ensure you've pulled the model: `ollama pull deepseek-r1`

3. **Out of Memory Errors**
   - Try reducing `max_tokens` parameter when generating text
   - Close other memory-intensive applications

4. **Slow Generation**
   - First generation after initialization may be slower as the model loads into memory
   - Consider pre-warming the model with a simple generation before user interaction

### Getting Help

For more information:
- See the [Ollama documentation](https://github.com/ollama/ollama/blob/main/README.md)
- Check the deepseek-r1 model details in the [Ollama model library](https://ollama.ai/library/deepseek-r1)
