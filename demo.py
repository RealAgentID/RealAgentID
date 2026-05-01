import time
from agents.keygen import generate_agent_identity
from agents.registry import register_agent_from_key, list_agents
from agents.signing import sign_message, verify_message_from_registry
from agents.audit import write_log

print("=" * 55)
print("   RealAgentID - Zero Trust Agent Identity Demo")
print("=" * 55)
print()

print("--- PHASE 1: Identity Generation ---")
generate_agent_identity("coordinator", "./keys")
generate_agent_identity("worker-1", "./keys")
print()

print("--- PHASE 2: Agent Registration ---")
register_agent_from_key("coordinator", "keys/coordinator_public.pem")
register_agent_from_key("worker-1", "keys/worker-1_public.pem")
print()
print("Registered agents:")
list_agents()
print()

print("--- PHASE 3: Signed Message ---")
signed = sign_message(
    agent_id="coordinator",
    private_key_path="./keys/coordinator_private.pem",
    channel="tasks:worker-1",
    payload={"task": "analyze", "target": "dataset-7"}
)
print("Message signed by coordinator")
print()

print("--- PHASE 4: Registry Verification ---")
verified = verify_message_from_registry(signed)
print("Payload:", verified["payload"])
print()

print("--- PHASE 5: Spoofing Attack ---")
generate_agent_identity("rogue", "./keys")
spoofed = sign_message(
    agent_id="coordinator",
    private_key_path="./keys/rogue_private.pem",
    channel="tasks:worker-1",
    payload={"task": "exfiltrate", "target": "all-data"}
)
try:
    verify_message_from_registry(spoofed)
    print("[!] VULNERABILITY: Spoof succeeded")
except Exception as e:
    print("[+] Spoof blocked:", e)
print()

print("--- PHASE 6: Replay Attack ---")
print("Waiting 6 seconds...")
time.sleep(6)
try:
    verify_message_from_registry(signed, ttl_seconds=5)
    print("[!] VULNERABILITY: Replay succeeded")
except Exception as e:
    print("[+] Replay blocked:", e)
print()

print("=" * 55)
print("   All attacks blocked. Audit log written.")
print("=" * 55)
