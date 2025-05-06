import requests
import json
import logging
import time
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OllamaClient:
    """
    Client for interacting with Ollama API to generate text using the deepseek model.
    """
    
    def __init__(self, model="deepseek-coder", base_url="http://localhost:11434"):
        """Initialize the Ollama client."""
        self.model = model
        self.base_url = base_url
        self._ensure_model_loaded()
    
    def _ensure_model_loaded(self):
        """Ensure that the model is loaded and Ollama is running."""
        try:
            # Check if Ollama process is running
            result = subprocess.run(['pgrep', '-f', 'ollama'], capture_output=True, text=True)
            if not result.stdout:
                logging.warning("Ollama process not found. Starting Ollama...")
                # Start Ollama in the background
                subprocess.Popen(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(5)  # Wait for Ollama to start
            
            # Check if our model is loaded
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name") for m in models]
                
                if self.model not in model_names:
                    logging.warning(f"Model {self.model} not found. Pulling the model...")
                    self._pull_model()
            else:
                logging.error(f"Failed to check available models: {response.status_code}")
                raise ConnectionError("Could not connect to Ollama API")
                
        except Exception as e:
            logging.error(f"Error ensuring model is loaded: {str(e)}")
            raise
    
    def _pull_model(self):
        """Pull the specified model from Ollama's registry."""
        try:
            logging.info(f"Pulling model {self.model}...")
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": self.model}
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to pull model: {response.status_code}")
                
            logging.info(f"Successfully pulled model {self.model}")
        except Exception as e:
            logging.error(f"Error pulling model: {str(e)}")
            raise
    
    def generate(self, prompt, max_tokens=2000, temperature=0.7):
        """Generate text using the deepseek model."""
        try:
            logging.info("Generating text with Ollama")
            
            # Prepare the request
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            # Make the request to Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            
            if response.status_code != 200:
                error_msg = f"Failed to generate text: {response.status_code}"
                logging.error(error_msg)
                raise Exception(error_msg)
                
            # Extract generated text
            result = response.json()
            generated_text = result.get("response", "")
            
            logging.info("Successfully generated text")
            return generated_text
            
        except Exception as e:
            logging.error(f"Error generating text with Ollama: {str(e)}")
            # Fallback to a simple response if generation fails
            return "I couldn't generate specific content at this time. Please check Ollama is properly installed and running."
    
    def chat(self, messages, max_tokens=2000, temperature=0.7):
        """
        Chat with the model using a list of messages.
        Each message should be a dict with 'role' and 'content' keys.
        """
        try:
            logging.info("Starting chat with Ollama")
            
            # Prepare the request
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            # Make the request to Ollama
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            
            if response.status_code != 200:
                error_msg = f"Failed to chat: {response.status_code}"
                logging.error(error_msg)
                raise Exception(error_msg)
                
            # Extract generated text
            result = response.json()
            message = result.get("message", {})
            generated_text = message.get("content", "")
            
            logging.info("Successfully completed chat")
            return generated_text
            
        except Exception as e:
            logging.error(f"Error chatting with Ollama: {str(e)}")
            return "I couldn't process this chat at this time. Please check if Ollama is properly installed and running."


if __name__ == "__main__":
    # Test the Ollama client
    client = OllamaClient()
    response = client.generate("Tell me a short joke about programming")
    print(f"Generated response: {response}")
    
    chat_response = client.chat([
        {"role": "user", "content": "What are the main benefits of using Docker?"}
    ])
    print(f"Chat response: {chat_response}")