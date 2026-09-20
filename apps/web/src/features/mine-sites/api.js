import { api } from '../../services/apiClient.js'

export const listMineSites = () => api.get('/mine-sites')
export const getMineSite = (id) => api.get(`/mine-sites/${id}`)
export const createMineSite = (payload) => api.post('/mine-sites', payload)
export const updateMineSite = (id, payload) => api.patch(`/mine-sites/${id}`, payload)
export const deleteMineSite = (id) => api.del(`/mine-sites/${id}`)

export const listSiteAssignments = (id) => api.get(`/mine-sites/${id}/assignments`)
export const assignUserToSite = (id, userId) =>
  api.post(`/mine-sites/${id}/assignments`, { user_id: userId })
export const unassignUserFromSite = (id, userId) =>
  api.del(`/mine-sites/${id}/assignments/${userId}`)
