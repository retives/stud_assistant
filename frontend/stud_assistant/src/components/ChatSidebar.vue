<template>
  <aside :class="['chat-sidebar', { open: visible }]" @click.stop>
    <header class="sidebar-header">
      <h3 v-if="hasToken">Conversations</h3>
      <h3 v-else>Stud Assistant</h3>
      <button class="close-btn" @click="$emit('update:visible', false)">✕</button>
    </header>

    <div v-if="hasToken" class="chat-list">
      <div class="new-conv"><button class="submit" @click="createNewConversation()">New chat</button></div>
      <div v-if="loading" class="empty">Loading...</div>
      <div v-else-if="error" class="empty">Error: {{ error }}</div>
      <div v-else-if="(!displayChats || displayChats.length === 0)" class="empty">No conversations</div>
      <ul v-else>
        <li v-for="chat in sortedChats" :key="chat.id" class="chat-item">
          <router-link :to="{ name: 'Chat', params: { id: chat.id } }" class="chat-link" @click="">
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
    
    <footer class="sidebar-footer">
      
      <button v-if="hasToken" class="submit" @click="goToSubscription">
        Subscribe to Plus
      </button>
      <button v-else class="submit" @click="router.push('/signup'); $emit('update:visible', false)">
        Sign Up
      </button>
    </footer>
    </aside>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { getToken, removeToken } from '../utils/localStorage'
import { useRouter } from 'vue-router'
import { readJWT } from '../utils/readJWT'
// import { fetchHistory } from './Chat.vue'
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
const router = useRouter()
const token = getToken()
// Ensure we treat a token as valid only if it decodes successfully.
const decodedToken = token ? readJWT(token) : null
const hasToken = !!decodedToken
const isPlus = decodedToken?.is ?? false

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
  // Only fetch conversations when we have a valid decoded token.
  if (!hasToken) {
    error.value = 'Not authenticated'
    return
  }

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
async function createNewConversation() {
  if (!token) return
  loading.value = true
  error.value = null
  try{
    const res = await fetch(`${API_BASE}/conversations/new-conversation`,{
      method: "POST",
      headers: { 'Authorization': `Bearer ${token}` },
      credentials: 'include'
    })
    const data = await res.json()
    let conversationId = data.id 
  router.replace({ name: 'Chat', params: { id: conversationId } })
    fetchConversations()
    // this.$forceUpdate();
  }catch (err) {
    console.error('Failed to fetch conversations', err)
    error.value = err.message || String(err)
  } finally {
    loading.value = false
  }
}
async function handleLogout() {
  // 1. Invalidate session on the backend
  try {
    const res = await fetch(`${API_BASE}/logout`, {
      method: "POST",
      headers: { 'Authorization': `Bearer ${token}` },
      credentials: 'include'
    })
  } catch (e) {
    console.error("Logout request failed (network issue or server down):", e)
  }


  removeToken()
  token.value = null 


  emit('update:visible', false)
  router.replace('/login')
}

function goToSubscription() {
  router.push({ name: 'Subscription' });
}
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
.submit{
  background: linear-gradient(90deg,#4ade80 0%, #06b6d4 100%);
  color: #001219;
  border: none;
  padding: 12px 22px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 800;
  font-size: 16px;
  min-width: 140px;
  box-shadow: 0 8px 24px rgba(6,182,212,0.18);
  width: 100%;
}
.sidebar-footer{
  align-self: center;
  display: flex;
  margin-top: auto;
  width: 100%;
}

</style>
