<template>
  <div id="app">
    <!-- Only show sidebar for authenticated users and not on landing page -->
    <chat-sidebar 
      v-if="showSidebar" 
      v-model:visible="sidebarOpen" 
      :chats="chats" 
    />

    <header v-if="showSidebar" class="topbar">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">☰</button>
      <!-- Only the title will slide when the sidebar opens; the button is fixed -->
      <div class="app-title" :class="{ shifted: showSidebar && sidebarOpen }">Study Assistant</div>
    </header>

    <!-- Show profile card on landing page (root) so guests can login/signup -->
    <ProfileCard class="global-profile" />

    <main class="main-area" :class="{ 'shifted': showSidebar && sidebarOpen }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import ChatSidebar from './components/ChatSidebar.vue'
import ProfileCard from './components/ProfileCard.vue'
import { getToken } from './utils/localStorage'

// Sidebar visible by default; user can toggle to hide it
const sidebarOpen = ref(true)

// Reactive auth token: poll localStorage so SPA updates when token changes
const authToken = ref(getToken())
let pollId = null
onMounted(() => {
  pollId = setInterval(() => {
    authToken.value = getToken()
  }, 500)
})
onUnmounted(() => {
  if (pollId) clearInterval(pollId)
})

// Show sidebar only for authenticated users
const showSidebar = computed(() => !!authToken.value)

// Show profile card on the landing page (Home) for unauthenticated users
const route = useRoute()
const isLanding = computed(() => (route.name === 'Home' || route.path === '/') && !showSidebar.value)

// Example data in the format you specified. In real use pass this in or fetch from the API.
const chats = ref([
  {
    owner_id: '1abd2afd-6f88-4e59-9a8e-7864223462fe',
    id: 'f430a1ec-e03c-4638-b99e-e7d766302c6b',
    title: 'New chat',
    date_changed: '2025-11-17T06:57:19'
  },
  {
    owner_id: '1abd2afd-6f88-4e59-9a8e-7864223462fe',
    id: 'eae5b870-63e0-447b-a88c-6df03430ae62',
    title: 'New chat',
    date_changed: '2025-11-17T06:57:22'
  }
])
</script>

<style scoped>
.topbar {
  height: 56px;
  display:flex;
  align-items:center;
  gap:12px;
  padding:0 12px;
  border-bottom:1px solid var(--color-border, #e5e5e5);
}
.menu-btn { font-size:30px; background:transparent; border:none; cursor:pointer; color: #ffffff; margin-bottom: 10px; }
.menu-btn { position: fixed; top: 12px; left: 12px; z-index: 1400 }
.app-title { font-weight:700; display:inline-block; margin-left:48px; transition: transform 240ms ease-in-out }
.app-title.shifted { transform: translateX(280px); }
.main-area { padding:18px; transition: margin-left 240ms ease-in-out }
.main-area.shifted { margin-left: 280px }
#app { min-height:100vh; background:var(--color-background); color:var(--color-text) }

/* Global profile card positioning */
.global-profile{ position: fixed; top: 20px; right: 20px; z-index: 1500 }
</style>