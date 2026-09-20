import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function MaterialsListPage() {
  const [items, setItems] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    api.list().then(setItems).catch((e) => setError(e.message))
  }, [])

  if (error) return <p style={{ color: 'tomato' }}>Error: {error}</p>

  return (
    <section>
      <h2>Materials</h2>
      <ul>
        {items.map((m) => (
          <li key={m.id}>
            <strong>{m.code}</strong> — {m.name} ({m.status})
          </li>
        ))}
      </ul>
      {items.length === 0 && <p>No materials yet.</p>}
    </section>
  )
}
