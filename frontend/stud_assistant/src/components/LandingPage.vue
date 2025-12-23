<template>
  <div class="landing-page">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Welcome to Stud Assistant</h1>
        <p class="hero-subtitle">
          Your AI-powered study companion. Get help with homework, explanations, and learning assistance 24/7.
        </p>
        <div class="hero-actions">
          <button v-if="!token" @click="router.push('/login')" class="btn-primary">
            Get Started
          </button>
          <button v-if="token" @click="startNewChat" class="btn-primary">
            Start New Chat
          </button>
          <button v-if="!token" @click="router.push('/signup')" class="btn-secondary">
            Sign Up
          </button>
        </div>
      </div>
      <div class="hero-image">
        <div class="illustration">
          <div class="chat-bubble">
            <span>👋 Hi! I'm here to help you learn!</span>
          </div>
          <div class="robot-avatar">
            🤖
          </div>
        </div>
      </div>
    </div>

    <div class="features-section">
      <h2>What can Stud Assistant do?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">📚</div>
          <h3>Homework Help</h3>
          <p>Get step-by-step solutions and explanations for your assignments</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🧠</div>
          <h3>Concept Explanations</h3>
          <p>Understand complex topics with clear, simple explanations</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💬</div>
          <h3>24/7 Support</h3>
          <p>Available anytime to answer your questions and help you learn</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📝</div>
          <h3>Study Planning</h3>
          <p>Get help organizing your study schedule and materials</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getToken } from '@/utils/localStorage'
import { createConversation } from '@/utils/createConversation'

const router = useRouter()
const token = computed(() => getToken())

async function startNewChat() {
  const result = await createConversation()
  if (result.error) {
    console.error('Failed to create conversation:', result.error)
    // Could show an error message to user
    return
  }
  // Navigate to the new conversation
  router.push(`/chat/${result.data.id}`)
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f1724 0%, #1e293b 50%, #334155 100%);
  color: #f8fafc;
  position: relative;
  overflow-x: hidden;
}

.hero-section {
  display: flex;
  align-items: center;
  min-height: 80vh;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  gap: 4rem;
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #cbd5e1;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(59, 130, 246, 0.6);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #f8fafc;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.illustration {
  position: relative;
  width: 300px;
  height: 300px;
}

.robot-avatar {
  font-size: 4rem;
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
}

.chat-bubble {
  position: absolute;
  top: 20px;
  left: 20px;
  background: white;
  color: #1e293b;
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-width: 200px;
  font-weight: 500;
}

.chat-bubble::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 30px;
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 10px solid white;
}

.features-section {
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.features-section h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: #f8fafc;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #f8fafc;
}

.feature-card p {
  color: #cbd5e1;
  line-height: 1.6;
}

.profile-card-floating {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    padding: 1rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-actions {
    justify-content: center;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .illustration {
    width: 250px;
    height: 250px;
  }
}
</style>