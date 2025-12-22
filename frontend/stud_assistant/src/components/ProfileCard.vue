<template>
    <!-- Profile -->
     
    <div v-if="token">
        <button class="profile-actions" @click="toggleMenu()">
            <div class="profile-card">
                <div class="info">
                    <div class="username">{{ user.username || 'Guest' }}</div>
                    <div class="email" v-if="user.email">{{ user.email }}</div>
                </div>
                <div class="avatar">
                    <img src="/stud_assistant/src/assets/avatar-placeholder.jpeg" alt="avatar" />
                </div>
            </div>
        </button>
        <!-- Action menu -->
        <div v-if="isMenuOpen">

            <button class="menu-item" @click="handleLogout()">Logout</button>
        </div>
    </div>

    <!-- Guest block -->
    <div v-else>
        <div class="profile-card">
            <button class="submit" @click="router.push('/login')">
                Log in
            </button>
            <button class="submit" @click="router.push('/signup')">
                Signup
            </button>
        </div>
    </div>
</template>

<script setup>

import { ref } from 'vue'
import { getToken, removeToken } from '@/utils/localStorage'
import { readJWT } from '@/utils/readJWT'
import { useRouter } from 'vue-router'
import { fetchConversations } from '@/utils/fetchConversations'

// Backend base URL from env
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:7000'

const token = getToken()
const user = token ? readJWT(token) : { username: 'Guest' }
const router = useRouter()

// boolean menu state; toggles between true/false
const isMenuOpen = ref(false)

function toggleMenu() {
    isMenuOpen.value = !isMenuOpen.value
}

function goToSignup() {
    router.push({ name: 'Signup' })
}

// Logout
async function handleLogout() {
    try {
        const currentToken = getToken()
        if (currentToken) {
            await fetch(`${API_BASE}/logout`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${currentToken}` },
                credentials: 'include'
            })
        }
    } catch (e) {
        console.error('Logout request failed (network issue or server down):', e)
    }

    // Clear client-side token and navigate to login.
    removeToken()
    isMenuOpen.value = false
    // Refresh conversations list (best-effort); helper returns data but we don't need it here.
    try { await fetchConversations() } catch (e) { /* ignore */ }
    router.replace({ name: 'Login' })
}

</script>

<style scoped>
.profile-card{
    display:flex;
    align-items:center;
    gap:12px;
    padding:8px 12px;
    border-radius:10px;
    background: rgba(255,255,255,0.02);
    color: #eef2f6;
    min-width: 160px;
    box-shadow: 0 6px 18px rgba(2,6,23,0.45);
}
.profile-card .info{ display:flex; flex-direction:column }
.profile-card .username{ font-weight:700 }
.profile-card .avatar img{ width:40px; height:40px; object-fit:cover; border-radius:50% }
</style>
