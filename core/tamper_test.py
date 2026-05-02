from signing import sign_message, verify_message
import json

print("--- RealAgentID Tamper Test ---")

# Coordinator signs a legitimate message
signed_json = sign_message(
    agent_id="coordinator",
    private_key_path="./keys/coordinator_private.pem",
    channel="tasks:worker-1",
    payload={"task": "analyze", "target": "dataset-7"}
)

# Attacker intercepts and modifies the payload
signed = json.loads(signed_json)
signed["message"]["payload"]["target"] = "INJECTED-TARGET"
tampered_json = json.dumps(signed)

print("Tampered message created — attempting verification...")

try:
    verify_message(
        signed_json=tampered_json,
        public_key_path="./keys/coordinator_public.pem"
    )
except Exception as e:
    print("[RealAgentID] Tamper detected - message blocked:", str(e))
