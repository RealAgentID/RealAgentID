import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from realagentid import Agent
from core.audit import read_log
from datetime import datetime

FINTECH_ROLES = ["signal_gen", "risk_guard", "order_router", "compliance_log"]

SIGNAL_SCHEMA = {
    "required": ["action", "asset", "confidence"],
    "valid_actions": ["buy", "sell", "hold"],
    "valid_assets": ["BTC", "ETH", "LNG", "SILVER", "SPY", "CACC"]
}

RISK_SCHEMA = {
    "required": ["signal_id", "risk_level", "approved"],
    "valid_risk_levels": ["low", "medium", "high", "critical"]
}

def validate_payload(payload, schema):
    for field in schema.get("required", []):
        if field not in payload:
            return False, f"Missing required field: {field}"
    if "valid_actions" in schema:
        if payload.get("action") not in schema["valid_actions"]:
            return False, f"Invalid action: {payload.get('action')}"
    if "valid_assets" in schema:
        if payload.get("asset") not in schema["valid_assets"]:
            return False, f"Invalid asset: {payload.get('asset')}"
    if "valid_risk_levels" in schema:
        if payload.get("risk_level") not in schema["valid_risk_levels"]:
            return False, f"Invalid risk level: {payload.get('risk_level')}"
    if "max_amount" in schema:
        if payload.get("amount", 0) > schema["max_amount"]:
            return False, f"Amount exceeds maximum: {payload.get('amount')}"
    return True, "valid"

class SignalAgent(Agent):
    def __init__(self, name="signal_gen"):
        super().__init__(name=name, role="signal_gen")

    def generate_signal(self, action, asset, confidence, channel="signal:default"):
        payload = {"action": action, "asset": asset, "confidence": confidence, "timestamp": datetime.utcnow().isoformat()}
        valid, reason = validate_payload(payload, SIGNAL_SCHEMA)
        if not valid:
            raise ValueError(f"Invalid signal payload: {reason}")
        return self.sign(payload, channel=channel)

class RiskGuard(Agent):
    def __init__(self, name="risk_guard"):
        super().__init__(name=name, role="risk_guard")

    def evaluate(self, signal_id, risk_level, approved, channel="risk:default"):
        payload = {"signal_id": signal_id, "risk_level": risk_level, "approved": approved, "timestamp": datetime.utcnow().isoformat()}
        valid, reason = validate_payload(payload, RISK_SCHEMA)
        if not valid:
            raise ValueError(f"Invalid risk payload: {reason}")
        return self.sign(payload, channel=channel)

class OrderRouter(Agent):
    def __init__(self, name="order_router", max_order_amount=100000):
        super().__init__(name=name, role="order_router")
        self.max_order_amount = max_order_amount

    def route(self, signal_id, risk_id, action, asset, amount, channel="order:default"):
        schema = {"required": ["signal_id", "risk_id", "action", "asset", "amount"], "max_amount": self.max_order_amount}
        payload = {"signal_id": signal_id, "risk_id": risk_id, "action": action, "asset": asset, "amount": amount, "timestamp": datetime.utcnow().isoformat()}
        valid, reason = validate_payload(payload, schema)
        if not valid:
            raise ValueError(f"Invalid order payload: {reason}")
        return self.sign(payload, channel=channel)

class ComplianceLog(Agent):
    def __init__(self, name="compliance_log"):
        super().__init__(name=name, role="compliance_log")

    def record(self, event, details, channel="audit:default"):
        payload = {"event": event, "details": details, "timestamp": datetime.utcnow().isoformat()}
        return self.sign(payload, channel=channel)

    def get_audit_trail(self):
        return read_log()
