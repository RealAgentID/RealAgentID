import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from realagentid import Agent
from core.audit import read_log
import json
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

ORDER_SCHEMA = {
    "required": ["signal_id", "risk_id", "action", "asset", "amount"],
    "max_amount": 100000
}

def validate_payload(payload: dict, schema: dict) -> tuple:
    for field in schema.get("required", []):
        if field not in payload:
            return False, f"Missing required field: {field}"
    if "valid_actions" in schema:
        if payload.get("action") not in schema["valid_actions"]:
            return False, f"Invalid action: {payload.get('action')}"
    if "valid_assets" in schema:
        if payload.get("asset") not in schema["valid_assets"]:
            return False, f"Invalid asset: {payload.get('asset')}"
    if "max_amount" in schema:
        if payload.get("amount", 0) > schema["max_amount"]:
            return False, f"Amount exceeds maximum: {payload.get('amount')}"
    return True, "valid"

class SignalAgent(Agent):
    def __init__(self, name="signal_gen"):
        super().__init__(name=name, role="signal_gen")

    def generate_signal(self, action: str, asset: str, confidence: float, channel: str = "signal:default"):
        payload = {
            "action": action,
            "asset": asset,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }
        valid, reason = validate_payload(payload, SIGNAL_SCHEMA)
        if not valid:
            raise ValueError(f"Invalid signal payload: {reason}")
        return self.sign(payload, channel=channel)

class RiskGuard(Agent):
    def __init__(self, name="risk_guard"):
        super().__init__(name=name, role="risk_guard")

    def evaluate(self, signal_id: str, risk_level: str, approved: bool, channel: str = "risk:default"):
        payload = {
            "signal_id": signal_id,
            "risk_level": risk_level,
            "approved": approved,
            "timestamp": datetime.utcnow().isoformat()
        }
        valid, reason = validate_payload(payload, RISK_SCHEMA)
        if not valid:
            raise ValueError(f"Invalid risk payload: {reason}")
        return self.sign(payload, channel=channel)

class OrderRouter(Agent):
    def __init__(self, name="order_router"):
        super().__init__(name=name, role="order_router")

    def route(self, signal_id: str, risk_id: str, action: str, asset: str, amount: float, channel: str = "order:default"):
        payload = {
            "signal_id": signal_id,
            "risk_id": risk_id,
            "action": action,
            "asset": asset,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat()
        }
        valid, reason = validate_payload(payload, ORDER_SCHEMA)
        if not valid:
            raise ValueError(f"Invalid order payload: {reason}")
        return self.sign(payload, channel=channel)

class ComplianceLog(Agent):
    def __init__(self, name="compliance_log"):
        super().__init__(name=name, role="compliance_log")

    def record(self, event: str, details: dict, channel: str = "audit:default"):
        payload = {
            "event": event,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        return self.sign(payload, channel=channel)

    def get_audit_trail(self):
        return read_log()
