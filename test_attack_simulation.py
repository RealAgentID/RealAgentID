from agents.signing import sign_message, verify_message_from_registry
from agents.keygen import generate_agent_identity
import os

print("=== RealAgentID Attack Simulation ===")
print()

# Generate a rogue agent keypair - not registered
print("[*] Generating rogue agent identity...")
generate_agent_identity("rogue", "./keys")

# Rogue agent signs a message pretending to be coordinator
print("[*] Rogue agent signing message as 'coordinator'...")
signed = sign_message(
    agent_id="coordinator",
    private_key_path="./keys/rogue_private.pem",
    channel="tasks:worker-1",
    payload={"task": "exfiltrate", "target": "all-data"}
)
print("[*] Spoofed message created")
print()

# Attempt registry verification - should fail
print("[*] Attempting registry verification...")
try:
    verified = verify_message_from_registry(signed)
    print("[!] CRITICAL: Spoofed message accepted - VULNERABILITY")
except Exception as e:
    print(f"[+] Attack blocked: {e}")
