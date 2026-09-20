import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api.js'
import StatusBadge from '../components/StatusBadge.jsx'

export default function MiningOperationDetailPage() {
  const { id } = useParams()
  const [op, setOp] = useState(null)
  const [audit, setAudit] = useState([])
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  const refresh = async () => {
    try {
      setOp(await api.get(id))
      setAudit(await api.audit(id))
    } catch (e) {
      setError(e.message)
    }
  }

  useEffect(() => {
    refresh()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  const run = async (fn) => {
    setBusy(true)
    try {
      await fn()
      await refresh()
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy(false)
    }
  }

  if (error) return <p style={{ color: 'tomato' }}>Error: {error}</p>
  if (!op) return <p>Loading…</p>

  return (
    <section>
      <h2>
        {op.operation_number} <StatusBadge status={op.status} />
      </h2>

      <dl style={{ display: 'grid', gridTemplateColumns: '180px 1fr', gap: '0.5rem' }}>
        <dt>Date</dt><dd>{op.operation_date}</dd>
        <dt>Quantity</dt><dd>{op.quantity}</dd>
        <dt>Status</dt><dd>{op.status}</dd>
        {op.cancellation_reason && (<>
          <dt>Cancellation reason</dt><dd>{op.cancellation_reason}</dd>
        </>)}
      </dl>

      <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
        {op.status === 'draft' && (
          <button disabled={busy} onClick={() => run(() => api.record(id))}>
            Record
          </button>
        )}
        {op.status === 'recorded' && (
          <button disabled={busy} onClick={() => run(() => api.approve(id))}>
            Approve
          </button>
        )}
        {(op.status === 'draft' || op.status === 'recorded') && (
          <button
            disabled={busy}
            onClick={() => {
              const reason = window.prompt('Cancellation reason?')
              if (reason) run(() => api.cancel(id, reason))
            }}
          >
            Cancel
          </button>
        )}
      </div>

      <h3 style={{ marginTop: '2rem' }}>Audit trail</h3>
      <ul>
        {audit.map((a) => (
          <li key={a.id}>
            <code>{a.created_at}</code> — <strong>{a.action}</strong>
            {a.from_status && a.to_status && (
              <> ({a.from_status} → {a.to_status})</>
            )}
            {a.changes && (
              <pre style={{ fontSize: '0.75rem' }}>
                {JSON.stringify(a.changes, null, 2)}
              </pre>
            )}
          </li>
        ))}
      </ul>
    </section>
  )
}
