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
        <li v-for="chat in sortedChats" :key="chat.id" class="chat-item">
          <router-link :to="`/chat/${chat.id}`" class="chat-link" @click="$emit('update:visible', false)">
            <div class="title">{{ chat.title || 'Untitled' }}</div>
            <div class="meta">{{ formatDate(chat.date_changed) }}</div>
          </router-link>
          <div class="actions">
            <button class="dots" @click.stop="toggleMenu(chat.id)" aria-label="Open actions">⋮</button>
            <div v-if="openedMenuId === chat.id" class="menu" @click.stop>
              <button class="menu-item" @click="editConversation(chat.id)">Edit</button>
              <button class="menu-item" @click="deleteConversaiton(chat.id)">Delete</button>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </aside>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { getToken } from '../utils/localStorage'
// Backend base URL from env
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:7000'

const emit = defineEmits(['update:visible', 'edit-conversation'])

const props = defineProps({
  chats: { type: Array, default: () => [] },
  visible: { type: Boolean, default: false }
})
const localChats = ref([])
const loading = ref(false)
const error = ref(null)

const token = getToken()
const hasToken = !!token

// Menu state for actions (which conversation menu is open)
const openedMenuId = ref(null)

function toggleMenu(conversationID) {
  openedMenuId.value = openedMenuId.value === conversationID ? null : conversationID
}

function editConversation(conversationID) {
  // emit to parent for handling edit flow
  emit('edit-conversation', conversationID)
  openedMenuId.value = null
}

// Close menu when clicking outside
function onDocumentClick(e) {
  openedMenuId.value = null
}

onMounted(() => {
  // fetch if user is logged in
  fetchConversations()
  document.addEventListener('click', onDocumentClick)
})

onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick)
})

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
  const res = await fetch(`${API_BASE}/conversations/`, {
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

async function deleteConversaiton(conversationID) {
  const token = getToken()
  if (!token) return
  loading.value = true
  error.value = null
  try {
  const res = await fetch(`${API_BASE}/conversations/${conversationID}/delete`,{
      method: "DELETE",
      headers: { 'Authorization': `Bearer ${token}` },
      credentials: 'include'
    })
    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`)
    }

    await fetchConversations()

  }catch (err) {
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
.meta { font-size:0.85rem; color: #8ff0ff; }
.chat-link { color: #eef2ff; }
.chat-item { display:flex; align-items:center; justify-content:space-between; gap:8px; padding-right:8px }
.actions { position:relative }
.dots { background:transparent; border:none; font-size:18px; cursor:pointer; color:#9be7ef; padding:6px; border-radius:6px }
.dots:hover { background:rgba(255,255,255,0.03) }
.menu { position:absolute; right:0; top:36px; background:linear-gradient(180deg,#0f1724, #121426); border:1px solid rgba(255,255,255,0.04); padding:6px; border-radius:8px; box-shadow:0 8px 24px rgba(2,6,23,0.6); min-width:120px; z-index:1300 }
.menu-item { display:block; width:100%; text-align:left; background:transparent; border:none; color:#e6faff; padding:8px 10px; cursor:pointer; border-radius:6px }
.menu-item:hover { background:rgba(255,255,255,0.02) }
.empty { padding:12px; color:rgba(0,0,0,0.5) }
</style>
