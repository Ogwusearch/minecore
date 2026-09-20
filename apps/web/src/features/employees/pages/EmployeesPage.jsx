import { useEffect, useState } from 'react'
import {
  listEmployees,
  createEmployee,
  deleteEmployee,
} from '../api.js'
import EmployeeForm from '../components/EmployeeForm.jsx'

export default function EmployeesPage() {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)

  async function refresh() {
    setLoading(true)
    try {
      setEmployees(await listEmployees())
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
    await createEmployee(payload)
    setShowForm(false)
    await refresh()
  }

  async function handleDelete(id) {
    if (!confirm('Delete this employee?')) return
    await deleteEmployee(id)
    await refresh()
  }

  return (
    <section>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Employees</h2>
        <button onClick={() => setShowForm((v) => !v)}>
          {showForm ? 'Close' : 'New employee'}
        </button>
      </div>

      {showForm && (
        <EmployeeForm onSubmit={handleCreate} onCancel={() => setShowForm(false)} />
      )}

      {loading && <p>Loading…</p>}
      {error && <p style={{ color: '#f87171' }}>{error}</p>}

      {!loading && !error && employees.length === 0 && <p>No employees yet.</p>}

      {employees.length > 0 && (
        <table style={{ width: '100%', marginTop: 16, borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ textAlign: 'left' }}>Number</th>
              <th style={{ textAlign: 'left' }}>Name</th>
              <th style={{ textAlign: 'left' }}>Job title</th>
              <th style={{ textAlign: 'left' }}>Department</th>
              <th style={{ textAlign: 'left' }}>Status</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {employees.map((emp) => (
              <tr key={emp.id}>
                <td>{emp.employee_number}</td>
                <td>{emp.full_name}</td>
                <td>{emp.job_title || '—'}</td>
                <td>{emp.department || '—'}</td>
                <td>{emp.status}</td>
                <td style={{ textAlign: 'right' }}>
                  <button onClick={() => handleDelete(emp.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}
