from flask import Flask, jsonify, request

app = Flask(__name__)
logs = []
errors = []

@app.route("/log", methods=["POST"])
def log():
    data = request.json
    if data:
        logs.append(data)
    return {"status": "ok"}

@app.route("/error", methods=["POST"])
def error():
    data = request.json
    if data:
        errors.append(data)
    return {"status": "ok"}

@app.route("/logs")
def get_logs():
    return jsonify(logs)

@app.route("/errors")
def get_errors():
    return jsonify(errors)

if __name__ == "__main__":
    app.run(port=8124)