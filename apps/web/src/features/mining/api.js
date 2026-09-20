const BASE = '/api/mining-operations'

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

function authHeaders() {
  // Phase 02 will replace this with a real session.
  const orgId = localStorage.getItem('minecore.organizationId')
  const userId = localStorage.getItem('minecore.userId')
  const h = {}
  if (orgId) h['X-Organization-Id'] = orgId
  if (userId) h['X-User-Id'] = userId
  return h
}

export const api = {
  list: (params = {}) => {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v != null),
    ).toString()
    return request(qs ? `${BASE}?${qs}` : BASE, { headers: authHeaders() })
  },
  get: (id) => request(`${BASE}/${id}`, { headers: authHeaders() }),
  audit: (id) => request(`${BASE}/${id}/audit`, { headers: authHeaders() }),
  create: (data) =>
    request(BASE, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: authHeaders(),
    }),
  update: (id, data) =>
    request(`${BASE}/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
      headers: authHeaders(),
    }),
  remove: (id) =>
    request(`${BASE}/${id}`, { method: 'DELETE', headers: authHeaders() }),
  record: (id) =>
    request(`${BASE}/${id}/record`, { method: 'POST', headers: authHeaders() }),
  approve: (id) =>
    request(`${BASE}/${id}/approve`, { method: 'POST', headers: authHeaders() }),
  cancel: (id, reason) =>
    request(`${BASE}/${id}/cancel`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
      headers: authHeaders(),
    }),
}
