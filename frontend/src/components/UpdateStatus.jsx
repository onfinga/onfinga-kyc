import { useState } from "react";
import { api } from "../lib/api";
import Alert from "./Alert";

export default function UpdateStatus({ sessionId }) {
  const [status, setStatus] = useState("approved");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState(null);

  const handleUpdate = async () => {
    setMsg(null);
    if (!sessionId) {
      setMsg({ type: "error", text: "No session selected. Start KYC first." });
      return;
    }
    setLoading(true);
    try {
      const data = await api.updateStatus(sessionId, status);
      setMsg({ type: "success", text: `Updated: ${JSON.stringify(data)}` });
    } catch (err) {
      setMsg({ type: "error", text: `${err.message} (code: ${err.code || "unknown"})` });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Update Status (Test/Admin)</h2>
      <div style={{ display: "flex", gap: 8 }}>
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          disabled={loading}
        >
          <option value="approved">Approve</option>
          <option value="rejected">Reject</option>
        </select>
        <button onClick={handleUpdate} disabled={loading || !sessionId}>
          {loading ? "Updating…" : "Update"}
        </button>
      </div>
      {msg && <Alert type={msg.type}>{msg.text}</Alert>}
    </div>
  );
}
