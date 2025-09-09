import { useState } from "react";
import StartKYC from "./components/StartKYC";
import CheckStatus from "./components/CheckStatus";
import UpdateStatus from "./components/UpdateStatus";
import "./App.css";

export default function App() {
  const [sessionId, setSessionId] = useState("");

  return (
    <div className="app-container">
      <h1>Onfinga KYC</h1>
      <StartKYC onSessionCreated={setSessionId} />
      <hr />
      <CheckStatus sessionId={sessionId} />
      <UpdateStatus sessionId={sessionId} />
    </div>
  );
}
