import json, os
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

REGISTRY_FILE = "agent_registry.json"

def register_agent_from_key(agent_id, public_key_pem_path):
    with open(public_key_pem_path, "rb") as f:
        public_key = load_pem_public_key(f.read())
    public_key_hex = public_key.public_bytes(
        Encoding.Raw, PublicFormat.Raw
    ).hex()
    registry = load_registry()
    registry[agent_id] = {"public_key": public_key_hex}
    save_registry(registry)
    print(f"[+] Agent '{agent_id}' registered.")

def get_public_key(agent_id):
    registry = load_registry()
    return registry.get(agent_id, {}).get("public_key")

def list_agents():
    registry = load_registry()
    if not registry:
        print("No agents registered.")
        return
    for agent_id, data in registry.items():
        print(f"  {agent_id}: {data['public_key'][:16]}...")

def load_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE) as f:
            return json.load(f)
    return {}

def save_registry(registry):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)

if __name__ == "__main__":
    list_agents()
