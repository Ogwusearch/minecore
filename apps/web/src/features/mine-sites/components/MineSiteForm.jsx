import { useState } from 'react'

export default function MineSiteForm({ initial, onSubmit, onCancel }) {
  const [code, setCode] = useState(initial?.code || '')
  const [name, setName] = useState(initial?.name || '')
  const [status, setStatus] = useState(initial?.status || 'active')
  const [location, setLocation] = useState(initial?.location || '')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(event) {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await onSubmit({
        code,
        name,
        status,
        location: location || null,
      })
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: 12 }}>
      {!initial && (
        <div style={{ marginBottom: 8 }}>
          <label>
            Code
            <input
              value={code}
              onChange={(e) => setCode(e.target.value)}
              required
              style={{ marginLeft: 8 }}
            />
          </label>
        </div>
      )}
      <div style={{ marginBottom: 8 }}>
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
      <div style={{ marginBottom: 8 }}>
        <label>
          Status
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            style={{ marginLeft: 8 }}
          >
            <option value="active">active</option>
            <option value="inactive">inactive</option>
            <option value="closed">closed</option>
          </select>
        </label>
      </div>
      <div style={{ marginBottom: 8 }}>
        <label>
          Location
          <input
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            style={{ marginLeft: 8 }}
          />
        </label>
      </div>
      {error && <p style={{ color: '#f87171' }}>{error}</p>}
      <div style={{ display: 'flex', gap: 8 }}>
        <button type="submit" disabled={busy}>
          {busy ? 'Saving…' : 'Save'}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} disabled={busy}>
            Cancel
          </button>
        )}
      </div>
    </form>
  )
}
