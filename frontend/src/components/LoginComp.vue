<template>
  <div>
    <h2 class="h2Auth">Login</h2>
    <form @submit.prevent="login" class="formAuth">
      <input v-model="username" placeholder="Username" required />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />
      <button type="submit" class="buttonAuth">Login</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
    <h5>
      Don't have an account?
      <span class="highlightText" @click="showRegister">register here</span>
    </h5>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        let response = await this.$http.post("/login", {
          username: this.username,
          password: this.password,
        });
        if (response.status === 200) {
          this.$emit("login-success");
          this.$router.push({ name: "user" });
        }
      } catch (error) {
        if (
          error.response &&
          error.response.status === 401 &&
          error.response.data &&
          error.response.data.message
        ) {
          this.errorMessage = error.response.data.message;
        } else {
          console.error("Login failed", error);
          this.errorMessage = "Login failed";
        }
      }
    },
    showRegister() {
      this.$emit("show-register");
    },
  },
};
</script>
