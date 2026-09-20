import { api } from '../../services/apiClient.js'

export function getCurrentOrganization() {
  return api.get('/organizations/current')
}

export function updateCurrentOrganization(payload) {
  return api.patch('/organizations/current', payload)
}
