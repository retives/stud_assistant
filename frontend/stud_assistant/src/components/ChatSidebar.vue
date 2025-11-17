<template>
  <aside :class="['chat-sidebar', { open: visible }]" @click.stop>
    <header class="sidebar-header">
      <h3>Conversations</h3>
      <button class="close-btn" @click="$emit('update:visible', false)">✕</button>
    </header>

    <div class="chat-list">
      <div v-if="loading" class="empty">Loading...</div>
      <div v-else-if="error" class="empty">Error: {{ error }}</div>
      <div v-else-if="(!displayChats || displayChats.length === 0)" class="empty">No conversations</div>
      <ul v-else>
        <li v-for="chat in sortedChats" :key="chat.id">
          <router-link :to="`/chat/${chat.id}`" class="chat-link" @click="$emit('update:visible', false)">
            <div class="title">{{ chat.title || 'Untitled' }}</div>
            <div class="meta">{{ formatDate(chat.date_changed) }}</div>
          </router-link>
        </li>
      </ul>
    </div>
  </aside>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { getToken } from '../utils/localStorage'

const props = defineProps({
  chats: { type: Array, default: () => [] },
  visible: { type: Boolean, default: false }
})

const localChats = ref([])
const loading = ref(false)
const error = ref(null)

const token = getToken()
const hasToken = !!token

const displayChats = computed(() => {
  // If user has a token prefer fetched conversations; otherwise use passed-in chats when available
  if (hasToken) return localChats.value
  return (props.chats && props.chats.length) ? props.chats : localChats.value
})

const sortedChats = computed(() => {
  const list = displayChats.value || []
  return [...list].sort((a, b) => {
    const da = a.date_changed ? new Date(a.date_changed) : new Date(0)
    const db = b.date_changed ? new Date(b.date_changed) : new Date(0)
    return db - da
  })
})

function formatDate(d) {
  if (!d) return ''
  try {
    return new Date(d).toLocaleString()
  } catch (e) {
    return d
  }
}

async function fetchConversations() {
  const token = getToken()
  if (!token) return
  loading.value = true
  error.value = null
  try {
    const res = await fetch('http://localhost:7000/conversations', {
      headers: { 'Authorization': `Bearer ${token}` },
      credentials: 'include'
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    if (Array.isArray(data)) {
      localChats.value = data
    } else if (data && Array.isArray(data.conversations)) {
      localChats.value = data.conversations
    } else {
      localChats.value = []
    }
  } catch (err) {
    console.error('Failed to fetch conversations', err)
    error.value = err.message || String(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // fetch if user is logged in
  fetchConversations()
})
</script>

<style scoped>
.chat-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 280px;
  background: var(--color-background-soft, #ffffff);
  border-right: 1px solid var(--color-border, #e5e5e5);
  transform: translateX(-100%);
  transition: transform 240ms ease-in-out;
  z-index: 1200;
  display: flex;
  flex-direction: column;
  padding: 12px;
  box-shadow: 2px 0 10px rgba(0,0,0,0.06);
}
.chat-sidebar.open { transform: translateX(0%); }
.sidebar-header { display:flex; align-items:center; justify-content:space-between; padding:8px 4px; }
.sidebar-header h3 { margin:0; font-size:1.05rem; }
.close-btn { background:transparent; border:none; font-size:1.1rem; cursor:pointer }
.chat-list { overflow:auto; padding-top:8px }
.chat-list ul { list-style:none; padding:0; margin:0 }
.chat-link { display:block; padding:10px; border-radius:8px; text-decoration:none; color:var(--color-text); }
.chat-link:hover { background:rgba(0,0,0,0.03); }
.title { font-weight:600 }
.meta { font-size:0.85rem; color:rgba(0,0,0,0.5) }
.empty { padding:12px; color:rgba(0,0,0,0.5) }
</style>
