import requests
import json
import os
import random
import time
from openai import OpenAI
from dotenv import load_dotenv

# Try importing RateLimitError; if it fails, use a generic Exception as fallback.
try:
    from openai.error import RateLimitError
except ModuleNotFoundError:
    RateLimitError = Exception

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

try:
    response = openai.Model.list()
    print("OpenAI API is accessable!")
except openai.error.AuthenticationError:
    print("Error: Unvalid Key.")
except openai.error.RateLimitError:
    print("Error: Rate limit exceeded. Wait.")

def get_chatgpt_response(prompt, retries=5):
    """
    Send the user prompt to ChatGPT using OpenAI's API and return the response.
    Implements exponential backoff to handle rate limit (429) errors.
    """
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # or your preferred model
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            wait_time = 2 ** attempt  # Exponential backoff: 1, 2, 4, 8, ... seconds
            print(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
        except Exception as e:
            print("Error contacting ChatGPT:", e)
            return None
    print("Failed to get a response after several retries.")
    return None

class AutonomousChatGPTModule:
    def __init__(self, api_url, api_key):
        self.api_url = "http://84.203.90.102:8000"  # Use the provided API URL
        self.api_key = "9647cf29c1e313d17b661d2508cbf2b2"  # Use the provided API key
        self.logs = self.get_all_data()  # Fetch initial logs/data
        self.local_log_file = 'logs.json'  # Local file to store logs

        # Ensure the local log file exists
        self.ensure_local_log_exists()

    def get_all_data(self):
        """
        Fetch all data from the API to enable reflection and informed decision-making.
        This could be all past conversations, actions, or logs.
        """
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(f"{self.api_url}/get_new_data", headers=headers)
        if response.status_code == 200:
            return response.json()  # All past logs
        else:
            print("Error fetching data:", response.status_code)
            return []

    def add_log(self, log_data):
        """
        Add a new log entry to the API and to the local file.
        """
        headers = {'Authorization': f'Bearer {self.api_key}'}
        payload = {"log": log_data}
        response = requests.post(f"{self.api_url}/add_log", json=payload, headers=headers)
        if response.status_code == 200:
            print("Log added successfully.")
        else:
            print("Error adding log:", response.status_code)

        # Also append the log to the local file
        self.append_to_local_log(log_data)

    def append_to_local_log(self, log_data):
        """
        Append the log data to the local log file, creating it if it doesn't exist.
        """
        if not os.path.exists(self.local_log_file):
            with open(self.local_log_file, 'w') as f:
                json.dump([], f)

        with open(self.local_log_file, 'r+') as f:
            logs = json.load(f)
            logs.append(log_data)
            f.seek(0)
            json.dump(logs, f, indent=4)

    def ensure_local_log_exists(self):
        """
        Ensure that the local log file exists before performing any operations.
        """
        if not os.path.exists(self.local_log_file):
            with open(self.local_log_file, 'w') as f:
                json.dump([], f)

    def make_informed_decision(self, user_input):
        """
        Get a real response from ChatGPT using the OpenAI API.
        """
        print(f"Processing user input: {user_input}")

        # Get a response from ChatGPT using the defined function
        response_text = get_chatgpt_response(user_input)
        if response_text is None:
            response_text = f"Error processing your input: {user_input}"

        # Log both the user input and the ChatGPT response
        self.add_log({"log": user_input, "response": response_text})

        print(response_text)
        return response_text

    def interact(self):
        """
        Begin an interactive loop where ChatGPT responds to user input and logs interactions.
        """
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting...")
                break
            response = self.make_informed_decision(user_input)
            # Optionally, refresh logs after each interaction
            self.logs = self.get_all_data()

if __name__ == '__main__':
    # Initialize with your API URL and API Key
    api_url = "http://84.203.90.102:8000"
    api_key = "9647cf29c1e313d17b661d2508cbf2b2"

    # Create an instance of the AutonomousChatGPTModule
    module = AutonomousChatGPTModule(api_url, api_key)

    # Start the interaction loop
    module.interact()
