<template>
    <div class="modal-overlay" @click="emit('close')">
        <div class="edit-profile-modal" @click.stop>
            <h2>Edit profile</h2>

            <div class="input-group">
                <label>Profile Picture</label>
                <!-- Add the image handling -->
                <input type="file" accept="image/png, image/gif, image/jpeg" name="picture" @change="handleFileUpload">
                <div v-if="previewUrl" class="image-preview">
                    <img class="preview-image" :src="previewUrl" alt="Preview" />
                </div>
                <p v-if="usernameError" class="error-msg">{{ usernameError }}</p>
            </div>

            <div class="input-group">
                <label>Name</label>
                <input type="text" v-model="username" :placeholder="user.username" name="username">
                <p v-if="usernameError" class="error-msg">{{ usernameError }}</p>
            </div>
            <div class="actions">
                <button @click="saveProfile">Save</button>
                <button @click="cancelEdit">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { getToken, setToken, removeToken } from '@/utils/localStorage'
import { readJWT } from '@/utils/readJWT'
import axios from "axios";
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:7000'

const token = getToken()
const user = token ? readJWT(token) : { username: 'Guest' }
const username = ref(user.username || '')
const usernameError = ""
const previewUrl = ref(null)
const selectedFile = ref(null)

function handleFileUpload(event) {
    const file = event.target.files[0]
    if (file) {
        selectedFile.value = file
        previewUrl.value = URL.createObjectURL(file)
    }
}
async function saveProfile() {
  try {
    const response = await axios.patch(`${API_BASE}/update-account`, 
      { username: username.value },
      {
        headers: { 'Authorization': `Bearer ${token}` },
        withCredentials: true
      }
    );

    const newToken = response.data.access_token; 
    removeToken()
    setToken(newToken);
    emit('close');

  } catch (err) {
    if (err.response) {
      console.error("Server Error:", err.response.data);
    } else {
      console.error("Network Error:", err.message);
    }
  }
}

function cancelEdit() {
    emit('close')
}

const emit = defineEmits(['close'])
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1500;
}

.edit-profile-modal {
    background: linear-gradient(180deg, #0f1724, #121426);
    border: 1px solid rgba(255, 255, 255, 0.04);
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 12px 32px rgba(2, 6, 23, 0.8);
    min-width: 400px;
    max-width: 500px;
    z-index: 1600;
}

.input-group {
    margin-bottom: 20px;
}

label {
    display: block;
    color: #eef2f6;
    margin-bottom: 8px;
    font-weight: 500;
}

input {
    width: 100%;
    padding: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.05);
    color: #eef2f6;
    font-size: 16px;
}

input:focus {
    outline: none;
    border-color: rgba(255, 255, 255, 0.3);
}

.actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
    margin-top: 24px;
}

button {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    background: rgba(255, 255, 255, 0.1);
    color: #eef2f6;
    font-size: 16px;
    transition: background 0.2s;
}

.image-preview {
    margin-top: 10px;
    text-align: center;
}

.image-preview img {
    /* max-width: 150px;
    max-height: 150px; */
    width: 150px;
    height: 150px;
    border-radius: 8px;
    object-fit: cover;
    /* border: 2px solid rgba(255, 255, 255, 0.1); */
    border-radius: 50%;
}

</style>