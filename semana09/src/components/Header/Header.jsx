import './Header.css'

const navigationItems = [
  { label: 'Home', href: '#home' },
  { label: 'Movies', href: '#movies' },
  { label: 'Showtimes', href: '#showtimes' },
  { label: 'Contact', href: '#contact' },
]

function Header() {
  return (
    <header className="header">
      <div className="header__inner">
        <a className="header__brand" href="#home">
          <span className="header__brand-mark" aria-hidden="true">
            ★
          </span>
          <span>Cinema Luna</span>
        </a>

        <nav className="header__nav" aria-label="Main navigation">
          <ul className="header__nav-list">
            {navigationItems.map((item) => (
              <li key={item.href}>
                <a className="header__nav-link" href={item.href}>
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  )
}

export default Header
