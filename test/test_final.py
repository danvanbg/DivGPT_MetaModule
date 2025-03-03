from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API Key not found! Make sure .env is set up correctly.")

# Create an OpenAI client instance with the API key
client = OpenAI(api_key=api_key)


print(api_key)

# Create a request to the correct endpoint for model completion
try:
    response = client.completions.create(  # Use `completions.create` instead of `models.create`
        model="gpt-4",  # Correct model name
        prompt="Hello, ChatGPT!",
        max_tokens=15
    )
    print(response['choices'][0]['text'])
except Exception as e:
    if "insufficient_quota" in str(e):
        print("You've exceeded your quota. Check your billing details: https://platform.openai.com/account/billing")
    else:
        print(f"An OpenAI error occurred: {e}")
