import { useState } from 'react'

export default function MiningOperationForm({ initial = {}, onSubmit }) {
  const [form, setForm] = useState({
    mine_site_id: initial.mine_site_id || '',
    pit_id: initial.pit_id || '',
    shift_id: initial.shift_id || '',
    material_id: initial.material_id || '',
    unit_id: initial.unit_id || '',
    operation_date: initial.operation_date || new Date().toISOString().slice(0, 10),
    quantity: initial.quantity || '',
    operator_name: initial.operator_name || '',
    equipment_note: initial.equipment_note || '',
    notes: initial.notes || '',
  })

  const change = (key) => (e) => setForm({ ...form, [key]: e.target.value })

  const submit = (e) => {
    e.preventDefault()
    const payload = { ...form }
    // Drop empty optional uuid fields
    for (const key of ['shift_id', 'unit_id']) {
      if (!payload[key]) delete payload[key]
    }
    onSubmit(payload)
  }

  return (
    <form onSubmit={submit} style={{ display: 'grid', gap: '0.75rem', maxWidth: 480 }}>
      <label>Mine Site ID<input required value={form.mine_site_id} onChange={change('mine_site_id')} /></label>
      <label>Pit ID<input required value={form.pit_id} onChange={change('pit_id')} /></label>
      <label>Shift ID<input value={form.shift_id} onChange={change('shift_id')} /></label>
      <label>Material ID<input required value={form.material_id} onChange={change('material_id')} /></label>
      <label>Unit ID<input value={form.unit_id} onChange={change('unit_id')} /></label>
      <label>Date<input type="date" required value={form.operation_date} onChange={change('operation_date')} /></label>
      <label>Quantity<input type="number" step="0.0001" required value={form.quantity} onChange={change('quantity')} /></label>
      <label>Operator name<input value={form.operator_name} onChange={change('operator_name')} /></label>
      <label>Equipment note<input value={form.equipment_note} onChange={change('equipment_note')} /></label>
      <label>Notes<textarea value={form.notes} onChange={change('notes')} /></label>
      <button type="submit">Create draft</button>
    </form>
  )
}
