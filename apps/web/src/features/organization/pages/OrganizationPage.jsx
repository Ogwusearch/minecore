import { useEffect, useState } from 'react'
import { getCurrentOrganization, updateCurrentOrganization } from '../api.js'
import OrganizationForm from '../components/OrganizationForm.jsx'

export default function OrganizationPage() {
  const [organization, setOrganization] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    getCurrentOrganization()
      .then((data) => {
        if (!cancelled) setOrganization(data)
      })
      .catch((err) => {
        if (!cancelled) setError(err.message)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  async function handleSave(payload) {
    const updated = await updateCurrentOrganization(payload)
    setOrganization(updated)
  }

  if (loading) return <p>Loading…</p>
  if (error) return <p style={{ color: '#f87171' }}>{error}</p>
  if (!organization) return null

  return (
    <section>
      <h2>Organization</h2>
      <p>
        <strong>Code:</strong> {organization.code}
      </p>
      <p>
        <strong>ID:</strong> {organization.id}
      </p>
      <hr style={{ borderColor: '#1f2937', margin: '24px 0' }} />
      <OrganizationForm organization={organization} onSubmit={handleSave} />
    </section>
  )
}
