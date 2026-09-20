import { api } from '../../services/apiClient.js'

export const listEmployees = () => api.get('/employees')
export const getEmployee = (id) => api.get(`/employees/${id}`)
export const createEmployee = (payload) => api.post('/employees', payload)
export const updateEmployee = (id, payload) => api.patch(`/employees/${id}`, payload)
export const deleteEmployee = (id) => api.del(`/employees/${id}`)
