import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
from core.keygen import generate_agent_identity
from core.registry import register_agent_from_key, list_agents, get_role, revoke_agent
from core.signing import sign_message, verify_message
from core.audit import write_log, read_log

def main():
    parser = argparse.ArgumentParser(prog="realagentid", description="RealAgentID CLI")
    sub = parser.add_subparsers(dest="command")

    kg = sub.add_parser("keygen", help="Generate agent keypair")
    kg.add_argument("--name", required=True)
    kg.add_argument("--keys-dir", default="./keys")

    rg = sub.add_parser("register", help="Register agent")
    rg.add_argument("--agent-id", required=True)
    rg.add_argument("--pubkey", required=True)
    rg.add_argument("--role", default="worker")

    sub.add_parser("list", help="List all agents")

    sg = sub.add_parser("sign", help="Sign a message")
    sg.add_argument("--agent-id", required=True)
    sg.add_argument("--message", required=True)
    sg.add_argument("--privkey", required=True)
    sg.add_argument("--channel", default="default")

    vf = sub.add_parser("verify", help="Verify a signed message")
    vf.add_argument("--signed-json", required=True)
    vf.add_argument("--pubkey", required=True)

    rv = sub.add_parser("revoke", help="Revoke an agent")
    rv.add_argument("--agent-id", required=True)

    sub.add_parser("audit", help="Read audit log")

    args = parser.parse_args()

    if args.command == "keygen":
        result = generate_agent_identity(args.name, args.keys_dir)
        print(f"[+] Identity created: {result}")
    elif args.command == "register":
        register_agent_from_key(args.agent_id, args.pubkey, args.role)
        print(f"[+] Registered {args.agent_id} as {args.role}")
    elif args.command == "list":
        agents = list_agents()
        for a in (agents or []):
            print(a)
    elif args.command == "sign":
        signed = sign_message(args.agent_id, args.message, args.privkey, args.channel)
        print(signed)
    elif args.command == "verify":
        result = verify_message(args.signed_json, args.pubkey)
        print(f"[+] Valid: {result}")
    elif args.command == "revoke":
        revoke_agent(args.agent_id)
        print(f"[+] Revoked {args.agent_id}")
    elif args.command == "audit":
        logs = read_log()
        for entry in logs:
            print(entry)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
