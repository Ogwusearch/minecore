import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function DepositsListPage() {
  const [items, setItems] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    api.list().then(setItems).catch((e) => setError(e.message))
  }, [])

  if (error) return <p style={{ color: 'tomato' }}>Error: {error}</p>

  return (
    <section>
      <h2>Deposits</h2>
      <ul>
        {items.map((d) => (
          <li key={d.id}>
            <strong>{d.code}</strong> — {d.name} ({d.status})
          </li>
        ))}
      </ul>
      {items.length === 0 && <p>No deposits yet.</p>}
    </section>
  )
}
