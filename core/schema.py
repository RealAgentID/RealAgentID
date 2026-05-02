# RealAgentID Payload Schema Validator
# Defines allowed payload structures per channel
# Messages with payloads outside these schemas are rejected

CHANNEL_SCHEMAS = {
    "tasks:worker-1": {
        "required_fields": ["task", "target"],
        "allowed_tasks": ["analyze", "run_report", "scan", "monitor"],
        "forbidden_tasks": ["exfiltrate", "delete", "override", "shutdown"]
    },
    "tasks:worker-2": {
        "required_fields": ["task", "target"],
        "allowed_tasks": ["analyze", "run_report", "scan", "monitor"],
        "forbidden_tasks": ["exfiltrate", "delete", "override", "shutdown"]
    }
}

def validate_payload(channel: str, payload: dict) -> tuple:
    if channel not in CHANNEL_SCHEMAS:
        return True, None
    schema = CHANNEL_SCHEMAS[channel]
    for field in schema.get("required_fields", []):
        if field not in payload:
            return False, f"Missing required field: {field}"
    task = payload.get("task", "")
    if task in schema.get("forbidden_tasks", []):
        return False, f"Forbidden task detected: {task}"
    if task not in schema.get("allowed_tasks", []):
        return False, f"Unknown task: {task}"
    return True, None
