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
sys.path.insert(0, os.path.dirname(__file__))
import audit

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
        print(f"[RealAgentID] ✓ Signature VALID — from agent: {message['agent_id']}")
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
        print(f"[RealAgentID] ✗ Signature INVALID — message rejected")
        audit.write_log(
            event="signature_rejected",
            agent_id=message.get("agent_id", "unknown"),
            channel=message.get("channel", "unknown"),
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

