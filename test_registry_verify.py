from agents.signing import sign_message, verify_message_from_registry

# Coordinator signs a message
signed = sign_message(
    agent_id="coordinator",
    private_key_path="./keys/coordinator_private.pem",
    channel="tasks:worker-1",
    payload={"task": "analyze", "target": "dataset-7"}
)
print("Signed message created")

# Verify using registry only - no key file needed
verified = verify_message_from_registry(signed)
print(f"Registry verified payload: {verified['payload']}")
