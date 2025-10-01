# app.py  (vulnerable demo)
from flask import Flask, request, jsonify
import os, pickle

app = Flask(__name__)

# ----- ISSUE 1: DEBUG / detailed error info enabled -----
app.config['DEBUG'] = True

# ----- ISSUE 2: Hardcoded "secret" in code -----
API_KEY = "NOT_REALLY_SECRET_API_KEY_12345"

# ----- ISSUE 3: Insecure deserialization endpoint -----
@app.route('/deserialize', methods=['POST'])
def deserialize():
    payload = request.get_data()
    try:
        obj = pickle.loads(payload)
        return jsonify({"status": "ok", "repr": repr(obj)})
    except Exception as e:
        raise

@app.route('/cause_error')
def cause_error():
    raise RuntimeError(f"Some internal runtime error. API_KEY={API_KEY}")

@app.route('/secret')
def secret():
    key = request.args.get('key', '')
    if key == API_KEY:
        return jsonify({"data": "Very sensitive data: user-db-backup.sql"})
    return jsonify({"error": "invalid key"}), 403

@app.route('/')
def home():
    return "Risky Server. Endpoints: /serialize, /deserialize, /cause_error, /secret"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
