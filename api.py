from flask import Flask, request, jsonify
import sys, os, json, redis

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))
from registry import get_public_key
from signing import verify_message_from_registry

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/health', methods=['GET'])
def health():
    try:
        r.ping()
        return jsonify({"status": "ok", "redis": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "redis": str(e)}), 500

@app.route('/agents', methods=['GET'])
def list_all_agents():
    keys = r.keys("agent:*")
    agents = {}
    for key in keys:
        agent_id = key.split(":", 1)[1]
        data = r.get(key)
        if data:
            pub = json.loads(data).get("public_key", "")
            ttl = r.ttl(key)
            agents[agent_id] = {"public_key_preview": pub[:16] + "...", "ttl_seconds": ttl}
    return jsonify({"agents": agents}), 200

@app.route('/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    key = get_public_key(agent_id)
    if not key:
        return jsonify({"error": "Agent not found"}), 404
    ttl = r.ttl("agent:" + agent_id)
    return jsonify({"agent_id": agent_id, "public_key_preview": key[:16] + "...", "ttl_seconds": ttl}), 200

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    if not data or "signed_message" not in data:
        return jsonify({"error": "Missing signed_message"}), 400
    try:
        if isinstance(data["signed_message"], dict):
            signed_json = json.dumps(data["signed_message"])
        else:
            signed_json = data["signed_message"]
        message = verify_message_from_registry(signed_json)
        return jsonify({"result": "VALID", "agent_id": message["agent_id"], "channel": message["channel"]}), 200
    except Exception as e:
        return jsonify({"result": "INVALID", "reason": str(e)}), 403

if __name__ == "__main__":
    print("[RealAgentID] API starting on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
