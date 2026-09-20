import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  getMineSite,
  updateMineSite,
  listSiteAssignments,
  assignUserToSite,
  unassignUserFromSite,
} from '../api.js'
import MineSiteForm from '../components/MineSiteForm.jsx'

export default function MineSiteDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [site, setSite] = useState(null)
  const [assignments, setAssignments] = useState([])
  const [userId, setUserId] = useState('')
  const [error, setError] = useState(null)

  async function refresh() {
    try {
      const [siteData, assignmentData] = await Promise.all([
        getMineSite(id),
        listSiteAssignments(id),
      ])
      setSite(siteData)
      setAssignments(assignmentData)
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => {
    refresh()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  async function handleUpdate(payload) {
    const updated = await updateMineSite(id, payload)
    setSite(updated)
  }

  async function handleAssign(event) {
    event.preventDefault()
    if (!userId) return
    try {
      await assignUserToSite(id, userId)
      setUserId('')
      await refresh()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleUnassign(uid) {
    await unassignUserFromSite(id, uid)
    await refresh()
  }

  if (error) return <p style={{ color: '#f87171' }}>{error}</p>
  if (!site) return <p>Loading…</p>

  return (
    <section>
      <button onClick={() => navigate('/mine-sites')}>← Back</button>
      <h2>{site.name}</h2>
      <p>
        <strong>Code:</strong> {site.code} · <strong>Status:</strong> {site.status}
      </p>
      <p>
        <strong>Location:</strong> {site.location || '—'}
      </p>

      <h3>Edit</h3>
      <MineSiteForm initial={site} onSubmit={handleUpdate} />

      <h3 style={{ marginTop: 32 }}>Assigned users</h3>
      <form onSubmit={handleAssign} style={{ marginBottom: 12 }}>
        <input
          placeholder="user UUID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          style={{ marginRight: 8 }}
        />
        <button type="submit">Assign</button>
      </form>

      {assignments.length === 0 ? (
        <p>No users assigned.</p>
      ) : (
        <ul>
          {assignments.map((a) => (
            <li key={a.id}>
              {a.user_id}{' '}
              <button onClick={() => handleUnassign(a.user_id)}>Unassign</button>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
