import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API Key not found! Make sure .env is set up correctly.")

# Set the API Key for OpenAI
print(api_key)
# Create a chat completion request (Corrected for new API version)
try:
    #response = openai.completions.create(model="gpt-3.5-turbo",
    response = openai.completions.create(model="text-davinci-003",
    prompt="Hello, ChatGPT!",
    max_tokens=5)
    print(response.choices[0].text)
except openai.RateLimitError as e:
    print(f"Rate limit exceeded. Please check your quota. {e}")
except openai.OpenAIError as e:
    print(f"An error occurred: {e}")
