<template>
  <div>
    <!-- For authenticated users, show chat interface -->
    <div v-if="isAuthenticated" class="authenticated-home">
      <div class="welcome-message">
        <h1>Welcome back to Stud Assistant!</h1>
        <p>Select a conversation from the sidebar or start a new chat.</p>
      </div>
    </div>
    
    <!-- For guests, show landing page -->
    <LandingPage v-else />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getToken } from '@/utils/localStorage'
import LandingPage from './LandingPage.vue'
import { fetchConversations } from '@/utils/fetchConversations'

const router = useRouter()
const isAuthenticated = computed(() => !!getToken())

// For authenticated users, redirect to first conversation or show welcome
onMounted(async () => {
  if (isAuthenticated.value) {
    const result = await fetchConversations()
    if (result.data && result.data.length > 0) {
      // Redirect to the most recent conversation
      const mostRecent = result.data.sort((a, b) => 
        new Date(b.date_changed) - new Date(a.date_changed)
      )[0]
      router.replace(`/chat/${mostRecent.id}`)
    }
    // If no conversations, stay on home to show welcome message
  }
})
</script>

<style scoped>
.authenticated-home {
  padding: 2rem;
  text-align: center;
  color: #f8fafc;
}

.welcome-message h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.welcome-message p {
  font-size: 1.2rem;
  color: #cbd5e1;
}
</style>