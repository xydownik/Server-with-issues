import pickle
import requests

payload = {'hello': 'world'}

p = pickle.dumps(payload)

# resp = requests.post("http://127.0.0.1:5000/deserialize", data=p)
resp = requests.post("http://127.0.0.1:5001/deserialize", data=p)

print("Status:", resp.status_code)
print("Response:", resp.text)
