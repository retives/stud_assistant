
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
import { useRoute } from 'vue-router'
import { getToken } from '@/utils/localStorage'
import { readJWT } from '@/utils/readJWT'

const route = useRoute()
const conversationId = ref(route.params.id || '1')

const messages = ref([])
const input = ref('')
const loading = ref(true)
const sending = ref(false)
const error = ref(null)
const messagesContainer = ref(null)

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

onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
.chat-app {
  max-width: 600px;
  margin: 40px auto;
  font-family: 'Inter', sans-serif;
  display: flex;
  flex-direction: column;
  height: 80vh;
  border: 1px solid #ccc;
  border-radius: 12px;
  overflow: hidden;
  background: #1e1e2f;
  color: #e0e0e0;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}

.messages {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
  background: #252535;
}

.message {
  display: flex;
  flex-direction: column;
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(90deg, #4ade80, #22d3ee);
  color: #012;
  padding: 10px 14px;
  border-radius: 12px 12px 4px 12px;
  max-width: 75%;
  word-wrap: break-word;
}

.message.assistant {
  align-self: flex-start;
  background: #3b3b55;
  padding: 10px 14px;
  border-radius: 12px 12px 12px 4px;
  max-width: 75%;
  word-wrap: break-word;
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
  padding: 12px;
  border-top: 1px solid #444;
  background: #1f1f2d;
  gap: 8px;
}

.composer input {
  flex: 1;
  padding: 10px 12px;
  border-radius: 8px;
  border: none;
  background: #2a2a3d;
  color: #e0e0e0;
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
  background: #4ade80;
  color: #012;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.composer button:hover:not(:disabled) {
  background: #22d3ee;
}

.composer button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

::-webkit-scrollbar-track {
  background: transparent;
}
</style>

