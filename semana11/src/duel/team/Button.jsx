// Semana 10 — Botón reutilizable.
// Recibe su contenido por children y su aspecto por la prop variant.
export default function Button({ children, variant = "primary", onClick, type = "button", className, disabled = false }) {
  const variants = {
    primary: "button--primary",
    secondary: "button--secondary",
    outline: "button--outline",
    ghost: "button--ghost",
    danger: "button--danger",
  };

  const classes = ["button", variants[variant], className].filter(Boolean).join(" ");

  return (
    <button className={classes} onClick={onClick} type={type} disabled={disabled}>
      {children}
    </button>
  );
}
