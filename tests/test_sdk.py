import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from realagentid import Agent

def test_sdk():
    print("\n[1] Creating agent...")
    a = Agent("sdk_test_agent", role="worker")

    print("[2] Generating keypair...")
    a.keygen()

    print("[3] Registering agent...")
    a.register()

    print("[4] Signing payload...")
    signed = a.sign({"action": "buy", "asset": "BTC", "amount": 0.5}, channel="signal:btc")

    print("[5] Verifying signature...")
    result = a.verify(signed)

    if result and result.get("agent_id") == "sdk_test_agent":
        print("\n✅ RealAgentID SDK test PASSED")
    else:
        print("\n❌ FAILED")
        sys.exit(1)

if __name__ == "__main__":
    test_sdk()
