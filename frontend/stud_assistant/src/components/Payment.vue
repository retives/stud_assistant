<template>
  <div class="auth-page">
    <h2>Upgrade to Plus</h2>

    <form @submit.prevent="startCheckout" class="auth-form"> 
      
      <div class="input-group">
        <label>Subscription Plan</label>
        
        <select v-model="selectedPlan" :class="{ error: planError }"> 
          <option disabled value="">Select a plan</option>
          <option value="plus_monthly">Plus (Monthly)</option>
        </select>
        <p v-if="planError" class="error-msg">{{ planError }}</p>
      </div>

      <div class="input-group">
        <label>Benefits</label>
        <ul class="benefits-list">
          <li>Unlimited AI interactions</li>
          <li>Faster response times</li>
          <li>Priority queue</li>
          <li>Access to premium tools</li>
        </ul>
      </div>

      <button type="submit">Proceed to Checkout</button>

      <p v-if="serverError" class="error-msg server">{{ serverError }}</p>

      <div class="links">
        <router-link :to="{ name: 'Home' }">Back to Dashboard</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { getToken } from '../utils/localStorage';
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:7000'

export default { 
  
  name: "SubscriptionPage",
  data() {
    return {
      selectedPlan: "",
      planError: "",
      serverError: "",
    };
  },
  methods: {
    
    async startCheckout() {
      
      const token = getToken()
      console.log(token)
      this.clearErrors();

      if (!this.selectedPlan) {
        this.planError = "Please select a subscription plan.";
        return;
      }

      try {
        const response = await axios.post(
          `${API_BASE}/payments/create-checkout-session`,
          { selected_plan: this.selectedPlan },
          {
            withCredentials: true,
            headers: {
              "Authorization": `Bearer ${token}` 
            }
          }
        );

        if (response.data.url) {
          window.location.href = response.data.url; // Redirect to Stripe
        } else {
          this.serverError = "Unable to start checkout session.";
        }
      } catch (error) {
        if (error.response && error.response.status >= 500) {
          this.serverError = "Server error, please try again later.";
        } else if (error.response?.data?.detail) {
          this.serverError = error.response.data.detail;
        } else {
          this.serverError = "Failed to begin checkout.";
        }
      }
    },
    clearErrors() {
      this.planError = "";
      this.serverError = "";
    },
  },
}; 
</script>

<style scoped src="@/assets/auth.css">
.auth-page{
  width: max-content;
  min-width: 200px;
}
</style>