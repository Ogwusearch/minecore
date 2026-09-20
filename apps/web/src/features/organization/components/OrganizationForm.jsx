import { useState } from 'react'

export default function OrganizationForm({ organization, onSubmit }) {
  const [name, setName] = useState(organization.name)
  const [status, setStatus] = useState(organization.status)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(event) {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await onSubmit({ name, status })
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div style={{ marginBottom: 12 }}>
        <label>
          Name
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            style={{ marginLeft: 8 }}
          />
        </label>
      </div>
      <div style={{ marginBottom: 12 }}>
        <label>
          Status
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            style={{ marginLeft: 8 }}
          >
            <option value="active">active</option>
            <option value="inactive">inactive</option>
            <option value="suspended">suspended</option>
          </select>
        </label>
      </div>
      {error && <p style={{ color: '#f87171' }}>{error}</p>}
      <button type="submit" disabled={busy}>
        {busy ? 'Saving…' : 'Save'}
      </button>
    </form>
  )
}
