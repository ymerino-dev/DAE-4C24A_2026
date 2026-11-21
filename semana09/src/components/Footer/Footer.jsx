import './Footer.css'

const currentYear = new Date().getFullYear()

function Footer() {
  return (
    <footer className="footer" id="contact">
      <div className="footer__inner">
        <div className="footer__section">
          <h2 className="footer__heading">Cinema Luna</h2>
          <p>128 Sunset Boulevard</p>
          <p>Los Angeles, CA 90028</p>
        </div>

        <div className="footer__section">
          <h2 className="footer__heading">Contact</h2>
          <p>
            <a href="tel:+13105550142">+1 (310) 555-0142</a>
          </p>
          <p>
            <a href="mailto:hello@cinemaluna.example">hello@cinemaluna.example</a>
          </p>
        </div>

        <div className="footer__section">
          <h2 className="footer__heading">Hours</h2>
          <p>Monday - Thursday: 12:00 - 23:00</p>
          <p>Friday - Sunday: 11:00 - 01:00</p>
        </div>
      </div>

      <p className="footer__copyright">
        © {currentYear} Cinema Luna. All rights reserved.
      </p>
    </footer>
  )
}

export default Footer
