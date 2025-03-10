import os
import requests
from flask import Flask, jsonify, request

# Initialize Flask app
app = Flask(__name__)

# Load API key from system environment
API_KEY = os.getenv("WEYSENTINEL_API_KEY")

# GitHub Credentials
GITHUB_TOKEN = os.getenv("WEYSENTINEL_GITHUB_PAT")
REPO_OWNER = "debaedoma"
REPO_NAME = "weyoto-assist"


# Function to fetch latest commits
def get_latest_commits():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch commits: {response.status_code}"}


# Flask route to fetch latest commits
@app.route('/get-latest-code', methods=['GET'])
def fetch_code():
    # Step 1: Get API Key from the request header
    provided_key = request.headers.get("X-API-KEY")

    # Step 2: Check if API Key is missing or incorrect
    if not provided_key or provided_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401  # Return 401 if unauthorized

    # Step 3: If API Key is correct, fetch and return commits
    commits = get_latest_commits()
    return jsonify(commits)


# Run Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

