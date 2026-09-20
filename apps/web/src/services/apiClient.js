/**
 * Minimal fetch wrapper.
 *
 * Phase 02 will replace the auth header logic with real JWT handling.
 * Until then, X-User-Id and X-Organization-Id are read from
 * localStorage, falling back to the seeded demo org/user.
 */

const DEMO_USER_ID = '00000000-0000-0000-0000-000000000002'
const DEMO_ORG_ID = '00000000-0000-0000-0000-000000000001'

const API_BASE = import.meta.env.VITE_API_URL || ''

function authHeaders() {
  return {
    'X-User-Id': localStorage.getItem('minecore.userId') || DEMO_USER_ID,
    'X-Organization-Id': localStorage.getItem('minecore.orgId') || DEMO_ORG_ID,
  }
}

async function request(method, path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  })

  if (res.status === 204) return null

  const text = await res.text()
  const data = text ? JSON.parse(text) : null

  if (!res.ok) {
    const err = new Error((data && data.detail) || res.statusText)
    err.status = res.status
    err.body = data
    throw err
  }

  return data
}

export const api = {
  get: (path) => request('GET', path),
  post: (path, body) => request('POST', path, body),
  patch: (path, body) => request('PATCH', path, body),
  del: (path) => request('DELETE', path),
}
