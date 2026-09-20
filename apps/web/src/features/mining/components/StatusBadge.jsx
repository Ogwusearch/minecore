const COLORS = {
  draft:     { bg: '#334155', fg: '#e2e8f0' },
  recorded:  { bg: '#1e40af', fg: '#dbeafe' },
  approved:  { bg: '#166534', fg: '#dcfce7' },
  cancelled: { bg: '#7f1d1d', fg: '#fee2e2' },
}

export default function StatusBadge({ status }) {
  const { bg, fg } = COLORS[status] || COLORS.draft
  return (
    <span
      style={{
        background: bg,
        color: fg,
        padding: '2px 8px',
        borderRadius: '999px',
        fontSize: '0.75rem',
        fontWeight: 600,
        textTransform: 'uppercase',
        letterSpacing: '0.05em',
      }}
    >
      {status}
    </span>
  )
}
