import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api.js'
import Form from '../components/Form.jsx'

export default function NewMiningOperationPage() {
  const navigate = useNavigate()
  const [error, setError] = useState(null)

  const onSubmit = async (data) => {
    try {
      const op = await api.create(data)
      navigate(`/mining/${op.id}`)
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <section>
      <h2>New Mining Operation</h2>
      {error && <p style={{ color: 'tomato' }}>Error: {error}</p>}
      <Form onSubmit={onSubmit} />
    </section>
  )
}
