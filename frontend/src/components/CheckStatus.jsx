// File: frontend/src/components/CheckStatus.jsx
import { useEffect, useState } from 'react';

export default function CheckStatus({ sessionId }) {
  const [statusResult, setStatusResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!sessionId) return;

    const fetchStatus = async () => {
      setLoading(true);
      try {
        const res = await fetch(`http://127.0.0.1:5000/kyc/status/${sessionId}`);
        const data = await res.json();
        if (res.ok) {
          setStatusResult(data);
        } else {
          setStatusResult({ error: data.error || 'Unknown error' });
        }
      } catch (err) {
        setStatusResult({ error: err.message });
      }
      setLoading(false);
    };

    fetchStatus();
  }, [sessionId]);

  return (
    <div className="card">
      <h2>Check KYC Status</h2>
      <input
        type="text"
        placeholder="Session ID"
        value={sessionId}
        readOnly
      />
      {loading ? (
        <p>Checking...</p>
      ) : statusResult ? (
        <pre>{JSON.stringify(statusResult, null, 2)}</pre>
      ) : (
        <p>Start a KYC session to check status.</p>
      )}
    </div>
  );
}
