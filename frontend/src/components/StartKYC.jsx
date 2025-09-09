import { useState } from "react";
import { api } from "../lib/api";
import Alert from "./Alert";

export default function StartKYC({ onSessionCreated }) {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState(null); // {type: 'error'|'success'|'info', text: string}

  const handleStart = async () => {
    setMsg(null);
    if (!email.trim()) {
      setMsg({ type: "error", text: "Please enter your email address." });
      return;
    }
    setLoading(true);
    try {
      const data = await api.startKYC(email.trim());
      onSessionCreated?.(data.session_id);
      setMsg({
        type: "success",
        text: `Session created: ${data.session_id}\nStatus: ${data.status}`,
      });
    } catch (err) {
      setMsg({
        type: "error",
        text: `${err.message}${err.code ? ` (code: ${err.code})` : ""}`,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Start KYC</h2>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          type="email"
          placeholder="Enter email e.g. placeholder@onfinga.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ flex: 1 }}
          disabled={loading}
        />
        <button onClick={handleStart} disabled={loading}>
          {loading ? "Starting…" : "Start"}
        </button>
      </div>
      {msg && <Alert type={msg.type}>{msg.text}</Alert>}
    </div>
  );
}
