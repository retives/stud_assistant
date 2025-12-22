<template>
    <div v-if="token">
        <div class="profile-card">
            <div class="info">
                <div class="username">{{ user.username || 'Guest' }}</div>
                <div class="email" v-if="user.email">{{ user.email }}</div>
            </div>
            <div class="avatar">
                <img src="/stud_assistant/src/assets/avatar-placeholder.jpeg" alt="avatar" />
            </div>
        </div>
    </div>
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
import { getToken } from '@/utils/localStorage'
import { readJWT } from '@/utils/readJWT'
import { useRouter } from 'vue-router'


const token = getToken()
const user = token ? readJWT(token) : { username: 'Guest' }
const router = useRouter()
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
