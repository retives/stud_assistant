import { getToken } from '@/utils/localStorage'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:7000'

/**
 * Create a new conversation
 * Returns: { data: Conversation, error: string|null }
 */
export async function createConversation() {
  const token = getToken()
  if (!token) return { data: null, error: 'Not authenticated' }

  try {
    const res = await fetch(`${API_BASE}/conversations/new-conversation`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      credentials: 'include'
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    return { data, error: null }
  } catch (err) {
    console.error('Failed to create conversation', err)
    return { data: null, error: err.message || String(err) }
  }
}