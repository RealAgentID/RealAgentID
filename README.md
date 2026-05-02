# RealAgentID

![RealAgentID]()

Cryptographic identity verification for AI agents. Prevents spoofing, replay attacks, and unauthorized commands before they reach your infrastructure.

## What It Does

- Generates Ed25519 keypairs per agent
- Signs and verifies messages cryptographically
- Blocks replay attacks via Redis TTL nonces
- Detects payload tampering
- Logs all events to a tamper-evident audit trail

## Quick Start

```bash
git clone https://github.com/RealAgentID/RealAgentID.git
cd RealAgentID
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 tests/test_full_run.py

## Requirements

- Python 3.12+
- Redis

## Setup Redis

**Ubuntu/Debian**
'''bash
sudo apt install redis-server -y
sudo service redis start
redis cli-ping

- Should return PONG
