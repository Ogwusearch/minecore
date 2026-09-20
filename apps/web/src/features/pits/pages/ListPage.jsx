import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function PitsListPage() {
  const [items, setItems] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    api.list().then(setItems).catch((e) => setError(e.message))
  }, [])

  if (error) return <p style={{ color: 'tomato' }}>Error: {error}</p>

  return (
    <section>
      <h2>Pits</h2>
      <ul>
        {items.map((p) => (
          <li key={p.id}>
            <strong>{p.code}</strong> — {p.name} ({p.status})
          </li>
        ))}
      </ul>
      {items.length === 0 && <p>No pits yet.</p>}
    </section>
  )
}
