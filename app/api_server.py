from flask import Flask, request, jsonify

app = Flask(__name__)

# Load API key from .key file
with open(".api.key", "r") as key_file:
    VALID_API_KEY = key_file.read().strip()

# Example data
logs = []

def check_api_key():
    api_key = request.headers.get('Authorization')
    if api_key != f"Bearer {VALID_API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401
    return None

@app.route('/get_new_data', methods=['GET'])
def get_new_data():
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    return jsonify(logs), 200

@app.route('/add_log', methods=['POST'])
def add_log():
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    log_entry = request.json
    logs.append(log_entry)
    return jsonify({"message": "Log added successfully!"}), 200

@app.route('/process_data', methods=['POST'])
def process_data():
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    data = request.json.get('data', {})
    return jsonify({"message": "Data processed successfully!", "processed_data": data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
