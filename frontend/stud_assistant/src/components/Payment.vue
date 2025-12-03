<template>
<head>
  <title>Stripe PaymentIntent Demo</title>
  <script src="https://js.stripe.com/v3/"></script>
</head>
<body>
  <h1>Pay $10</h1>
  <form id="payment-form">
    <div id="card-element"></div>
    <button type="submit">Pay</button>
    <div id="payment-result"></div>
  </form>

  <script>
    import { getTokem } from "../utils/localStorage"

    const stripe = Stripe("pk_test_51SZpU01fYwurwjWvwYipBvqsLMqWq4UJXhhQlZo77k1Ru46yeqSCcQXurIXRufobp65hru7Lajp5Z7JFH5kkAZ9U008p2zbvo8"); 
    const elements = stripe.elements();
    const card = elements.create("card");
    const token = 
    card.mount("#card-element");

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
    });

    form.addEventListener("submit", async (e)) => {
      e.preventDefault();
      const res = await fetch("http://127.0.0.1:8000/payments/subscribe", {
        method: "POST",
        headers: {
          "Content-Type":"application/json",
          "Authorization": `Bearer ${token}`,
        },
        body:{
        }
      })

      const data = await res.json()
      return data
    }
  </script>
</body>
</template>
