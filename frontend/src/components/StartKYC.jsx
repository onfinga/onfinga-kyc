// File: frontend/src/components/StartKYC.jsx
import { useState } from 'react';

export default function StartKYC({ onSessionCreated }) {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const startKYC = async () => {
    try {
      const res = await fetch('http://localhost:5000/kyc/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })  // ✅ Now using email
      });

      const data = await res.json();
      if (res.ok) {
        setMessage(`✅ Session started: ${data.session_id}`);
        onSessionCreated(data.session_id);
      } else {
        setMessage(`❌ ${data.error || 'Something went wrong.'}`);
      }
    } catch (err) {
      setMessage('❌ Server error: ' + err.message);
    }
  };

  return (
    <div className="card">
      <h2>Start KYC Session</h2>
      <input
        type="email"
        placeholder="Enter user email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={startKYC}>Start KYC</button>
      <p>{message}</p>
    </div>
  );
}
