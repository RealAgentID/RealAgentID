import json
import redis
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

AGENT_TTL = 86400

def register_agent_from_key(agent_id, public_key_pem_path):
    with open(public_key_pem_path, "rb") as f:
        public_key = load_pem_public_key(f.read())
    public_key_hex = public_key.public_bytes(
        Encoding.Raw, PublicFormat.Raw
    ).hex()
    r.setex(f"agent:{agent_id}", AGENT_TTL, json.dumps({"public_key": public_key_hex}))
    print(f"[+] Agent '{agent_id}' registered in Redis (TTL: {AGENT_TTL}s).")

def get_public_key(agent_id):
    data = r.get(f"agent:{agent_id}")
    if data is None:
        return None
    return json.loads(data).get("public_key")

def list_agents():
    keys = r.keys("agent:*")
    if not keys:
        print("No agents registered.")
        return
    for key in keys:
        agent_id = key.split(":", 1)[1]
        data = r.get(key)
        if data:
            pub_key = json.loads(data).get("public_key", "")
            ttl = r.ttl(key)
            print(f"  {agent_id}: {pub_key[:16]}... (TTL: {ttl}s)")

if __name__ == "__main__":
    list_agents()
