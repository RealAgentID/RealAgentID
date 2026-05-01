
## Redis Backend (v2)

RealAgentID now uses Redis as its registry backend, replacing the flat JSON file.

### What changed
- Agent identities stored in Redis with native TTL expiration (24 hours)
- Replay attacks blocked via Redis message ID tracking (5 minute window)
- Registry is persistent across restarts and distributable across nodes

### Requirements
- Redis server running locally (`sudo service redis-server start`)
- Python redis client (`pip install redis --break-system-packages`)

### How replay protection works
Every message carries a unique `message_id` (UUID4). On verification, the ID is checked against Redis. If it already exists, the message is rejected and the event is logged to the audit trail. First use passes. Second use is blocked — every time.
