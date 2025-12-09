
<template>
  <div class="chat-app">
    <div ref="messagesContainer" class="messages">
      <div v-if="loading" class="empty-state">Loading conversation...</div>
      <div v-else-if="error" class="error-state">{{ error }}</div>
      <div v-else-if="messages.length === 0" class="empty-state">No messages yet</div>
      <div v-else v-for="(msg, i) in messages" :key="i" :class="['message', msg.role]">
        <b>{{ msg.role }}:</b> {{ msg.content }}
      </div>
    </div>

    <div class="composer">
      <input
        v-model="input"
        @keyup.enter="sendMessage"
        placeholder="Type a message..."
        :disabled="loading || sending"
      />
      <button @click="sendMessage" :disabled="loading || sending || !input.trim()">
        {{ sending ? "Sending..." : "Send" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getToken } from '@/utils/localStorage'
import { readJWT } from '@/utils/readJWT'

const route = useRoute()
const router = useRouter()
const conversationId = ref(route.params.id || '1')

const messages = ref([])
const input = ref('')
const loading = ref(true) 
const sending = ref(false)
const error = ref(null)
const messagesContainer = ref(null)


onMounted(()=>{
  if (!getToken()){
    router.push("/login")
  }
})
// Special sender ID for AI responses
const ASSISTANT_SENDER_ID = '00000000-0000-0000-0000-000000000001'

// Determine role based on sender_id
function getRole(senderId) {
  return senderId === ASSISTANT_SENDER_ID ? 'assistant' : 'user'
}

// Scroll to bottom of messages
async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Fetch message history on mount
async function fetchHistory() {
  loading.value = true
  error.value = null
  try {
    const token = getToken()
    if (!token) {
      error.value = 'Not authenticated'
      return
    }

    const res = await fetch(`http://localhost:7000/conversations/${conversationId.value}`, {
      headers: { 'Authorization': `Bearer ${token}` },
      credentials: 'include'
    })
    if (!res.ok) throw new Error(`Failed to load conversation: ${res.status}`)

    const data = await res.json()
    // Expect data.messages or data.chat_history or similar; adapt to backend response
    const msgList = data.messages || data.chat_history || data || []
    messages.value = msgList.map(msg => ({
      content: msg.content || msg.message || '',
      role: getRole(msg.sender_id),
      sender_id: msg.sender_id,
      sender_name: msg.sender_name
    }))
    await scrollToBottom()
  } catch (err) {
    console.error('Failed to fetch history', err)
    error.value = err.message || 'Failed to load conversation'
  } finally {
    loading.value = false
  }
}

// Send a message
async function sendMessage() {
  if (!input.value.trim() || sending.value) return

  const token = getToken()
  if (!token) {
    error.value = 'Not authenticated'
    return
  }

  const payload = readJWT(token)
  const messageText = input.value.trim()
  console.log(messageText)
  input.value = ''

  // Add user message to UI immediately
  messages.value.push({
    content: messageText,
    role: 'user',
    sender_id: payload.user_id,
    sender_name: payload.username || 'You'
  })
  console.log("Message sent successfully")
  await scrollToBottom()

  sending.value = true
  error.value = null

  try {
    // Backend expects POST to /conversations/{id}/sendmessage and message_content as a query param
    const url = `http://localhost:7000/conversations/${conversationId.value}/sendmessage`
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body:JSON.stringify({
        message_content: messageText
      })
    })
    console.log(res)
    if (!res.ok) throw new Error(`Failed to send message: ${res.status}`)

    const data = await res.json()
    // Expect backend to return the AI response in data.content, data.message, or similar
    const aiContent = data.content || data.message || data.response || '[No response]'
    const aiSenderId = data.sender_id || ASSISTANT_SENDER_ID

    messages.value.push({
      content: aiContent,
      role: getRole(aiSenderId),
      sender_id: aiSenderId,
      sender_name: 'Assistant'
    })
    await scrollToBottom()
  } catch (err) {
    console.error('Failed to send message', err)
    error.value = err.message || 'Failed to send message'
    // Remove the unsent message from the UI
    messages.value.pop()
  } finally {
    sending.value = false
  }
}
onMounted(async () => {    
  const token = getToken()

  if (!token || !readJWT(token)) {
    return router.push("/login")
  }

  await fetchHistory()
})
</script>

<style scoped>
.chat-app {
  /* Fill most of the viewport on desktop while keeping a comfortable margin */
  position: fixed;
  inset: 40px; /* top/right/bottom/left margin */
  max-width: none;
  width: auto;
  padding: 20px;
  font-family: 'Inter', sans-serif;
  display: flex;
  flex-direction: column;
  height: auto;
  border-radius: 14px;
  overflow: hidden;
  background: linear-gradient(180deg,#171726 0%, #1e1e2f 100%);
  color: #e6e8ee;
  box-shadow: 0 18px 40px rgba(2,6,23,0.6);
  transition: max-width 200ms ease, padding 180ms ease;
}

.messages {
  flex: 1;
  padding: 28px 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  background: linear-gradient(180deg, rgba(37,37,53,0.06), rgba(37,37,53,0.02));
  font-size: 17px;
}

.message {
  display: flex;
  flex-direction: column;
  line-height: 1.4;
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(90deg, #4ade80 0%, #06b6d4 100%);
  color: #001219;
  padding: 16px 20px;
  border-radius: 14px 14px 6px 14px;
  max-width: 68%;
  word-wrap: break-word;
  box-shadow: 0 10px 30px rgba(3,10,14,0.35);
  font-weight: 600;
}

.message.assistant {
  align-self: flex-start;
  background: linear-gradient(180deg,#3b3b55 0%, #2f2f45 100%);
  padding: 14px 18px;
  border-radius: 14px 14px 14px 6px;
  max-width: 72%;
  word-wrap: break-word;
  box-shadow: 0 6px 20px rgba(10,12,20,0.25);
  color: #eef0f6;
}

.empty-state,
.error-state {
  margin: auto;
  padding: 20px;
  text-align: center;
  color: #888;
}

.error-state {
  color: #f87171;
}

.composer {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.04);
  background: rgba(18,19,30,0.85);
  gap: 12px;
}

.composer input {
  flex: 1;
  padding: 14px 16px;
  border-radius: 10px;
  border: none;
  background: #232333;
  color: #f0f3f7;
  font-size: 16px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
}

.composer input:focus {
  outline: none;
  box-shadow: 0 0 0 2px #4ade80;
}

.composer input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.composer button {
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
}

.composer button:hover:not(:disabled) {
  background: #22d3ee;
}

.composer button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Scrollbar tweaks */
.messages::-webkit-scrollbar {
  width: 10px;
}
.messages::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 6px;
}
.messages::-webkit-scrollbar-track {
  background: transparent;
}

/* Responsive adjustments */
@media (min-width: 1280px) {
  .chat-app {
    max-width: 1400px;
    height: 82vh;
  }
  .message.user, .message.assistant {
    max-width: 60%;
    font-size: 18px;
  }
  .composer button {
    min-width: 160px;
    padding: 14px 22px;
  }
}

@media (max-width: 600px) {
  .chat-app {
    /* On small screens revert to normal flow so it doesn't overlay other UI */
    position: static;
    inset: auto;
    margin: 16px;
    height: 85vh;
    border-radius: 8px;
  }
  .messages {
    padding: 12px;
    gap: 8px;
  }
  .message.user, .message.assistant {
    max-width: 85%;
    font-size: 14px;
  }
  .composer button {
    min-width: 80px;
    padding: 8px 12px;
  }
}
</style>

