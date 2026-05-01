import time
from agents.signing import sign_message, verify_message_from_registry

print("=== RealAgentID Replay Attack Simulation ===")
print()

print("[*] Coordinator signing legitimate message...")
signed = sign_message(
    agent_id="coordinator",
    private_key_path="./keys/coordinator_private.pem",
    channel="tasks:worker-1",
    payload={"task": "analyze", "target": "dataset-7"}
)
print("[+] Message signed")
print()

print("[*] Immediate verification (should pass)...")
try:
    verified = verify_message_from_registry(signed, ttl_seconds=5)
    print("[+] Verified:", verified["payload"])
except Exception as e:
    print(f"[!] Failed: {e}")

print()
print("[*] Waiting 6 seconds to simulate replay attempt...")
time.sleep(6)
print()

print("[*] Replaying expired message (should be blocked)...")
try:
    verified = verify_message_from_registry(signed, ttl_seconds=5)
    print("[!] CRITICAL: Replay attack succeeded - VULNERABILITY")
except Exception as e:
    print(f"[+] Replay blocked: {e}")
