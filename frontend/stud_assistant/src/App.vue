<template>
  <div id="app">
    <chat-sidebar v-model:visible="sidebarOpen" :chats="chats" />

    <header class="topbar">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">☰</button>
      <div class="app-title">Study Assistant</div>
    </header>

    <main class="main-area" :class="{ 'shifted': sidebarOpen }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatSidebar from './components/ChatSidebar.vue'

// Sidebar visible by default; user can toggle to hide it
const sidebarOpen = ref(true)

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
.menu-btn { font-size:20px; background:transparent; border:none; cursor:pointer }
.app-title { font-weight:700 }
.main-area { padding:18px; transition: margin-left 240ms ease-in-out }
.main-area.shifted { margin-left: 280px }
#app { min-height:100vh; background:var(--color-background); color:var(--color-text) }
</style>