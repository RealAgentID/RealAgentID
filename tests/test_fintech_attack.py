import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters.fintech import SignalAgent, RiskGuard, OrderRouter

def test_schema_violation():
    print("\n[ATTACK 1] Schema violation - invalid asset...")
    s = SignalAgent()
    s.keygen()
    s.register()
    try:
        signal = s.generate_signal("buy", "FAKE_COIN", 0.99, channel="signal:btc")
        print("❌ FAILED - should have been blocked")
        return False
    except ValueError as e:
        print(f"✅ BLOCKED - {e}")
        return True

def test_invalid_action():
    print("\n[ATTACK 2] Schema violation - invalid action...")
    s = SignalAgent()
    try:
        signal = s.generate_signal("exfiltrate", "BTC", 0.99, channel="signal:btc")
        print("❌ FAILED - should have been blocked")
        return False
    except ValueError as e:
        print(f"✅ BLOCKED - {e}")
        return True

def test_order_exceeds_limit():
    print("\n[ATTACK 3] Order exceeds maximum amount...")
    o = OrderRouter()
    o.keygen()
    o.register()
    try:
        order = o.route("sig-001", "risk-001", "buy", "BTC", 999999, channel="order:btc")
        print("❌ FAILED - should have been blocked")
        return False
    except ValueError as e:
        print(f"✅ BLOCKED - {e}")
        return True

def test_risk_invalid_level():
    print("\n[ATTACK 4] Invalid risk level...")
    r = RiskGuard()
    r.keygen()
    r.register()
    try:
        risk = r.evaluate("sig-001", "apocalyptic", True, channel="risk:btc")
        print("❌ FAILED - should have been blocked")
        return False
    except ValueError as e:
        print(f"✅ BLOCKED - {e}")
        return True

if __name__ == "__main__":
    print("=== RealAgentID Fintech Attack Simulation ===")
    results = [
        test_schema_violation(),
        test_invalid_action(),
        test_order_exceeds_limit(),
        test_risk_invalid_level()
    ]
    print(f"\n{'='*45}")
    if all(results):
        print("✅ All attacks blocked - RealAgentID held the line")
    else:
        print("❌ Some attacks got through")
        sys.exit(1)
