with open("agents/signing.py", "r") as f:
    content = f.read()
old = "    agent_id = message[\"agent_id\"]\n    public_key_hex"
new = "    agent_id = message[\"agent_id\"]\n    message_age = time.time() - message[\"timestamp\"]\n    if message_age > ttl_seconds:\n        print(f\"[RealAgentID] X Message expired\")\n        raise ValueError(f\"Message expired: {message_age:.1f}s exceeds TTL {ttl_seconds}s\")\n    public_key_hex"
if old in content:
    with open("agents/signing.py", "w") as f:
        f.write(content.replace(old, new))
    print("Done")
else:
    print("Pattern not found")
