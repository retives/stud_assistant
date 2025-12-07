<template>
  <div class="status-page cancel-page">
    <div class="content-box">
      <i class="fas fa-times-circle cancel-icon"></i>
      <h2>Payment Canceled</h2>
      <p>Your checkout session was canceled or incomplete.</p>
      <p class="next-step">
        No payment was processed. Feel free to try again or explore other options.
      </p>

      <router-link to="/pricing" class="action-button">
        Back to Pricing
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CancelPage',
};
</script>

<style scoped>
/* Reuse styles from SuccessPage, but change the color */
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
}

.cancel-icon {
  font-size: 60px;
  color: #f44336; /* Red */
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
  background-color: #f44336; /* Red for cancel button */
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #d32f2f;
}
</style>