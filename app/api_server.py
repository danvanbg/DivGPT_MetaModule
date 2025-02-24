# api_server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Example data
logs = []

# Define a valid API key
VALID_API_KEY = "9647cf29c1e313d17b661d2508cbf2b2"  # Replace this with your actual API key

# Function to check the API key in the request header
def check_api_key():
    api_key = request.headers.get('Authorization')
    if api_key != f"Bearer {VALID_API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401  # Unauthorized if the key doesn't match
    return None  # Return None if the API key is valid

@app.route('/get_new_data', methods=['GET'])
def get_new_data():
    # Validate the API key
    auth_error = check_api_key()
    if auth_error:
        return auth_error  # If the API key is invalid, return error

    return jsonify(logs), 200

@app.route('/add_log', methods=['POST'])
def add_log():
    # Validate the API key
    auth_error = check_api_key()
    if auth_error:
        return auth_error  # If the API key is invalid, return error

    log_entry = request.json
    logs.append(log_entry)
    return jsonify({"message": "Log added successfully!"}), 200

@app.route('/process_data', methods=['POST'])
def process_data():
    # Validate the API key
    auth_error = check_api_key()
    if auth_error:
        return auth_error  # If the API key is invalid, return error

    data = request.json.get('data', {})
    # Here you can add logic for data processing or ChatGPT interaction
    return jsonify({"message": "Data processed successfully!", "processed_data": data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
