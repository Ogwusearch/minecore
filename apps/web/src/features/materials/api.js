const BASE = '/api/materials'

async function request(url, options = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status} ${res.statusText}: ${text}`)
  }
  if (res.status === 204) return null
  return res.json()
}

function orgHeaders() {
  // Phase 02 will replace this with real auth.
  const orgId = localStorage.getItem('minecore.organizationId')
  return orgId ? { 'X-Organization-Id': orgId } : {}
}

export const api = {
  list: () => request(BASE, { headers: orgHeaders() }),
  get: (id) => request(`${BASE}/${id}`, { headers: orgHeaders() }),
  create: (data) =>
    request(BASE, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: orgHeaders(),
    }),
  update: (id, data) =>
    request(`${BASE}/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
      headers: orgHeaders(),
    }),
  remove: (id) =>
    request(`${BASE}/${id}`, { method: 'DELETE', headers: orgHeaders() }),
}
