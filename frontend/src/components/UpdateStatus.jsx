// File: frontend/src/components/UpdateStatus.jsx
import { useState } from 'react';

export default function UpdateStatus({ sessionId }) {
  const [newStatus, setNewStatus] = useState('approved');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpdate = async () => {
    if (!sessionId) {
      setResult({ error: 'Missing session ID' });
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:5000/kyc/update/${sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });

      const data = await res.json();
      setResult(res.ok ? data : { error: data.error || 'Update failed' });
    } catch (err) {
      setResult({ error: err.message });
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Simulate Admin Action</h2>
      <p>Session ID: <strong>{sessionId || 'N/A'}</strong></p>
      <select value={newStatus} onChange={(e) => setNewStatus(e.target.value)}>
        <option value="approved">✅ Approve</option>
        <option value="rejected">❌ Reject</option>
      </select>
      <button onClick={handleUpdate} disabled={!sessionId}>
        Update Status
      </button>

      {loading ? (
        <p>Updating...</p>
      ) : result ? (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      ) : null}
    </div>
  );
}
