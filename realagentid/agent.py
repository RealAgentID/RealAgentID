import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.keygen import generate_agent_identity
from core.registry import register_agent_from_key
from core.signing import sign_message, verify_message
from core.audit import read_log

class Agent:
    def __init__(self, name: str, role: str = "worker", keys_dir: str = "./keys"):
        self.name = name
        self.role = role
        self.keys_dir = keys_dir
        self.private_key = f"{keys_dir}/{name}_private.pem"
        self.public_key = f"{keys_dir}/{name}_public.pem"

    def keygen(self):
        return generate_agent_identity(self.name, self.keys_dir)

    def register(self):
        return register_agent_from_key(self.name, self.public_key, self.role)

    def sign(self, payload: dict, channel: str = "default"):
        return sign_message(self.name, self.private_key, channel, payload)

    def verify(self, signed_json: str):
        return verify_message(signed_json, self.public_key)

    def audit(self):
        return read_log()
