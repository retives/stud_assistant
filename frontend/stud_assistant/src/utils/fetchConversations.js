
import { getToken } from '@/utils/localStorage'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:7000'

/**
 * Fetch conversations and return a standardized result.
 * Returns: { data: Array, error: string|null }
 */
export async function fetchConversations() {
  const token = getToken()
  if (!token) return { data: [], error: 'Not authenticated' }

  try {
    const res = await fetch(`${API_BASE}/conversations/`, {
      headers: { 'Authorization': `Bearer ${token}` },
      credentials: 'include'
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    if (Array.isArray(data)) return { data, error: null }
    if (data && Array.isArray(data.conversations)) return { data: data.conversations, error: null }
    return { data: [], error: null }
  } catch (err) {
    console.error('Failed to fetch conversations', err)
    return { data: [], error: err.message || String(err) }
  }
}