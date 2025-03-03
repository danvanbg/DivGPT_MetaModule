import requests
import json
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

try:
    from openai.error import RateLimitError
except ModuleNotFoundError:
    RateLimitError = Exception

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found! Make sure it's set in the .env file or as an environment variable.")

client = OpenAI(api_key=api_key)

def read_file(filename):
    """Read the first line from a file and return it as a string."""
    try:
        with open(filename, 'r') as f:
            return f.readline().strip()
    except FileNotFoundError:
        raise ValueError(f"File {filename} not found. Ensure it exists and is readable.")

# Load API URL and Key from files
local_api_url = read_file(".api.url")
local_api_key = read_file(".api.key")

class AutonomousChatGPTModule:
    def __init__(self):
        self.api_url = local_api_url
        self.api_key = local_api_key
        self.logs = self.get_all_data()
        self.local_log_file = 'logs.json'
        self.ensure_local_log_exists()

    def get_all_data(self):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(f"{self.api_url}/get_new_data", headers=headers)
        return response.json() if response.status_code == 200 else []

    def add_log(self, log_data):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.post(f"{self.api_url}/add_log", json={"log": log_data}, headers=headers)
        if response.status_code != 200:
            print("Error adding log:", response.status_code)
        self.append_to_local_log(log_data)

    def append_to_local_log(self, log_data):
        if not os.path.exists(self.local_log_file):
            with open(self.local_log_file, 'w') as f:
                json.dump([], f)
        with open(self.local_log_file, 'r+') as f:
            logs = json.load(f)
            logs.append(log_data)
            f.seek(0)
            json.dump(logs, f, indent=4)

    def ensure_local_log_exists(self):
        if not os.path.exists(self.local_log_file):
            with open(self.local_log_file, 'w') as f:
                json.dump([], f)

    def make_informed_decision(self, user_input):
        print(f"Processing user input: {user_input}")
        response_text = get_chatgpt_response(user_input) or f"Error processing input: {user_input}"
        self.add_log({"log": user_input, "response": response_text})
        print(response_text)
        return response_text

    def interact(self):
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting...")
                break
            response = self.make_informed_decision(user_input)
            self.logs = self.get_all_data()

def get_chatgpt_response(prompt, retries=5):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except RateLimitError:
            wait_time = 2 ** attempt
            print(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
        except Exception as e:
            print("Error contacting ChatGPT:", e)
            return None
    print("Failed to get a response after several retries.")
    return None

if __name__ == '__main__':
    module = AutonomousChatGPTModule()
    module.interact()
