<template>
  <div class="auth-page">
    <h2>Log In</h2>
    <form @submit.prevent="handleLogin" class="auth-form">
      <div class="input-group">
        <label>Username</label>
        <input
          type="text"
          v-model="username"
          placeholder="Enter username"
          :class="{ error: usernameError }"
        />

        <p v-if="usernameError" class="error-msg">{{ usernameError }}</p>
      </div>

      <div class="input-group">
        <label>Password</label>
        <input
          type="password"
          v-model="password"
          placeholder="Enter password"
          :class="{ error: passwordError }"
        />
        <p v-if="passwordError" class="error-msg">{{ passwordError }}</p>
      </div>

      <button type="submit">Log In</button>
      <p v-if="serverError" class="error-msg server">{{ serverError }}</p>

      <div class="links">
        <!-- <a href="#">Forgot password?</a> -->
        <router-link to="/signup">Sign up</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { setToken } from "@/utils/localStorage";
export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      usernameError: "",
      passwordError: "",
      serverError: "",
    };
  },
  methods: {
    async handleLogin() {
      this.clearErrors();

      if (this.username.length < 3) {
        this.usernameError = "Username must be at least 3 characters.";
      }
      if (this.password.length < 8) {
        this.passwordError = "Password must be at least 8 characters.";
      }
      if (this.usernameError || this.passwordError) return;


      const params = new URLSearchParams()
      params.append('username', this.username);
      params.append('password', this.password);
      try {
        const response = await axios.post("http://localhost:7000/token", params,{
          headers: {
            'Content-Type':'application/x-www-form-urlencoded'
          }});

        setToken(response.data.access_token);
        this.$router.push("/");
      } catch (error) {
        if (error.response && error.response.status >= 500) {
          this.serverError = "Server error, please try again later.";
        } else if (error.response && error.response.data.detail) {
          this.serverError = error.response.data.detail;
        } else {
          this.serverError = "Invalid username or password.";
        }
      }
    },
    clearErrors() {
      this.usernameError = "";
      this.passwordError = "";
      this.serverError = "";
    },
  },
};
</script>

<style scoped src="@/assets/auth.css"></style>
