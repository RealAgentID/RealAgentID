import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters.fintech import SignalAgent, RiskGuard, OrderRouter, ComplianceLog

def test_fintech_pipeline():
    print("\n[1] Initializing agents...")
    s = SignalAgent()
    s.keygen()
    s.register()

    r = RiskGuard()
    r.keygen()
    r.register()

    o = OrderRouter()
    o.keygen()
    o.register()

    c = ComplianceLog()
    c.keygen()
    c.register()

    print("[2] Running pipeline...")
    signal = s.generate_signal("buy", "BTC", 0.85, channel="signal:btc")
    risk = r.evaluate("sig-001", "medium", True, channel="risk:btc")
    order = o.route("sig-001", "risk-001", "buy", "BTC", 5000, channel="order:btc")
    log = c.record("trade_complete", {"signal": "sig-001", "status": "executed"})

    if signal and risk and order and log:
        print("\n✅ Fintech adapter test PASSED")
    else:
        print("\n❌ FAILED")
        sys.exit(1)

if __name__ == "__main__":
    test_fintech_pipeline()
