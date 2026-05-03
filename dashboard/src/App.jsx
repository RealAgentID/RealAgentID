import { useState, useEffect } from "react"

function AgentCard({ agent }) {
  const ttl = agent.ttl || 0
  const status = ttl > 3600 ? "green" : ttl > 600 ? "yellow" : "red"
  return (
    <div style={{
      background: "#1a1a1a",
      border: `1px solid ${status === "green" ? "#00ff88" : status === "yellow" ? "#ffaa00" : "#ff4444"}`,
      borderRadius: 8,
      padding: 16,
      marginBottom: 12
    }}>
      <div style={{ color: "#fff", fontWeight: "bold", fontSize: 16 }}>{agent.agent_id}</div>
      <div style={{ color: "#888", fontSize: 13 }}>Role: {agent.role}</div>
      <div style={{ color: "#888", fontSize: 13 }}>TTL: {ttl}s</div>
      <div style={{ color: "#888", fontSize: 13, wordBreak: "break-all" }}>Key: {agent.pub_key}</div>
    </div>
  )
}

function AuditEntry({ entry }) {
  const color = entry.result === "VALID" ? "#00ff88" : "#ff4444"
  return (
    <div style={{
      background: "#111",
      borderLeft: `3px solid ${color}`,
      padding: "8px 12px",
      marginBottom: 8,
      fontSize: 12,
      color: "#ccc"
    }}>
      <span style={{ color }}>[{entry.result}]</span> {entry.event} — {entry.agent_id} — {entry.channel}
      {entry.reason && <span style={{ color: "#ff8888" }}> ({entry.reason})</span>}
    </div>
  )
}

export default function App() {
  const [agents, setAgents] = useState([])
  const [audit, setAudit] = useState([])

  const fetchData = () => {
    fetch("http://localhost:5050/api/agents")
      .then(r => r.json())
      .then(setAgents)
      .catch(() => {})
    fetch("http://localhost:5050/api/audit")
      .then(r => r.json())
      .then(setAudit)
      .catch(() => {})
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ background: "#0a0a0a", minHeight: "100vh", padding: 24, fontFamily: "monospace" }}>
      <div style={{ display: "flex", alignItems: "center", marginBottom: 32 }}>
        <div>
          <h1 style={{ color: "#ff4400", margin: 0, fontSize: 28 }}>RealAgentID</h1>
          <div style={{ color: "#666", fontSize: 13 }}>Control Center</div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
        <div>
          <h2 style={{ color: "#fff", fontSize: 16, marginBottom: 16 }}>
            Live Agent Registry <span style={{ color: "#666" }}>({agents.length})</span>
          </h2>
          {agents.length === 0
            ? <div style={{ color: "#444" }}>No agents registered</div>
            : agents.map((a, i) => <AgentCard key={i} agent={a} />)
          }
        </div>

        <div>
          <h2 style={{ color: "#fff", fontSize: 16, marginBottom: 16 }}>
            Audit Log <span style={{ color: "#666" }}>({audit.length})</span>
          </h2>
          <div style={{ maxHeight: 600, overflowY: "auto" }}>
            {audit.length === 0
              ? <div style={{ color: "#444" }}>No audit entries</div>
              : audit.map((e, i) => <AuditEntry key={i} entry={e} />)
            }
          </div>
        </div>
      </div>
    </div>
  )
}
