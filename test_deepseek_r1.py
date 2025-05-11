import logging
from ollama_integration import OllamaClient
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_generate():
    """Test the generate method of OllamaClient with deepseek-r1 model."""
    client = OllamaClient(model="deepseek-r1")
    
    # Test 1: Simple prompt
    prompt = "What are the three most important skills for a software developer?"
    logging.info(f"Testing generate with prompt: {prompt}")
    response = client.generate(prompt, max_tokens=500, temperature=0.7)
    logging.info(f"Response: {response}")
    print(f"\nGENERATE TEST 1 RESPONSE:\n{response}\n")
    
    # Give a moment before the next request
    time.sleep(2)
    
    # Test 2: More complex prompt related to profile building
    profile_prompt = "Create a professional summary for a senior software engineer with 8 years of experience in Python, JavaScript, and cloud technologies."
    logging.info(f"Testing generate with profile prompt: {profile_prompt}")
    profile_response = client.generate(profile_prompt, max_tokens=1000, temperature=0.7)
    logging.info(f"Profile Response: {profile_response}")
    print(f"\nGENERATE TEST 2 RESPONSE:\n{profile_response}\n")

def test_chat():
    """Test the chat method of OllamaClient with deepseek-r1 model."""
    client = OllamaClient(model="deepseek-r1")
    
    # Test 1: Simple chat
    messages = [
        {"role": "user", "content": "What are the best practices for writing API documentation?"}
    ]
    logging.info(f"Testing chat with messages: {messages}")
    chat_response = client.chat(messages, max_tokens=800, temperature=0.7)
    logging.info(f"Chat Response: {chat_response}")
    print(f"\nCHAT TEST 1 RESPONSE:\n{chat_response}\n")
    
    # Give a moment before the next request
    time.sleep(2)
    
    # Test 2: Multi-turn conversation
    multi_turn_messages = [
        {"role": "user", "content": "I want to build a professional Upwork profile for a data scientist."},
        {"role": "assistant", "content": "That's a great goal. I can help you create a professional profile for a data scientist on Upwork. What kind of experience and skills should this profile highlight?"},
        {"role": "user", "content": "The profile should highlight experience with Python, pandas, scikit-learn, and experience with NLP projects."}
    ]
    logging.info(f"Testing chat with multi-turn conversation")
    multi_turn_response = client.chat(multi_turn_messages, max_tokens=1200, temperature=0.7)
    logging.info(f"Multi-turn Chat Response: {multi_turn_response}")
    print(f"\nCHAT TEST 2 RESPONSE:\n{multi_turn_response}\n")

if __name__ == "__main__":
    print("\n=== STARTING DEEPSEEK-R1 MODEL TESTS ===\n")
    logging.info("Starting deepseek-r1 tests")
    test_generate()
    logging.info("Generate tests completed")
    print("\n=== GENERATE TESTS COMPLETED ===\n")
    
    time.sleep(3)  # Pause between test sets
    
    print("\n=== STARTING CHAT TESTS ===\n")
    logging.info("Starting chat tests")
    test_chat()
    logging.info("Chat tests completed")
    print("\n=== CHAT TESTS COMPLETED ===\n")
    
    logging.info("All tests completed")
    print("\n=== ALL DEEPSEEK-R1 MODEL TESTS COMPLETED ===\n")
