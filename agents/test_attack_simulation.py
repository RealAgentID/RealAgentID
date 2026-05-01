# ─── TEST 3: MALICIOUS PAYLOAD ───
print("--- Test 3: Malicious Payload Attack ---")
print("[*] Legitimate agent sending forbidden task...")
malicious = sign_message(
    agent_id="coordinator",
    private_key_path="./keys/coordinator_private.pem",
    channel="tasks:worker-1",
    payload={"task": "exfiltrate", "target": "all-data"}
)
try:
    verified = verify_message_from_registry(malicious)
    print("[!] CRITICAL: Malicious payload accepted - VULNERABILITY")
except Exception as e:
    print(f"[+] Malicious payload blocked: {e}")

print()
