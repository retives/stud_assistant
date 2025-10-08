<template>
  <div class="auth-page">
    <h2>Sign Up</h2>
    <form @submit.prevent="handleSignup" class="auth-form">
      <div class="input-group">
        <label>Email</label>
        <input type="email" v-model="email" placeholder="Enter email" :class="{ error: emailError }" />
        <p v-if="emailError" class="error-msg">{{ emailError }}</p>
      </div>

      <div class="input-group">
        <label>Username</label>
        <input type="text" v-model="username" placeholder="Enter username" :class="{ error: usernameError }" />
        <p v-if="usernameError" class="error-msg">{{ usernameError }}</p>
      </div>

      <div class="input-group">
        <label>Password</label>
        <input type="password" v-model="password" placeholder="Enter password" :class="{ error: passwordError }" />
        <p v-if="passwordError" class="error-msg">{{ passwordError }}</p>
      </div>

      <div class="input-group">
        <label>Repeat Password</label>
        <input type="password" v-model="repeatPassword" placeholder="Repeat password" :class="{ error: repeatPasswordError }" />
        <p v-if="repeatPasswordError" class="error-msg">{{ repeatPasswordError }}</p>
      </div>

      <button type="submit">Sign Up</button>
      <p v-if="serverError" class="error-msg server">{{ serverError }}</p>

      <div class="links">
        <router-link to="/login">Log in</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SignupPage",
  data() {
    return {
      email: "",
      username: "",
      password: "",
      repeatPassword: "",
      emailError: "",
      usernameError: "",
      passwordError: "",
      repeatPasswordError: "",
      serverError: "",
    };
  },
  methods: {
    async handleSignup() {
      this.clearErrors();

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!emailPattern.test(this.email)) {
        this.emailError = "Enter a valid email address.";
      }
      if (this.username.length < 3) {
        this.usernameError = "Username must be at least 3 characters.";
      }
      if (this.password.length < 8) {
        this.passwordError = "Password must be at least 8 characters.";
      }
      if (this.password !== this.repeatPassword) {
        this.repeatPasswordError = "Passwords do not match.";
      }

      if (this.emailError || this.usernameError || this.passwordError || this.repeatPasswordError) return;

      try {
        await axios.post("http://localhost:8000/signup", {
          email: this.email,
          username: this.username,
          password: this.password,
        });
        this.$router.push("/login");
      } catch (error) {
        if (error.response && error.response.status >= 500) {
          this.serverError = "Server error, please try again later.";
        } else if (error.response && error.response.data.detail) {
          this.serverError = error.response.data.detail;
        } else {
          this.serverError = "Signup failed. Please check your input.";
        }
      }
    },
    clearErrors() {
      this.emailError = "";
      this.usernameError = "";
      this.passwordError = "";
      this.repeatPasswordError = "";
      this.serverError = "";
    },
  },
};
</script>

<style scoped src="@/assets/auth.css"></style>
