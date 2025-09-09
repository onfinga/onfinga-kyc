// Simple fetch wrapper with consistent error handling
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    // best effort: non-JSON response
    data = { error: "Non-JSON response from server" };
  }

  if (!res.ok) {
    const message = data?.error || `Request failed (${res.status})`;
    const code = data?.code || "unknown_error";
    const err = new Error(message);
    err.code = code;
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

export const api = {
  startKYC: (email) =>
    request("/kyc/start", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),
  getStatus: (sessionId) => request(`/kyc/status/${sessionId}`),
  updateStatus: (sessionId, status) =>
    request(`/kyc/update/${sessionId}`, {
      method: "POST",
      body: JSON.stringify({ status }),
    }),
  listByEmail: (email) => request(`/kyc/list?email=${encodeURIComponent(email)}`),
};

export { BASE_URL };
