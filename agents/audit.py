# RealAgentID Audit Module
# Compliance note: This module logs metadata only by default.
# Payload content is never logged unless explicitly enabled.
# See COMPLIANCE.md for framework mappings and data retention guidance.
# Designed toward: SOC 2, GDPR, HIPAA, NIST AI RMF, EU AI Act

import json
import time
import os
from datetime import datetime, timezone

LOG_FILE = "./logs/realagentid_audit.log"

def write_log(event: str, agent_id: str, channel: str, result: str, reason: str = None, message_id: str = None, latency_ms: float = None):
    os.makedirs("./logs", exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "agent_id": agent_id,
        "channel": channel,
        "result": result,
    }
    if reason:
        entry["reason"] = reason
    if message_id:
        entry["message_id"] = message_id
    if latency_ms is not None:
        entry["latency_ms"] = round(latency_ms, 3)
    line = json.dumps(entry)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    print(f"[RealAgentID AUDIT] {result} | {event} | agent: {agent_id} | channel: {channel}")

def read_log():
    if not os.path.exists(LOG_FILE):
        print("No audit log found.")
        return
    with open(LOG_FILE, "r") as f:
        for line in f:
            print(line.strip())

if __name__ == "__main__":
    read_log()
