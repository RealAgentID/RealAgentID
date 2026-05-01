import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'realagentid.db')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event TEXT NOT NULL,
            agent_id TEXT NOT NULL,
            channel TEXT,
            result TEXT NOT NULL,
            message_id TEXT,
            reason TEXT,
            latency_ms REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("[RealAgentID DB] audit_log table ready.")

def insert_event(timestamp, event, agent_id, channel, result, message_id=None, reason=None, latency_ms=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_log (timestamp, event, agent_id, channel, result, message_id, reason, latency_ms)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, event, agent_id, channel, result, message_id, reason, latency_ms))
    conn.commit()
    conn.close()

def query_events(agent_id=None, event=None, result=None, limit=100):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM audit_log WHERE 1=1"
    params = []
    if agent_id:
        query += " AND agent_id = ?"
        params.append(agent_id)
    if event:
        query += " AND event = ?"
        params.append(event)
    if result:
        query += " AND result = ?"
        params.append(result)
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
