
<template>
  <div class="chat-app">
    <div class="messages">
      <div v-for="(msg, i) in messages" :key="i" :class="msg.role">
        <b>{{ msg.role }}:</b> {{ msg.content }}
      </div>
    </div>

    <div class="composer">
      <input v-model="input" @keyup.enter="formRequestJson" placeholder="Type a message..." />
      <button @click="formRequestJson">Send</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SimpleChat",
  data() {
    return {  
      messages: [
        {"role":"system", "content":"Be a helpful assistant for students, find the info on university's website and read the timetable"},
        {"role":"user", "content":"Where is the Faculty of Computer Science in the IFNTUOG"},
        {"role":"assistant", "content":"Got it! The Faculty of Computer Science of Ivano-Frankivsk National Technical University of Oil and Gas is located at Berehova Street."}
      ],
      input: "",
      apiEndpoint: "https://localhost:11434",
      apiKey: "",
      model: "qwen2.5:latest",
      
    };
  },
  mounted() {
    axios.get('http://localhost:8000/')
      .then(response => {
        this.apiKey = response.data.apikey;
      })
      .catch(error => {
        console.error("Error fetching API key:", error);
      });
  },
  methods: {
    // Request method to the LLM
    async sendMessage() {
      if (!this.input.trim()) return;
      const userMsg = { role: "user", content: this.input };
      this.messages.push(userMsg);
      const inputCopy = this.input;
      this.input = "";

      try {
        const res = await fetch(this.apiEndpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.apiKey}`,
          },
          body: JSON.stringify({ model: this.model, messages: this.messages }),
        });
        const data = await res.json();
        const reply = data.choices?.[0]?.message?.content || "[No response]";
        this.messages.push({ role: "assistant", content: reply });
      } catch (e) {
        console.error(e);
        this.messages.push({ role: "assistant", content: "Error calling API" });
      }
    },
    async formRequestJson() {
      if (!this.input.trim()) return;
      const userMsg = { role: "user", content: this.input };
      this.messages.push(userMsg);
      const inputCopy = this.input;
      this.input = "";
    }
  },

};
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

.messages .user {
  align-self: flex-end;
  background: linear-gradient(90deg, #4ade80, #22d3ee);
  color: #012;
  padding: 10px 14px;
  border-radius: 12px 12px 4px 12px;
  max-width: 75%;
  word-wrap: break-word;
}

.messages .assistant {
  align-self: flex-start;
  background: #3b3b55;
  padding: 10px 14px;
  border-radius: 12px 12px 12px 4px;
  max-width: 75%;
  word-wrap: break-word;
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

.composer button {
  background: #4ade80;
  color: #012;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.composer button:hover {
  background: #22d3ee;
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

