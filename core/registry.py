import json
import redis
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from connection import get_redis, AGENT_TTL, VALID_ROLES
r = get_redis()

def register_agent_from_key(agent_id, public_key_pem_path, role="worker"):
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role: {role}. Must be one of {VALID_ROLES}")
    with open(public_key_pem_path, "rb") as f:
        public_key = load_pem_public_key(f.read())
    public_key_hex = public_key.public_bytes(
        Encoding.Raw, PublicFormat.Raw
    ).hex()
    data = {"public_key": public_key_hex, "role": role}
    r.setex(f"agent:{agent_id}", AGENT_TTL, json.dumps(data))
    print(f"[+] Agent '{agent_id}' registered in Redis as role='{role}' (TTL: {AGENT_TTL}s).")

def get_public_key(agent_id):
    data = r.get(f"agent:{agent_id}")
    if data is None:
        return None
    return json.loads(data).get("public_key")

def get_role(agent_id):
    data = r.get(f"agent:{agent_id}")
    if data is None:
        return None
    return json.loads(data).get("role")

def revoke_agent(agent_id):
    key = f"agent:{agent_id}"
    if r.exists(key):
        r.delete(key)
        print(f"[!] Agent '{agent_id}' revoked and removed from registry.")
        return True
    return False

def list_agents():
    keys = r.keys("agent:*")
    if not keys:
        print("No agents registered.")
        return
    for key in keys:
        agent_id = key.split(":", 1)[1]
        data = r.get(key)
        if data:
            parsed = json.loads(data)
            pub_key = parsed.get("public_key", "")
            role = parsed.get("role", "unknown")
            ttl = r.ttl(key)
            print(f"  {agent_id} [{role}]: {pub_key[:16]}... (TTL: {ttl}s)")

if __name__ == "__main__":
    list_agents()
