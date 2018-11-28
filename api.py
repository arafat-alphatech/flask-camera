from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return jsonify({"score": 10, "codes": 10}), 200
   # return "<h1 style='color:blue'>Hello There!</h1>" 

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug= True)
