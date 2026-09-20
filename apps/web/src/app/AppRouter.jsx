import { Routes, Route, Link } from 'react-router-dom'

import OrganizationPage from '../features/organization/pages/OrganizationPage.jsx'
import MineSitesPage from '../features/mine-sites/pages/MineSitesPage.jsx'
import MineSiteDetailsPage from '../features/mine-sites/pages/MineSiteDetailsPage.jsx'
import EmployeesPage from '../features/employees/pages/EmployeesPage.jsx'

function Home() {
  return (
    <section>
      <h2>MineCore</h2>
      <p>Phase 03 — Organizations &amp; Mine Sites.</p>
      <ul>
        <li>
          <Link to="/organization">Organization profile</Link>
        </li>
        <li>
          <Link to="/mine-sites">Mine sites</Link>
        </li>
        <li>
          <Link to="/employees">Employees</Link>
        </li>
      </ul>
    </section>
  )
}

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/organization" element={<OrganizationPage />} />
      <Route path="/mine-sites" element={<MineSitesPage />} />
      <Route path="/mine-sites/:id" element={<MineSiteDetailsPage />} />
      <Route path="/employees" element={<EmployeesPage />} />
    </Routes>
  )
}
