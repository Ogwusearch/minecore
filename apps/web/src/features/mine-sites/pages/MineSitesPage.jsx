import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listMineSites, createMineSite, deleteMineSite } from '../api.js'
import MineSiteForm from '../components/MineSiteForm.jsx'

export default function MineSitesPage() {
  const [sites, setSites] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)

  async function refresh() {
    setLoading(true)
    try {
      setSites(await listMineSites())
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  async function handleCreate(payload) {
    await createMineSite(payload)
    setShowForm(false)
    await refresh()
  }

  async function handleDelete(id) {
    if (!confirm('Delete this mine site?')) return
    await deleteMineSite(id)
    await refresh()
  }

  return (
    <section>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Mine Sites</h2>
        <button onClick={() => setShowForm((v) => !v)}>
          {showForm ? 'Close' : 'New site'}
        </button>
      </div>

      {showForm && (
        <MineSiteForm onSubmit={handleCreate} onCancel={() => setShowForm(false)} />
      )}

      {loading && <p>Loading…</p>}
      {error && <p style={{ color: '#f87171' }}>{error}</p>}

      {!loading && !error && sites.length === 0 && <p>No mine sites yet.</p>}

      {sites.length > 0 && (
        <table style={{ width: '100%', marginTop: 16, borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ textAlign: 'left' }}>Code</th>
              <th style={{ textAlign: 'left' }}>Name</th>
              <th style={{ textAlign: 'left' }}>Status</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {sites.map((site) => (
              <tr key={site.id}>
                <td>{site.code}</td>
                <td>
                  <Link to={`/mine-sites/${site.id}`}>{site.name}</Link>
                </td>
                <td>{site.status}</td>
                <td style={{ textAlign: 'right' }}>
                  <button onClick={() => handleDelete(site.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}
