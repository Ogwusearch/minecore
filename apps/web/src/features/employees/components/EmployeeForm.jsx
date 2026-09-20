import { useState } from 'react'

export default function EmployeeForm({ initial, onSubmit, onCancel }) {
  const [employeeNumber, setEmployeeNumber] = useState(initial?.employee_number || '')
  const [fullName, setFullName] = useState(initial?.full_name || '')
  const [jobTitle, setJobTitle] = useState(initial?.job_title || '')
  const [department, setDepartment] = useState(initial?.department || '')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(event) {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      const payload = {
        full_name: fullName,
        job_title: jobTitle || null,
        department: department || null,
      }
      if (!initial) payload.employee_number = employeeNumber
      await onSubmit(payload)
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
            Employee number
            <input
              value={employeeNumber}
              onChange={(e) => setEmployeeNumber(e.target.value)}
              required
              style={{ marginLeft: 8 }}
            />
          </label>
        </div>
      )}
      <div style={{ marginBottom: 8 }}>
        <label>
          Full name
          <input
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
            style={{ marginLeft: 8 }}
          />
        </label>
      </div>
      <div style={{ marginBottom: 8 }}>
        <label>
          Job title
          <input
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            style={{ marginLeft: 8 }}
          />
        </label>
      </div>
      <div style={{ marginBottom: 8 }}>
        <label>
          Department
          <input
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
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
