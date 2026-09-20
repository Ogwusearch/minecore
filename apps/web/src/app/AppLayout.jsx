import { NavLink } from 'react-router-dom'

const navLinkStyle = ({ isActive }) => ({
  color: isActive ? '#e5e7eb' : '#94a3b8',
  textDecoration: 'none',
  marginRight: 16,
  fontWeight: isActive ? 600 : 400,
})

export default function AppLayout({ children }) {
  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>MineCore</h1>
        <nav>
          <NavLink to="/" style={navLinkStyle} end>
            Home
          </NavLink>
          <NavLink to="/organization" style={navLinkStyle}>
            Organization
          </NavLink>
          <NavLink to="/mine-sites" style={navLinkStyle}>
            Mine Sites
          </NavLink>
          <NavLink to="/employees" style={navLinkStyle}>
            Employees
          </NavLink>
        </nav>
      </header>
      <main className="app-main">{children}</main>
    </div>
  )
}
