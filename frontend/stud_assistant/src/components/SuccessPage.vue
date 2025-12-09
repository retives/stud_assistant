<template>
  <div class="status-page success-page">
    <div class="content-box">
      <i class="fas fa-check-circle success-icon"></i>
      <h2>Payment Successful!</h2>
      <p>Thank you for subscribing! Your Plus plan is now active.</p>
      <p v-if="sessionId">
        Confirmation ID: <strong id="session">{{ sessionId }}</strong>
      </p>
      <p class="next-step">
        You can now access all premium AI features.
      </p>
      
      <router-link to="/chat" class="action-button">
        Go to chats
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:7000'

export default {
  name: 'SuccessPage',
  data() {
    return {
      sessionId: null,
      verificationStatus: 'Verifying...',
    };
  },
  mounted() {
    this.sessionId = this.$route.query.session_id;

    if (this.sessionId) {
      this.verifySubscription();
    }
  },
  methods: {
    async verifySubscription() {
      try {
        await axios.post(
          `${API_BASE}/payments/verify-session`, 
          { session_id: this.sessionId },
          { withCredentials: true }
        );
        this.verificationStatus = 'Subscription confirmed.';
      } catch (error) {
        this.verificationStatus = 'Could not verify subscription status.';
        console.error('Verification failed:', error);
      }
    }
  }
};
</script>

<style scoped>
/* Add simple styling for status pages */
.status-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  text-align: center;
  
}

.content-box {
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  background: white;
  max-width: 500px;
  width: fit-content;
}

.success-icon {
  font-size: 60px;
  color: #4CAF50; /* Green */
  margin-bottom: 20px;
}

h2 {
  color: #333;
  margin-bottom: 10px;
}

p {
  color: #666;
  margin-bottom: 5px;
}

.next-step {
  margin-top: 20px;
  font-weight: bold;
}

.action-button {
  display: inline-block;
  margin-top: 30px;
  padding: 10px 20px;
  background-color: #5c67f2;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #4a54e6;
}
#session{
  font-size: 11px;
}
</style>