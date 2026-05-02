from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import (
    Encoding, PrivateFormat, PublicFormat, NoEncryption,
    load_pem_private_key, load_pem_public_key
)
from cryptography.exceptions import InvalidSignature
import json
import time
import uuid
import base64
import sys
import os
import redis

sys.path.insert(0, os.path.dirname(__file__))
import audit
import schema

from connection import get_redis, REPLAY_TTL, ROLE_PERMISSIONS
r = get_redis()

def load_private_key(path: str):
    with open(path, "rb") as f:
        return load_pem_private_key(f.read(), password=None)

def load_public_key(path: str):
    with open(path, "rb") as f:
        return load_pem_public_key(f.read())

def sign_message(agent_id: str, private_key_path: str, channel: str, payload: dict) -> str:
    private_key = load_private_key(private_key_path)
    message = {
        "message_id": str(uuid.uuid4()),
        "agent_id": agent_id,
        "channel": channel,
        "payload": payload,
        "timestamp": time.time()
    }
    message_bytes = json.dumps(message, sort_keys=True).encode()
    signature = private_key.sign(message_bytes)
    signature_b64 = base64.b64encode(signature).decode()
    signed = {"message": message, "signature": signature_b64}
    return json.dumps(signed)

def verify_message(signed_json: str, public_key_path: str) -> dict:
    signed = json.loads(signed_json)
    message = signed["message"]
    signature = base64.b64decode(signed["signature"])
    public_key = load_public_key(public_key_path)
    message_bytes = json.dumps(message, sort_keys=True).encode()
    try:
        start = time.time()
        public_key.verify(signature, message_bytes)
        latency = (time.time() - start) * 1000
        print(f"[RealAgentID] ✓ Signature VALID - from agent: {message['agent_id']}")
        audit.write_log(
            event="signature_verified",
            agent_id=message["agent_id"],
            channel=message["channel"],
            result="VALID",
            message_id=message.get("message_id"),
            latency_ms=latency
        )
        return message
    except InvalidSignature:
        print(f"[RealAgentID] X Signature INVALID - message rejected")
        audit.write_log(
            event="signature_rejected",
            agent_id=message.get("agent_id", "unknown"),
            channel=message.get("channel", "unknown"),
            result="INVALID",
            reason="tamper_detected"
        )
        raise

def verify_message_from_registry(signed_json: str, ttl_seconds: int = 300) -> dict:
    from registry import get_public_key, get_role
    signed = json.loads(signed_json)
    message = signed["message"]
    agent_id = message["agent_id"]
    message_id = message.get("message_id")
    channel = message.get("channel", "unknown")
    payload = message.get("payload", {})

    # TTL check
    message_age = time.time() - message["timestamp"]
    if message_age > ttl_seconds:
        print(f"[RealAgentID] X Message expired")
        raise ValueError(f"Message expired: {message_age:.1f}s exceeds TTL {ttl_seconds}s")

    # Replay check
    replay_key = f"seen_msg:{message_id}"
    if r.exists(replay_key):
        print(f"[RealAgentID] X Replay attack detected - message_id already used: {message_id}")
        audit.write_log(
            event="replay_attack_blocked",
            agent_id=agent_id,
            channel=channel,
            result="INVALID",
            message_id=message_id,
            reason="replay_detected"
        )
        raise ValueError(f"Replay attack blocked: message_id {message_id} already used")
    r.setex(replay_key, REPLAY_TTL, "1")

    # Payload schema validation
    valid, reason = schema.validate_payload(channel, payload)
    if not valid:
        print(f"[RealAgentID] X Payload schema violation - {reason}")
        audit.write_log(
            event="payload_schema_violation",
            agent_id=agent_id,
            channel=channel,
            result="INVALID",
            message_id=message_id,
            reason=reason
        )
        raise ValueError(f"Payload schema violation: {reason}")

    # Registry lookup
    public_key_hex = get_public_key(agent_id)
    if not public_key_hex:
        raise ValueError(f"[RealAgentID] Unknown agent: {agent_id} - not in registry")

    # Role check
    agent_role = get_role(agent_id)
    allowed_channels = ROLE_PERMISSIONS.get(agent_role, [])
    channel_prefix = channel.split(":")[0] + ":*"
    if "*" not in allowed_channels and channel_prefix not in allowed_channels:
        print(f"[RealAgentID] X Role violation - agent: {agent_id} has role '{agent_role}', not permitted on channel '{channel}'")
        audit.write_log(
            event="role_violation",
            agent_id=agent_id,
            channel=channel,
            result="INVALID",
            message_id=message_id,
            reason=f"role '{agent_role}' not permitted on channel '{channel}'"
        )
        raise ValueError(f"Role violation: agent '{agent_id}' has role '{agent_role}', not permitted on channel '{channel}'")

    public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key_hex))
    signature = base64.b64decode(signed["signature"])
    message_bytes = json.dumps(message, sort_keys=True).encode()
    try:
        start = time.time()
        public_key.verify(signature, message_bytes)
        latency = (time.time() - start) * 1000
        print(f"[RealAgentID] ✓ Registry verification VALID - agent: {agent_id}")
        audit.write_log(
            event="registry_verification",
            agent_id=agent_id,
            channel=channel,
            result="VALID",
            message_id=message_id,
            latency_ms=latency
        )
        return message
    except InvalidSignature:
        print(f"[RealAgentID] X Registry verification FAILED - agent: {agent_id}")
        audit.write_log(
            event="registry_verification",
            agent_id=agent_id,
            channel=channel,
            result="INVALID",
            reason="tamper_detected"
        )
        raise

if __name__ == "__main__":
    print("--- RealAgentID Signing Test ---")
    signed = sign_message(
        agent_id="coordinator",
        private_key_path="./keys/coordinator_private.pem",
        channel="tasks:worker-1",
        payload={"task": "analyze", "target": "dataset-7"}
    )
    print("Signed message created")
    verified = verify_message(
        signed_json=signed,
        public_key_path="./keys/coordinator_public.pem"
    )
    print(f"Verified payload: {verified['payload']}")

