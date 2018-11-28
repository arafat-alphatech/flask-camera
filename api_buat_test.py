from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/camera")
def hello():
    return jsonify({"nomor": 1}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
