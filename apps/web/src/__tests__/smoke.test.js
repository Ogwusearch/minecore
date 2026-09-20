import { describe, it, expect } from 'vitest'

describe('smoke', () => {
  it('environment is ready', () => {
    expect(1 + 1).toBe(2)
  })
})
