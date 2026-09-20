import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api.js'
import StatusBadge from '../components/StatusBadge.jsx'

export default function MiningOperationsListPage() {
  const [items, setItems] = useState([])
  const [statusFilter, setStatusFilter] = useState('')
  const [error, setError] = useState(null)

  useEffect(() => {
    api
      .list(statusFilter ? { status: statusFilter } : {})
      .then(setItems)
      .catch((e) => setError(e.message))
  }, [statusFilter])

  if (error) return <p style={{ color: 'tomato' }}>Error: {error}</p>

  return (
    <section>
      <h2>Mining Operations</h2>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Status:{' '}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">All</option>
            <option value="draft">Draft</option>
            <option value="recorded">Recorded</option>
            <option value="approved">Approved</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </label>
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #334155' }}>
            <th align="left">Number</th>
            <th align="left">Date</th>
            <th align="right">Quantity</th>
            <th align="left">Status</th>
          </tr>
        </thead>
        <tbody>
          {items.map((op) => (
            <tr key={op.id} style={{ borderBottom: '1px solid #1e293b' }}>
              <td>
                <Link to={`/mining/${op.id}`}>{op.operation_number}</Link>
              </td>
              <td>{op.operation_date}</td>
              <td align="right">{op.quantity}</td>
              <td>
                <StatusBadge status={op.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {items.length === 0 && <p>No mining operations yet.</p>}
    </section>
  )
}
