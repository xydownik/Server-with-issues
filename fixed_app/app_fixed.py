from flask import Flask, request, jsonify
import os, json

# load config from environment or .env (you can use python-dotenv in dev)
from dotenv import load_dotenv
load_dotenv()  # optional for local development .env file

app = Flask(__name__)

# ----- FIX 1: Disable DEBUG in production -----
app.config['DEBUG'] = False

# ----- FIX 2: Use environment variable for secret -----
API_KEY = os.getenv('MY_APP_API_KEY')

# ----- FIX 3: Replace unsafe deserialization with safe JSON -----
@app.route('/deserialize', methods=['POST'])
def deserialize():
    try:
        obj = request.get_json(force=True)
        if not isinstance(obj, dict):
            return jsonify({"error": "invalid format"}), 400
        return jsonify({"status": "ok", "repr": obj})
    except Exception:
        return jsonify({"error": "invalid payload"}), 400

@app.route('/cause_error')
def cause_error():
    raise RuntimeError("An internal error occurred.")

@app.route('/secret')
def secret():
    key = request.args.get('key', '')
    if API_KEY and key == API_KEY:
        return jsonify({"data": "Very sensitive data: user-db-backup.sql"})
    return jsonify({"error": "invalid key"}), 403

@app.errorhandler(500)
def handle_internal(e):
    return jsonify({"error": "internal server error"}), 500

@app.route('/')
def home():
    return "Fixed Server. Endpoints: /deserialize, /cause_error, /secret"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
