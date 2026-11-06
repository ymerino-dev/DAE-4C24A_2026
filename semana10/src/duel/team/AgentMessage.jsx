// Semana 9 (completado en la semana 10) — Task 8
// Props: author (string), text (string producido por un agente de IA).
// Devuelve <p><strong>{author}:</strong> <span>{text}</span></p>.
// El texto del agente siempre se muestra como texto, nunca como HTML.
export default function AgentMessage({ author, text }) {
  return (
    <p className="agent-message">
      <strong>{author}:</strong> <span>{text}</span>
    </p>
  );
}
