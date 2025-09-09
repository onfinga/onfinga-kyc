export default function Alert({ type = "info", children }) {
  const bg =
    type === "error" ? "#ffe6e6" :
    type === "success" ? "#e6ffef" :
    "#eef2ff";
  const border =
    type === "error" ? "#ff8080" :
    type === "success" ? "#7bd389" :
    "#91a4ff";
  const color =
    type === "error" ? "#6b0000" :
    type === "success" ? "#0a4e1a" :
    "#1a2a6b";

  return (
    <div style={{
      background: bg,
      border: `1px solid ${border}`,
      color,
      padding: "10px 12px",
      borderRadius: 6,
      marginTop: 10,
      whiteSpace: "pre-wrap",
      wordBreak: "break-word",
      textAlign: "left"
    }}>
      {children}
    </div>
  );
}
