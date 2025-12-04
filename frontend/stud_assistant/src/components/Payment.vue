<template>
  <div>
    <h1>Pay $10</h1>

    <form id="payment-form" @submit.prevent="submitPayment">
      <div id="card-element"></div>
      <button type="submit">Pay</button>
      <div id="payment-result">{{ result }}</div>
    </form>
  </div>
</template>

<script>
import { getToken } from "../utils/localStorage";

export default {
  data() {
    return {
      stripe: null,
      card: null,
      result: "",
    };
  },

  async mounted() {
    await this.loadStripe();

    this.stripe = window.Stripe(
      "pk_test_51SZpU01fYwurwjWvwYipBvqsLMqWq4UJXhhQlZo77k1Ru46yeqSCcQXurIXRufobp65hru7Lajp5Z7JFH5kkAZ9U008p2zbvo8"
    );

    const elements = this.stripe.elements();
    this.card = elements.create("card");
    this.card.mount("#card-element");
  },

  methods: {
    // Load Stripe.js dynamically
    loadStripe() {
      return new Promise((resolve) => {
        if (window.Stripe) return resolve();

        const script = document.createElement("script");
        script.src = "https://js.stripe.com/v3/";
        script.onload = resolve;
        document.head.appendChild(script);
      });
    },

    async submitPayment() {
      const token = getToken();

      const response = await fetch("http://127.0.0.1:8000/payments/subscribe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({}),
      });

      const data = await response.json();
      
      const result = await stripe.confirmCardPayment(clientSecret, {
        payment_method: { card: card }
      });

      const output = document.getElementById("payment-result");
      if (result.error) {
        output.textContent = "Payment failed: " + result.error.message;
      } else if (result.paymentIntent.status === "succeeded") {
        output.textContent = "Payment succeeded!";
      }
      console.log(output)
    },
  },
};
</script>
<!-- 
    const form = document.getElementById("payment-form");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const res = await fetch("http://127.0.0.1:8000/create-payment-intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: 1, amount: 1000, currency: "usd" }) // Example payload
      });
      const data = await res.json();
      const clientSecret = data.client_secret;

      const result = await stripe.confirmCardPayment(clientSecret, {
        payment_method: { card: card }
      });

      const output = document.getElementById("payment-result");
      if (result.error) {
        output.textContent = "Payment failed: " + result.error.message;
      } else if (result.paymentIntent.status === "succeeded") {
        output.textContent = "Payment succeeded!";
      }
    }); -->