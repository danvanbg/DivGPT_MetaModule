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
    response = openai.completions.create(model="gpt-4o",
    prompt="Hello, ChatGPT!",
    max_tokens=15)
    print(response.choices[0].text)
except openai.OpenAIError as e:
    if "insufficient_quota" in str(e):
        print("You've exceeded your quota. Check your billing details: https://platform.openai.com/account/billing")
    else:
        print(f"An OpenAI error occurred: {e}")
except openai.OpenAIError as e:
    print(f"An error occurred: {e}")
