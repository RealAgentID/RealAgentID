import subprocess
import json
import os
import sys

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def test_full_run(agent_name="test_agent", role="worker", message="Hello from RealAgentID"):
    print(f"\n[1] Generating identity for {agent_name}...")
    run(f"python3 cli/main.py keygen --name {agent_name}")

    print(f"[2] Registering {agent_name} as {role}...")
    run(f"python3 cli/main.py register --agent-id {agent_name} --pubkey ./keys/{agent_name}_public.pem --role {role}")

    print(f"[3] Signing message...")
    run(f"python3 cli/main.py sign --agent-id {agent_name} --message '{message}' --privkey ./keys/{agent_name}_private.pem --channel tasks:default 2>/dev/null > /tmp/test_signed.json")

    os.system("grep '^{' /tmp/test_signed.json > /tmp/test_clean.json")

    print(f"[4] Verifying signature...")
    out, _ = run(f"python3 cli/main.py verify --signed-json \"$(cat /tmp/test_clean.json)\" --pubkey ./keys/{agent_name}_public.pem")
    print(out)

    if "Valid" in out:
        print("\n✅ RealAgentID full run PASSED")
    else:
        print("\n❌ FAILED")
        sys.exit(1)

if __name__ == "__main__":
    test_full_run()
