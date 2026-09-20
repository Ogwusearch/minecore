import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function ShiftsListPage() {
  const [items, setItems] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    api.list().then(setItems).catch((e) => setError(e.message))
  }, [])

  if (error) return <p style={{ color: 'tomato' }}>Error: {error}</p>

  return (
    <section>
      <h2>Shifts</h2>
      <ul>
        {items.map((s) => (
          <li key={s.id}>
            <strong>{s.code}</strong> — {s.name} ({s.start_time}–{s.end_time})
          </li>
        ))}
      </ul>
      {items.length === 0 && <p>No shifts yet.</p>}
    </section>
  )
}
