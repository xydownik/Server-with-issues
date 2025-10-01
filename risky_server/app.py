# app.py  (vulnerable demo)
from flask import Flask, request, jsonify
import os, pickle

app = Flask(__name__)

# ----- ISSUE 1: DEBUG / detailed error info enabled -----
# (This will show full stack traces and internal info)
app.config['DEBUG'] = True

# ----- ISSUE 2: Hardcoded "secret" in code -----
API_KEY = "NOT_REALLY_SECRET_API_KEY_12345"   # <- intentionally hardcoded secret

# ----- ISSUE 3: Insecure deserialization endpoint -----
# Accepts a 'data' parameter and unpickles it (unsafe)
@app.route('/deserialize', methods=['POST'])
def deserialize():
    payload = request.get_data()
    try:
        obj = pickle.loads(payload)   # UNSAFE: arbitrary code could run if payload crafted
        return jsonify({"status": "ok", "repr": repr(obj)})
    except Exception as e:
        # because DEBUG=True, stack traces will be shown in-browser/console
        raise

# Simple endpoint that leaks internal info via error
@app.route('/cause_error')
def cause_error():
    # This will raise an exception and reveal the stack trace because DEBUG=True
    raise RuntimeError(f"Some internal runtime error. API_KEY={API_KEY}")  # includes secret in message

# endpoint that returns a resource only if they provide the API_KEY
@app.route('/secret')
def secret():
    key = request.args.get('key', '')
    if key == API_KEY:
        return jsonify({"data": "Very sensitive data: user-db-backup.sql"})
    return jsonify({"error": "invalid key"}), 403

# Minimal home
@app.route('/')
def home():
    return "Risky Server. Endpoints: /serialize, /deserialize, /cause_error, /secret"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
