// Muestra la sinopsis como texto plano (nunca como HTML) para evitar XSS.
// Se eliminan las etiquetas HTML de terceros para que se vea limpio en pantalla.
export default function Synopsis({ text }) {
  const cleanText = text.replace(/<[^>]*>/g, "").replace(/\s+/g, " ").trim();

  return <p className="synopsis">{cleanText}</p>;
}
