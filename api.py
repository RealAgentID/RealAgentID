from flask import Flask, jsonify
from flask_cors import CORS
from core.registry import list_agents
from core.audit import read_log

app = Flask(__name__)
CORS(app)

@app.route('/api/agents')
def agents():
    return jsonify(list_agents() or [])

@app.route('/api/audit')
def audit():
    logs = read_log() or []
    return jsonify(logs)

if __name__ == '__main__':
    app.run(port=5050, debug=True)
