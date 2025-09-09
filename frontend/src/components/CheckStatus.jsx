import { useEffect, useState } from "react";
import { api } from "../lib/api";
import Alert from "./Alert";

export default function CheckStatus({ sessionId }) {
  const [status, setStatus] = useState(null);
  const [msg, setMsg] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setStatus(null);
    setMsg(null);
    if (!sessionId) {
      setMsg({ type: "info", text: "No session yet. Start KYC to check status." });
      return;
    }
    let cancelled = false;
    (async () => {
      setLoading(true);
      try {
        const data = await api.getStatus(sessionId);
        if (!cancelled) setStatus(data);
      } catch (err) {
        if (!cancelled) {
          setMsg({ type: "error", text: `${err.message} (code: ${err.code || "unknown"})` });
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [sessionId]);

  return (
    <div className="card">
      <h2>Check KYC Status</h2>
      <input type="text" value={sessionId || ""} readOnly />
      {loading && <Alert type="info">Checking…</Alert>}
      {status && <Alert type="success">{JSON.stringify(status, null, 2)}</Alert>}
      {!loading && !status && msg && <Alert type={msg.type}>{msg.text}</Alert>}
    </div>
  );
}
