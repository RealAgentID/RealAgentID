from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding, PrivateFormat, PublicFormat, NoEncryption
)
import os
import json

def generate_agent_identity(agent_name: str, keys_dir: str = "./keys"):
    # Generate Ed25519 keypair
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Serialize keys
    private_bytes = private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    public_bytes = public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

    # Write to keys directory
    os.makedirs(keys_dir, exist_ok=True)
    with open(f"{keys_dir}/{agent_name}_private.pem", "wb") as f:
        f.write(private_bytes)
    with open(f"{keys_dir}/{agent_name}_public.pem", "wb") as f:
        f.write(public_bytes)

    # Write identity manifest
    manifest = {"agent_id": agent_name, "public_key_file": f"{keys_dir}/{agent_name}_public.pem"}
    with open(f"{keys_dir}/{agent_name}_identity.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"[RealAgentID] Identity generated for: {agent_name}")
    print(f"  Private key: {keys_dir}/{agent_name}_private.pem")
    print(f"  Public key:  {keys_dir}/{agent_name}_public.pem")
    print(f"  Manifest:    {keys_dir}/{agent_name}_identity.json")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 keygen.py <agent_name>")
        sys.exit(1)
    generate_agent_identity(sys.argv[1])
