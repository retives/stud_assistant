<template>
    <div class="not-found">
        <h1>The page you are looking for does not exist</h1>
        <button class="btn" @click="returnHome">Go home</button>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function returnHome() {
    // use named route so routing works with router base
    router.push({ name: 'Home' })
}
</script>

<style scoped>
.not-found { padding: 24px; text-align: center }
.btn { margin-top: 12px; padding: 8px 14px; border-radius: 8px; border: none; cursor: pointer; background: #06b6d4; color: #001219 }
</style>