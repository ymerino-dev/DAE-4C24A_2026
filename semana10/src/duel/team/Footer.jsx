export default function Footer({ contact }) {
  return (
    <footer id="contacto">
      <p>{contact.address}</p>
      <p><a href={`tel:${contact.phone}`}>{contact.phone}</a></p>
      <p><a href={`mailto:${contact.email}`}>{contact.email}</a></p>
      <small>© {new Date().getFullYear()} Cine Tecsup. Cartelera sujeta a cambios.</small>
    </footer>
  );
}
