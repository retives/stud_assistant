<template>
    <!-- Profile -->
     
    <div v-if="token" @click="isMenuOpen = false; isEditOpen = false">
        <button class="profile-actions" @click.stop="toggleMenu()">
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
        <div v-if="isMenuOpen" @click.stop class="menu">
            <button class="menu-item" @click="toggleEdit()">Edit</button>
            <button class="menu-item" @click="handleLogout()">Logout</button>
        </div>
        <!-- Edit Profile Modal -->
        <EditProfile v-if="isEditOpen" @close="closeEdit" />
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
import EditProfile from './EditProfile.vue'

// Backend base URL from env
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:7000'

const token = getToken()
const user = token ? readJWT(token) : { username: 'Guest' }
const router = useRouter()

// boolean menu state; toggles between true/false
const isMenuOpen = ref(false)
const isEditOpen = ref(false)

function toggleMenu() {
    isMenuOpen.value = !isMenuOpen.value
}

function toggleEdit() {
    isEditOpen.value = true
    isMenuOpen.value = false // Close menu when opening edit
}

function closeEdit() {
    isEditOpen.value = false
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

    removeToken()
    isMenuOpen.value = false
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
.profile-card { background:linear-gradient(180deg,#0f1724, #121426)}
.profile-actions {background:transparent; border: none; }
.profile-card .info{ display:flex; flex-direction:column }
.profile-card .username{ font-weight:700 }
.menu-item { display:block; width:100%; text-align:left; background:transparent; border:none; color:#e6faff; padding:8px 10px; cursor:pointer; border-radius:0px }
.menu { position:absolute; right:0;  background:linear-gradient(180deg,#0f1724, #121426); border:1px solid rgba(255,255,255,0.04); padding:6px; border-radius:8px; box-shadow:0 8px 24px rgba(2,6,23,0.6); min-width:120px; z-index:1300; width: 100%; }

.profile-card .avatar img{ width:40px; height:40px; object-fit:cover; border-radius:50% }
</style>
