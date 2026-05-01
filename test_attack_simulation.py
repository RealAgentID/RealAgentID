from agents.signing import sign_message, verify_message_from_registry
from agents.keygen import generate_agent_identity
from agents.audit import write_log
import os
import time

print("=== RealAgentID Attack Simulation ===")
print()

# ─── TEST 1: SPOOFING ATTACK ───
print("--- Test 1: Spoofing Attack ---")
print("[*] Generating rogue agent identity...")
generate_agent_identity("rogue", "./keys")

print("[*] Rogue agent signing message as 'coordinator'...")
signed = sign_message(
    agent_id="coordinator",
    private_key_path="./keys/rogue_private.pem",
    channel="tasks:worker-1",
    payload={"task": "exfiltrate", "target": "all-data"}
)
print("[*] Spoofed message created")
print()

print("[*] Attempting registry verification...")
try:
    verified = verify_message_from_registry(signed)
    print("[!] CRITICAL: Spoofed message accepted - VULNERABILITY")
except Exception as e:
    print(f"[+] Spoofing attack blocked: {e}")

print()

# ─── TEST 2: REPLAY ATTACK ───
print("--- Test 2: Replay Attack ---")
print("[*] Signing a legitimate message as 'coordinator'...")
legitimate = sign_message(
    agent_id="coordinator",
    private_key_path="./keys/coordinator_private.pem",
    channel="tasks:worker-1",
    payload={"task": "run_report", "target": "q1"}
)
print("[*] Legitimate message signed.")
print()

print("[*] Verifying legitimate message (should pass)...")
try:
    verified = verify_message_from_registry(legitimate)
    print("[+] Legitimate message accepted.")
except Exception as e:
    print(f"[!] Unexpected failure: {e}")

print()
print("[*] Replaying same message after delay...")
time.sleep(2)
try:
    verified = verify_message_from_registry(legitimate)
    print("[!] CRITICAL: Replay accepted - VULNERABILITY")
except Exception as e:
    print(f"[+] Replay attack blocked: {e}")

print()
print("=== Simulation Complete ===")
